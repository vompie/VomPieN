from TeleVompy.Interface.window import Window

from settings import BOT_NAME, MAX_CLIENT_KEYS, MAX_ADMINS_KEYS
from database.sql import get_user, get_user_left_join_keys, get_user_left_join_keys_by_user_id

from add_client import add_client
from delete_client import delete_client
from update_client import update_client_by_key_id


class NewKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🔑'
        self.Page.Content.title = 'Новый ключ'
        self.Action.action_type = "click"
        self.relayed_payload.dad = 'Keys'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # new key for user/admin button
        if self.relayed_payload.Us:
            user_keys = await get_user_left_join_keys_by_user_id(id=self.relayed_payload.Us)
        # new key for self
        else:
            user_keys = await get_user_left_join_keys(tlg_id=self.User.chat_id)

        # check user
        if not user_keys or not len(user_keys) or user_keys[0]['is_banned']:
            return
        
        # max generate keys
        max_keys = MAX_CLIENT_KEYS
        if user_keys[0]['is_banned']:
            max_keys = -1
        elif self.self_profile['user_lvl'] == 1:
            max_keys = MAX_ADMINS_KEYS
        elif self.self_profile['user_lvl'] > 1:
            max_keys = 99
        if len(user_keys) >= max_keys:
            return
        
        # add new key
        await add_client(tlg_id=user_keys[0]['tlg_id'])


class DeleteKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🗑'
        self.Page.Content.title = 'Удалить'
        self.Action.action_type = "click"

    async def constructor(self) -> None:
        # delete key
        delete_result = await delete_client(id=self.relayed_payload.Ks)
        if not delete_result:
            return
        self.relayed_payload.del_attr('Ks')


class GetKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🎫'
        self.Page.Content.title = 'Получить'
        self.Action.action_type = "send"

    async def constructor(self) -> None:
        self.Page.Content.title = f'Ключ доступа к {BOT_NAME} 🧛🏻'
        self.Page.Content.text = 'Текст'
        self.Page.add_button(model='BYes')


class EnableKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🌕'
        self.Page.Content.title = 'Включить'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return
        
        # update key
        await update_client_by_key_id(id=self.relayed_payload.Ks, enabled=True)


class DisableKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🌑'
        self.Page.Content.title = 'Выключить'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return

        # update key
        await update_client_by_key_id(id=self.relayed_payload.Ks, enabled=False)
