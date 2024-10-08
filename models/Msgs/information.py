from TeleVompy.Interface.window import Window


class Info(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = self.Page.smile
        self.Page.Content.title = 'Обновление конфигурации сервера'

    async def constructor(self) -> None:
        self.Page.add_button(model='BYes')
        