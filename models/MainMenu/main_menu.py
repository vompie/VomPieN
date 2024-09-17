from TeleVompy.Interface.window import Window
from settings import bot_name


class MM(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🌐'
        self.Page.Content.title = bot_name
        self.Page.Content.text = 'Ознакомиться с....'

    async def constructor(self) -> None:
        self.Page.add_button(model='Advantage', row=0)
        self.Page.add_button(model='HowTo', row=0)
        self.Page.add_button(model='GetKey', row=1)
        self.Page.add_button(model='Profile', row=1)
        self.Page.add_button(model='AdminPanel', row=3)
    