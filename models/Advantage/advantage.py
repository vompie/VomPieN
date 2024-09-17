from TeleVompy.Interface.window import Window


class Advantage(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.smile = '⭐️'
        self.Page.Content.title = 'Почему мы?'
        self.Page.Content.text = 'Их много'

    async def constructor(self) -> None:
        self.Page.add_button(model='BBck', row=0, title='В меню', callback=self.CallBack.create(dad='MM'))
        self.Page.add_button(model='GetKey', row=0)
    