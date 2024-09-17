from TeleVompy.Interface.window import Window


class GetKey(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🔑'
        self.Page.Content.title = 'Получить ключ'
        self.Page.Content.text = 'Неа'

    async def constructor(self) -> None:
        self.Page.add_button(model='BBck', row=0, title='В меню', callback=self.CallBack.create(dad='MM'))
    