from TeleVompy.Interface.window import Window

from settings import BOT_NAME, BOT_SMILE, MAX_CLIENT_KEYS, MAX_ADMINS_KEYS
from settings import TEMPLATE_KEY
from database.sql import get_user, get_user_left_join_keys, get_user_left_join_keys_by_user_id, get_user_by_key_id, get_client

from add_client import add_client
from delete_client import delete_client
from update_client import update_client_by_key_id


class NewKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🔑'
        self.Page.Content.title = 'Новый ключ'
        self.Action.action_type = "click"
        self.relayed_payload.dad = kwargs.get('dad', 'Keys')

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # new key for user/admin button
        if self.relayed_payload.Bt == 'UsersAdmins':
            user_keys = await get_user_left_join_keys_by_user_id(id=self.relayed_payload.Us)
        # new key for keys button
        if self.relayed_payload.Bt == 'AdminPanel':
            user = await get_user_by_key_id(id=self.relayed_payload.Ks)
            user_keys = await get_user_left_join_keys(tlg_id=user['tlg_id'])
        # new key for self
        else:
            user_keys = await get_user_left_join_keys(tlg_id=self.User.chat_id)

        if self.relayed_payload.Bt == 'AdminPanel':
            self.relayed_payload.dad = 'Profile'

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

        # if limit
        if len(user_keys) >= max_keys:
            return
        
        # add new key
        add_client_result = await add_client(tlg_id=user_keys[0]['tlg_id'])
        if not add_client_result:
            return

        # send information message
        if self.relayed_payload.Bt:
            from bot_service.utils import send_msg
            await send_msg(chat_id=user_keys[0]['tlg_id'], model='InfoMsg', title='Получен новый ключ', text='Администраторы подарили тебе ключ')


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
        self.Page.Content.title = f'Ключ к {BOT_NAME} {BOT_SMILE}'

        # get key
        key = await get_client(id=self.relayed_payload.Ks)
        if not key['is_enabled']:
            return
        
        # get uri for key
        key_uri = TEMPLATE_KEY.replace('UUID_KEY_HERE', key['uuid'])
        self.Page.Content.text = self.Page.Content.html(key_uri).code()
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
