from TeleVompy.Interface.window import Window
from database.sql import get_user_keys, get_user, get_user_by_id, get_user_keys_by_id
from add_client import add_client
from delete_client import del_client
from settings import MAX_CLIENT_KEYS


class UAKeys(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🗝'
        self.Page.Content.title = 'Ключи доступа'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # from users/admins
        if self.relayed_payload.Us:
            user = await get_user_by_id(id=self.relayed_payload.Us)
            # all keys
            keys = await get_user_keys(tlg_id=user['tlg_id'], enabled=None)
        # from main menu
        else:
            user = False
            # enabled keys
            keys = await get_user_keys(tlg_id=self.User.chat_id, enabled=True)

        # back button
        self.Page.add_button(model='BBck', row=2, callback=self.CallBack.copy(dad='Profile', payload=self.relayed_payload))

        # new key button
        is_block = keys and len(keys) >= MAX_CLIENT_KEYS and self.self_profile['is_admin'] < 1
        self.Page.add_button(model='GetKey', row=2, callback=self.CallBack.copy(payload=self.relayed_payload), block=is_block, answer='cant_create_key') 
        
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
        # delete button
        self.Page.add_button(model='DeleteKey', row=1, callback=callback, block=(not self.relayed_payload.sl), answer='key_not_select')

    def content_setter(self, item: dict) -> tuple[str, str]:
        header = item['uuid']
        footer = f"Создан: {item['created_at']}"
        return header, footer

    def id_getter(self, item: dict) -> None:
        return item['id']




# class EnableKey(Window):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.Page.smile = '🌕'
#         self.Page.Content.title = 'Включить'
#         self.Action.action_type = "toggle"

#     async def constructor(self) -> None:
#         await update_client_by_id(id=self.relayed_payload.Ks, columns=['is_enabled'], values=[1])
#         self.relayed_payload.dad = 'Keys'


# class DisableKey(Window):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.Page.smile = '🌑'
#         self.Page.Content.title = 'Выключить'
#         self.Action.action_type = "toggle"

#     async def constructor(self) -> None:
#         await update_client_by_id(id=self.relayed_payload.Ks, columns=['is_enabled'], values=[0])
#         self.relayed_payload.dad = 'Keys'