from TeleVompy.Interface.window import Window
from database.sql import get_user


class Traffic(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '📈'
        self.Page.Content.title = 'Трафик'

    async def constructor(self) -> None:
        # check admin mode
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        if not self.self_profile or self.self_profile['is_admin'] < 1:
            self.Action.action_type = 'redirect'
            self.Action.redirect_to = 'MM'
            return        
        self.Page.add_button(model='BBck', row=0, callback=self.CallBack.create(dad='AdminPanel'))
    