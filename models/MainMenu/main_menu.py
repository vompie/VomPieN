from TeleVompy.Interface.window import Window

from settings import BOT_NAME, BOT_SMILE
from database.sql import get_user


class MM(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🌐'
        self.Page.Content.title = f"{BOT_NAME} — сервис, который не заблокировать"
        self.Page.Content.text = ''

    async def constructor(self) -> None:
        self.self_profile = await get_user(tlg_id=self.User.chat_id)

        self.Page.add_button(model='Advantage', row=0, title="Преимущества")
        self.Page.add_button(model='HowTo', row=0)
        self.Page.add_button(model='Keys', row=1)
        self.Page.add_button(model='Profile', row=1)

        # check admin mode
        if self.self_profile and self.self_profile['user_lvl'] > 0:
            self.Page.add_button(model='AdminPanel', row=2)
    