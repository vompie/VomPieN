from TeleVompy.Interface.window import Window
from database.sql import get_user_keys, get_user, get_user_by_id, update_client, get_user_and_keys_by_id
from add_client import add_client
from delete_client import delete_client
from settings import MAX_CLIENT_KEYS, MAX_ADMINS_KEYS


class Keys(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🗝'
        self.Page.Content.title = 'Ключи доступа'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # from users/admins
        if self.relayed_payload.Us:
            keys = await get_user_and_keys_by_id(id=self.relayed_payload.Us, enabled=None)
            if keys and len(keys):
                username = f"@{keys[0]['username']}" if keys[0]['username'] else keys[0]['tlg_id']
                self.Page.Content.title = f'Ключи доступа {username}'
        # from main menu/command/profile
        else:
            keys = await get_user_keys(tlg_id=self.User.chat_id, enabled=True)    
                
        # callback
        callback = self.CallBack.copy(payload=self.relayed_payload, dad='Profile')
        callback.payload.del_attr(attr='Ks').del_attr(attr='sl').del_attr(attr='pg')

        # back to Profile (users/admins)
        if self.relayed_payload.Bt and self.relayed_payload.Bt != 'Profile':
            self.Page.add_button(model='BBck', row=2, callback=callback)
        # back to Profile (profile)
        elif self.relayed_payload.Bt == 'Profile':
            self.Page.add_button(model='BBck', row=2, callback=self.CallBack.create(dad='Profile'))
        # back to MM (mm/command)
        else:
            self.Page.add_button(model='BBck', row=2, title='В меню', callback=self.CallBack.create(dad='MM'))

        # max keys count
        max_keys = MAX_CLIENT_KEYS
        # admin
        if self.self_profile['is_admin'] == 1:
            max_keys = MAX_ADMINS_KEYS
        # super admin
        elif self.self_profile['is_admin'] > 1:
            max_keys = 99
        elif self.self_profile['is_banned'] == 1:
            max_keys = 0
        
        # new key button
        is_block = keys and len(keys) >= max_keys and self.self_profile['is_admin'] < 1
        self.Page.add_button(model='NewKey', row=2, callback=self.CallBack.copy(payload=self.relayed_payload), block=is_block, answer='cant_create_key') 
        
        # return immediately
        if not keys or not len(keys):
            return
         
        # setup select
        if self.relayed_payload.Ks:
            self.relayed_payload.sl = self.relayed_payload.Ks
            self.relayed_payload_del_attr(attr='Ks')
        # pagination
        self.Pagination.add(dataset=keys, content_setter=self.content_setter, id_getter=self.id_getter)

        # server info

        # callback
        callback = self.CallBack.copy(payload=self.relayed_payload, dad=self.name)
        callback.payload.Ks = self.relayed_payload.sl
        callback.payload.del_attr(attr='sl')

        # key button
        
        # enable / disable button
        if self.Pagination.selected_item and self.Pagination.selected_item['is_enabled']:
            self.Page.add_button(model='DisableKey', row=1, callback=callback)
        else:
            self.Page.add_button(model='EnableKey', row=1, callback=callback, block=(not self.Pagination.selected_item), answer='key_not_select')
                
        # delete button
        self.Page.add_button(model='DeleteKey', row=1, callback=callback, block=(not self.relayed_payload.sl), answer='key_not_select')

        # get key button
        self.Page.add_button(model='GetKey', row=1, callback=callback, block=(not self.relayed_payload.sl), answer='key_not_select')


    def content_setter(self, item: dict) -> tuple[str, str]:
        # admin view
        if self.self_profile['is_admin'] > 0:
            # header
            header = item['email']

            # user info
            user_type = 'пользователь'
            if item['is_admin'] == -1:
                user_type = 'пользователь (разжалован)'
            elif item['is_admin'] > 0:
                user_type = f"администратор ({item['is_admin']}ур.)"
            elif item['is_banned'] == 1:
                user_type = 'пользователь (забанен)'
            user_type = f"Клиент: {user_type}"
            username = f"@{item['username']}" if item['username'] else item['tlg_id']
            user = f"Имя/id: {username}"
            key_status = f"Состояние ключа: включен" if item['is_enabled'] else f"Состояние: отключен"

            # key info
            uuid = f"UUID: {item['uuid']}"
            level = f"Уровень: {item['level']}"
            created_at = f"Создан: {item['created_at']}"

            # full info
            user_info = f"{user}\n{user_type}\n{key_status}"
            key_info = f"{uuid}\n{level}\n{created_at}"
            full_info = f"{user_info}\n\n{key_info}"

            # footer
            footer = self.Page.Content.html(full_info).quote_exp()
        # user view
        else:
            header = item['uuid']
            footer = f"Создан: {item['created_at']}"
        return header, footer

    def id_getter(self, item: dict) -> None:
        return item['id']


class GetKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🎫'
        self.Page.Content.title = 'Получить'
        self.Action.action_type = "send"

    async def constructor(self) -> None:
        self.Page.Content.title = 'Ключ'
        self.Page.Content.text = 'Текст'

        """
        vless://
        ff369834-301b-4b2b-8fab-8397c40679a1
        @173.44.139.49:443/?
        encryption=none&
        type=http&
        sni=www.codewars.com&
        host=awesomehostnameinventedbyme.com&
        path=%2FgRlxW8LQDUvSKCY3cbPIGdGh&
        fp=random&
        security=reality&
        alpn=h2&
        pbk=cP1aVEjDhbEhqtO_rMxmurgxP3hlNjfwTSuVzNRy2wg&
        packetEncoding=xudp
        #AdminVless
        """


        self.Page.add_button(model='BYes')


class DeleteKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🗑'
        self.Page.Content.title = 'Удалить'
        self.Action.action_type = "click"

    async def constructor(self) -> None:
        await delete_client(id=self.relayed_payload.Ks)
        self.relayed_payload.del_attr('Ks')

class NewKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🔑'
        self.Page.Content.title = 'Новый ключ'
        self.Action.action_type = "click"
        self.relayed_payload.dad = 'Keys'

    async def constructor(self) -> None:
        # кому создается ключ проверки
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        keys = await get_user_keys(tlg_id=self.User.chat_id, enabled=True)
        if keys and len(keys) >= MAX_CLIENT_KEYS and self.self_profile['is_admin'] < 1:
            return
        await add_client(tlg_id=self.User.chat_id)


class EnableKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🌕'
        self.Page.Content.title = 'Включить'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        await update_client(id=self.relayed_payload.Ks, columns=['is_enabled'], values=[1])

class DisableKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🌑'
        self.Page.Content.title = 'Выключить'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        await update_client(id=self.relayed_payload.Ks, columns=['is_enabled'], values=[0])
