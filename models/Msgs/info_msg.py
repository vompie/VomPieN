from TeleVompy.Interface.window import Window


class InfoMsg(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '📩'
        self.Action.action_type = 'send'

    async def constructor(self) -> None:
        self.Page.add_button(model='BYes', row=0, smile='📨')
