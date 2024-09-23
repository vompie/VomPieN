from TeleVompy.Interface.window import Window

from database.sql import get_user, get_user_left_join_keys, get_user_left_join_keys_by_user_id, get_keys_left_join_user
from settings import MAX_CLIENT_KEYS, MAX_ADMINS_KEYS


class Keys(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🗝'
        self.Page.Content.title = 'Ключи'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # from users_admins -> profile -> keys      UsersAdmins view
        if self.relayed_payload.Bt == 'UsersAdmins':
            user_keys = await get_user_left_join_keys_by_user_id(id=self.relayed_payload.Us)
            # callback
            callback = self.CallBack.copy(payload=self.relayed_payload, dad='Profile')
            callback.payload.del_attr(attr='Ks').del_attr(attr='sl').del_attr(attr='pg')
            # back to Profile button
            self.Page.add_button(model='BBck', row=2, callback=callback)

        # from admin_panel -> keys                  AdminPanel view
        elif self.relayed_payload.Bt == 'AdminPanel':
            user_keys = await get_keys_left_join_user()
            # back to AdminPanel button     
            self.Page.add_button(model='BBck', row=2, callback=self.CallBack.create(dad='AdminPanel'))

        # from main_menu/command -> keys            MainMenu view
        else:
            user_keys = await get_user_left_join_keys(tlg_id=self.User.chat_id)
            # back to MainMenu button     
            self.Page.add_button(model='BBck', row=2, title='В меню', callback=self.CallBack.create(dad='MM'))

        # return
        if not user_keys or not len(user_keys):
            return

        # max generate keys for UsersAdmins and MainMenu views
        if not self.relayed_payload.Bt or self.relayed_payload.Bt == 'UsersAdmins':
            max_keys = MAX_CLIENT_KEYS
            if user_keys[0]['is_banned']:
                max_keys = -1
            elif self.self_profile['user_lvl'] == 1:
                max_keys = MAX_ADMINS_KEYS
            elif self.self_profile['user_lvl'] > 1:
                max_keys = 99
            is_block = len(user_keys) >= max_keys

        # UsersAdmins view
        if self.self_profile['user_lvl'] > 0 and self.relayed_payload.Bt == 'UsersAdmins':
            # username
            username = f"@{user_keys[0]['username']}" if user_keys[0]['username'] else user_keys[0]['tlg_id']
            level = '(пользователь)'
            if user_keys[0]['user_lvl'] == -1:
                level = '(разжалован)'
            elif user_keys[0]['user_lvl'] > 0:
                level = f"(администратор {user_keys[0]['user_lvl']}ур.)"
            elif user_keys[0]['is_banned'] == 1:
                level = '(забанен)'
            self.Page.Content.title =  f"{username} {level}"
            # new key button
            self.Page.add_button(model='NewKey', row=2, title='Добавить ключ', callback=self.CallBack.copy(payload=self.relayed_payload), block=is_block, answer='cant_create_key')
        
        # MainMenu view
        elif not self.relayed_payload.Bt:
            # new key button
            self.Page.add_button(model='NewKey', row=2, callback=self.CallBack.copy(payload=self.relayed_payload), block=is_block, answer='cant_create_key')
     
        # return immediately
        if not user_keys or not len(user_keys) or not user_keys[0]['cid']:
            return
         
        # setup select
        if self.relayed_payload.Ks:
            self.relayed_payload.sl = self.relayed_payload.Ks
            self.relayed_payload_del_attr(attr='Ks')

        # pagination
        self.Pagination.add(dataset=user_keys, content_setter=self.content_setter, id_getter=self.id_getter)

        # server info
        server_info = self.Page.Content.html(self.server_info()).quote_exp()
        self.Page.Content.text += f"{server_info}"

        # callback
        callback = self.CallBack.copy(payload=self.relayed_payload, dad=self.name)
        callback.payload.Ks = self.relayed_payload.sl
        callback.payload.del_attr(attr='sl')
        
        # enable / disable button
        if self.self_profile['user_lvl'] > 0:
            if self.Pagination.selected_item and self.Pagination.selected_item['is_enabled']:
                self.Page.add_button(model='DisableKey', row=1, callback=callback)
            else:
                self.Page.add_button(model='EnableKey', row=1, callback=callback, block=(not self.Pagination.selected_item), answer='key_not_select')

        # delete button
        self.Page.add_button(model='DeleteKey', row=1, callback=callback, block=(not self.relayed_payload.sl), answer='key_not_select')
        
        # get key button
        self.Page.add_button(model='GetKey', row=1, callback=callback, block=(not self.relayed_payload.sl), answer='key_not_select')

        # profile button for AdminPanel view
        if self.relayed_payload.Bt == 'AdminPanel':
            self.Page.add_button(model='Profile', row=2, title='Владелец', callback=callback, block=(not self.relayed_payload.sl), answer='user_admin_not_select')


    def content_setter(self, item: dict) -> tuple[str, str]:
        # admin view for profile keys or user view
        if not self.relayed_payload.Bt or self.relayed_payload.Bt == 'UsersAdmins':
            # header
            header = item['uuid']
            # key info
            key_status = f"Состояние ключа: включен" if item['is_enabled'] else f"Состояние: отключен"
            level = f"Уровень: {item['level']}"
            created_at = f"Создан: {item['clients_created_at']}"
            full_info = f"{key_status}\n{created_at}"
            if self.self_profile['user_lvl'] > 0:
                full_info = f"{key_status}\n{level}\n{created_at}"
            # footer
            footer = self.Page.Content.html(full_info).quote_exp()
        # admin view for all keys
        else:
            # header
            header = item['email']
            # user info
            user_type = 'пользователь'
            if item['user_lvl'] == -1:
                user_type = 'пользователь (разжалован)'
            elif item['user_lvl'] > 0:
                user_type = f"администратор ({item['user_lvl']}ур.)"
            elif item['user_lvl'] == 1:
                user_type = 'пользователь (забанен)'
            user_type = f"Клиент: {user_type}"
            username = f"@{item['username']}" if item['username'] else item['tlg_id']
            user = f"Имя/id: {username}"
            key_status = f"Состояние ключа: включен" if item['is_enabled'] else f"Состояние: отключен"
            # key info
            uuid = f"UUID: {item['uuid']}"
            level = f"Уровень: {item['level']}"
            created_at = f"Создан: {item['clients_created_at']}"
            # full info
            user_info = f"{user}\n{user_type}\n{key_status}"
            key_info = f"{uuid}\n{level}\n{created_at}"
            full_info = f"{user_info}\n\n{key_info}"
            # footer
            footer = self.Page.Content.html(full_info).quote_exp()
        return header, footer

    def id_getter(self, item: dict) -> None:
        return item['cid']

    @staticmethod
    def server_info() -> str:
        from settings import BOT_NAME, BOT_SMILE, PROTOCOL, SERVER_IP, SERVER_PORT, SERVER_TYPE, SECURITY, ALPN, FINGERPRINT, PACKET_ENCODING
        
        title = f'Дополнительные данные для подключения к {BOT_NAME} {BOT_SMILE}'
        protocol = f"Protocol: {PROTOCOL}"
        ip = f'IP: {SERVER_IP}:{SERVER_PORT}'
        server_type = f"Type: {SERVER_TYPE}"
        security = f"Security: {SECURITY}"
        alpn = f"Alpn: {ALPN}"
        fp = f"Finger print: {FINGERPRINT}"
        packetEncoding = f"Packet encoding: {PACKET_ENCODING}"
        server_info = f"{title}\n\n{protocol}\n{ip}\n{server_type}\n{security}\n{alpn}\n{fp}\n{packetEncoding}"
        return server_info
