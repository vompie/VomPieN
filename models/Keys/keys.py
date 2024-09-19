from TeleVompy.Interface.window import Window
from database.sql import get_user_keys, get_user, get_user_by_id, update_client_by_id
from add_client import add_client
from delete_client import del_client
from settings import MAX_CLIENT_KEYS


class Keys(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🗝'
        self.Page.Content.title = 'Ключи доступа'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # from users/admins
        if self.relayed_payload.Us:
            user = await get_user_by_id(id=self.relayed_payload.Us)
            keys = await get_user_keys(tlg_id=user['tlg_id'], enabled=None)
            username = f"@{user['username']}" if user['username'] else user['tlg_id']
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

        # new key button
        is_block = keys and len(keys) >= MAX_CLIENT_KEYS and self.self_profile['is_admin'] < 1
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

    def content_setter(self, item: dict) -> tuple[str, str]:
        header = item['uuid'] # + email.user
        footer = f"Создан: {item['created_at']}"
        return header, footer

    def id_getter(self, item: dict) -> None:
        return item['id']


class DeleteKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🗑'
        self.Page.Content.title = 'Удалить'
        self.Action.action_type = "click"

    async def constructor(self) -> None:
        await del_client(id=self.relayed_payload.Ks)
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
        await update_client_by_id(id=self.relayed_payload.Ks, columns=['is_enabled'], values=[1])

class DisableKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🌑'
        self.Page.Content.title = 'Выключить'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        await update_client_by_id(id=self.relayed_payload.Ks, columns=['is_enabled'], values=[0])
