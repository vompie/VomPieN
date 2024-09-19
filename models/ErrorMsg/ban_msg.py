from TeleVompy.Interface.window import Window


class BanMsg(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🥲'
        self.Page.Content.title = f'Твой аккаунт заблокирован'

    async def constructor(self) -> None:
        self.Page.add_button(model='BYes', row=0, smile='🥲')
