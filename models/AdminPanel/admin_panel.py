from TeleVompy.Interface.window import Window

from database.sql import get_user


class AdminPanel(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🦇'
        self.Page.Content.title = 'Администрирование'

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        # check admin mode
        if not self.self_profile or self.self_profile['user_lvl'] < 1:
            return self.Action.set_action(ActionType=self.Action.types.REDIRECT, redirect_to='MM')
        
        self.Page.add_button(model='UsersAdmins', row=0)
        self.Page.add_button(model='Traffic', row=0)
        self.Page.add_button(model='UsersAdmins', row=1, smile='🧙🏻', title='Администраторы', callback=self.CallBack.copy(dad=self.name, payload=self.relayed_payload.set_attrs({'Adm': True})))
        self.Page.add_button(model='Keys', row=1, callback=self.CallBack.copy(dad=self.name, payload=self.relayed_payload.set_attrs({'Bt': 'AdminPanel'})))
        self.Page.add_button(model='BBck', row=2, title='В меню', callback=self.CallBack.create(dad='MM'))

        # check super admin mode
        if self.self_profile['user_lvl'] > 1:
            self.Page.add_button(model='Others', row=2)
