from TeleVompy.Interface.window import Window


class NewAdmin(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🦇'
        self.Page.Content.title = 'Добавить администратора'

    async def constructor(self) -> None:        
        self.Page.add_button(model='BBck', row=3, title='В меню', callback=self.CallBack.create(dad='AdminPanel'))
    