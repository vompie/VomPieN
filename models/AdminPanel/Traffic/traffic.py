from TeleVompy.Interface.window import Window
from json import loads, dumps
from database.sql import get_user
from settings import STATS_FILE
from statsquery import stats_query

class Traffic(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '📈'
        self.Page.Content.title = 'Трафик'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            return self.Action.set_action(ActionType=self.Action.types.REDIRECT, redirect_to='MM')

        # back button        
        self.Page.add_button(model='BBck', row=1, callback=self.CallBack.create(dad='AdminPanel'))

        # get server stats
        result, stats_str = await stats_query()
        
        if not result:
            self.Page.Content.text = "Ошибка получения статистики\n"
            return 

        # parse users
        users = self.parse_stats(stats=stats_str)
        if not users:
            users = self.load_stats()
        else:
            self.save_stats(users=users)

        # add user info
        user_info = await self.add_user_info(users=users)

        # pagination
        self.Pagination.add(dataset=user_info, content_setter=self.content_setter, id_getter=self.id_getter)

        # callback
        callback = self.CallBack.copy(payload=self.relayed_payload, dad=self.name)
        callback.payload.Us = self.relayed_payload.sl
        callback.payload.Bt = self.name
        callback.payload.del_attr(attr='sl')

        # info button
        self.Page.add_button(model='Profile', row=1, callback=callback, block=(not self.relayed_payload.sl), answer='user_admin_not_select')

    def content_setter(self, item: dict) -> tuple[str, str]:
        """ Parse users and add to page """
        # header
        username = f"@{item['username']}" if item['username'] else item['tlg_id']
        status = '(пользователь)'
        if item['user_lvl'] == -1:
            status = '(разжалован)'
        elif item['user_lvl'] > 0:
            status = f"(администратор {item['user_lvl']}ур.)"
        elif item['is_banned'] == 1:
            status = '(забанен)'
        header = f"{username} {status}"
        # footer
        upload = f"🡹 Загружено: {self.get_mb_gb(value=item['uplink'])}"
        download = f"🡻 Скачано: {self.get_mb_gb(value=item['downlink'])}"
        traffic = f"{upload}\n{download}"
        created_at = f"Зарегистрирован: {item['created_at']}"
        full_info = f"{traffic}\n{created_at}"
        footer = self.Page.Content.html(full_info).quote_exp()
        return header, footer

    def id_getter(self, item: dict) -> None:
        return item['id']

    def parse_stats(self, stats: str) -> bool | dict:
        """
        Parse stats string and return dict with users and their traffic
        
        Example input stats: 
            `{"stat": [{"name": "user>>>123456789_4k9za@telegram.com>>>traffic>>>uplink", "value": 4996604}, {"name": "user>>>123456789_4k9za@telegram.com>>>traffic>>>downlink", "value": 111492104}]}, {"name": "user>>>123456789_31b6a@telegram.com>>>traffic>>>uplink", "value": 261266}, {"name": "user>>>123456789_31b6a@telegram.com>>>traffic>>>downlink", "value": 12013380}`
        
        """

        # string to dict
        stats_dict = {}
        try:
            stats_dict = loads(stats)['stat']
        except Exception as e:
            self.Page.Content.text += f"Ошибка парсинга статистики: {e}\n"
            return False
        
        # parsing users
        users = {}
        try:
            for item in stats_dict:
                try:
                    _, email, _, type_link = item['name'].split('>>>')
                    tlg_id = email.split('_')[0]
                    # add user
                    if tlg_id not in users:
                        users[tlg_id] = {
                            "uplink": 0,
                            "downlink": 0
                        }
                    # add link type and value
                    users[tlg_id][type_link] += int(item['value'])
                except Exception as e:
                    pass
        except Exception as e:
            self.Page.Content.text += f"Ошибка парсинга данных: {e}\n"
            return False
        
        # return users-values
        return users

    def save_stats(self, users: dict) -> None:
        """ Save users and their traffic to file """
        try:
            with open(STATS_FILE, 'w') as file:
                file.write(dumps(users))
        except Exception as e:
            pass

    def load_stats(self) -> dict:
        """ Load users and their traffic from file """
        try:
            with open(STATS_FILE, 'r') as file:
                self.Page.Content.text += "Данные не актуальны\n"
                return loads(file.read())
        except Exception as e:
            self.Page.Content.text += f"Ошибка чтения статистики: {e}\n"
            return {}

    async def add_user_info(self, users: dict) -> list[dict]:
        """ Add user info to users stats """
        data_set = []
        for user, item in users.items():
            user_info = await get_user(tlg_id=user)
            if user_info:
                u = {
                    'tlg_id': user,
                    'uplink': item['uplink'],
                    'downlink': item['downlink']
                }
                u['id'] = user_info['id']
                u['username'] = user_info['username']
                u['user_lvl'] = user_info['user_lvl']
                u['is_banned'] = user_info['is_banned']
                u['created_at'] = user_info['created_at']
                data_set.append(u)
        return data_set

    def get_mb_gb(self, value: int) -> str:
        """ Convert bytes to megabytes and gigabytes """
        if value <= 0:
            return f"0 Kb"
        mb = value / (1024 ** 2)  # 1 MB = 1024 * 1024 bytes
        gb = value / (1024 ** 3)   # 1 GB = 1024 * 1024 * 1024 bytes
        if gb > 0.5:
            return f"{gb:.2f} Gb"
        return f"{mb:.2f} Mb"
