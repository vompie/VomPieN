from TeleVompy.Interface.window import Window


class Keys(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🗝'
        self.Page.Content.title = 'Ключи доступа'

    async def constructor(self) -> None:       
        self.Page.add_button(model='BBck', row=3, callback=self.CallBack.create(dad='AdminPanel'))
    