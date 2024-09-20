from TeleVompy.Interface.window import Window

from database.sql import get_user
from settings import BOT_NAME


class Others(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🎃'
        self.Page.Content.title = 'Прочее'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return
        
        self.Page.add_button(model='InviteAdmin', row=0, title='Пригласить администратора')
        self.Page.add_button(model='BBck', row=1, callback=self.CallBack.create(dad='AdminPanel'))
        # self.Page.add_button(model='BBck', row=2, title='Поиск пользователя', callback=self.CallBack.create(dad='MM'))


class InviteAdmin(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '⚰️'
        self.Page.Content.title = f'Приглашение стать администратором в {BOT_NAME} 🧛🏻'
        self.Action.action_type = "send"

    async def constructor(self) -> None:
        from bot_service.utils import new_deeplink
        deeplink = await new_deeplink(tlg_id=self.User.chat_id, type='new_admin')
        self.Page.Content.text = 'Пумпумпум... ошибочка вышла'
        if deeplink:
            self.Page.Content.text = deeplink
        self.Page.add_button(model='BYes')
