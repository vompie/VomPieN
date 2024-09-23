from TeleVompy.Interface.window import Window

from database.sql import get_user
from settings import BOT_NAME, BOT_SMILE
from xray_service.utils import reboot_server


class Others(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🎃'
        self.Page.Content.title = 'Прочее'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 2:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return
        
        self.Page.add_button(model='InviteAdmin', row=0, title='Администратор')
        self.Page.add_button(model='InviteUser', row=0, title='Пользователь')
        self.Page.add_button(model='InviteByKey', row=1, title='Вступительный ключ')
        self.Page.add_button(model='RebootSrv', row=1)
        self.Page.add_button(model='BBck', row=2, callback=self.CallBack.create(dad='AdminPanel'))
        # self.Page.add_button(model='BBck', row=2, title='Поиск пользователя')


class InviteAdmin(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '💌'
        self.Page.Content.title = f'Приглашение стать администратором в {BOT_NAME} {BOT_SMILE}'
        self.Action.action_type = "send"

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        
        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 2:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return

        from bot_service.utils import new_deeplink
        deeplink = await new_deeplink(tlg_id=self.User.chat_id, type='new_admin')
        self.Page.Content.text = 'Пумпумпум... ошибочка вышла'
        if deeplink:
            self.Page.Content.text = deeplink
        self.Page.add_button(model='BYes')


class InviteUser(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '📧'
        self.Page.Content.title = f'Приглашение в {BOT_NAME} {BOT_SMILE}'
        self.Action.action_type = "send"

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        
        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 2:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return


        from bot_service.utils import new_deeplink
        deeplink = await new_deeplink(tlg_id=self.User.chat_id, type='new_user')
        self.Page.Content.text = 'Пумпумпум... ошибочка вышла'
        if deeplink:
            self.Page.Content.text = deeplink
        self.Page.add_button(model='BYes')


class InviteByKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '✉️'
        self.Page.Content.title = f'Получить новый ключ'
        self.Action.action_type = "send"

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        
        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 2:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return

        from bot_service.utils import new_deeplink
        deeplink = await new_deeplink(tlg_id=self.User.chat_id, type='new_key')
        self.Page.Content.text = 'Пумпумпум... ошибочка вышла'
        if deeplink:
            self.Page.Content.text = deeplink
        self.Page.add_button(model='BYes')


class RebootSrv(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🔄'
        self.Page.Content.title = f'Перезагрузить сервер'
        self.Action.action_type = "toggle"

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 2:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return

        reboot_result = await reboot_server()

        # send error message
        if not reboot_result:
            from bot_service.utils import send_msg
            await send_msg(message_query=self.User.query, model='ErrorMsg', text='Не удалось перезагрузить сервер', action_type='send')
