from TeleVompy.Interface.window import Window


class AdminPanel(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '🦇'
        self.Page.Content.title = 'Администрирование'

    async def constructor(self) -> None:
        self.Page.add_button(model='Users', row=0)
        self.Page.add_button(model='Traffic', row=0)

        self.Page.add_button(model='Keys', row=1)
        # self.Page.add_button(model='Keys', row=1)

        self.Page.add_button(model='Admins', row=1)
        # self.Page.add_button(model='NewAdmin', row=2)
        
        self.Page.add_button(model='BBck', row=3, title='В меню', callback=self.CallBack.create(dad='MM'))
        self.Page.add_button(model='BBck', row=3, title='Поиск пользователя', callback=self.CallBack.create(dad='MM'))
    