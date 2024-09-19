from TeleVompy.Interface.window import Window
from settings import BOT_NAME
from database.sql import get_user


class MM(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🌐'
        self.Page.Content.title = BOT_NAME
        self.Page.Content.text = 'Ознакомиться с....'

    async def constructor(self) -> None:
        self.Page.add_button(model='Advantage', row=0, title="Почему мы?")
        self.Page.add_button(model='HowTo', row=0)
        self.Page.add_button(model='Keys', row=1)
        self.Page.add_button(model='Profile', row=1)
        # check admin mode
        self.self_profile = await get_user(tlg_id=self.User.chat_id)
        if self.self_profile and self.self_profile['is_admin'] > 0:
            self.Page.add_button(model='AdminPanel', row=2)
    