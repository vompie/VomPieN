from TeleVompy.Interface.window import Window


class UpdCfg(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = self.Page.smile
        self.Page.Content.title = 'Конфигурация сервера обновлена'

    async def constructor(self) -> None:
        self.Page.add_button(model='BYes')
        