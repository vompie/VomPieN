from TeleVompy.Interface.window import Window


class Traffic(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '📈'
        self.Page.Content.title = 'Траффик'

    async def constructor(self) -> None:        
        self.Page.add_button(model='BBck', row=0, callback=self.CallBack.create(dad='AdminPanel'))
    