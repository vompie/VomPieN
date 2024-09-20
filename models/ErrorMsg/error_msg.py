from TeleVompy.Interface.window import Window


class ErrorMsg(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🙁'
        self.Page.Content.title = f'🙁 Ошибка'
        self.Page.Content.text = 'Пумпумпум... Что-то пошло не так. Попробуй позже'

    async def constructor(self) -> None:
        self.Page.add_button(model='BNah', row=0)
        self.Page.add_button(model='BYes', row=0)
