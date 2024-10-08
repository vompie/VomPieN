from TeleVompy.Interface.window import Window


class BSlc(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.Content.title = "" 
        self.Page.smile = "👌🏻"
        self.Page.answer = "select_button_block"
        self.Action.action_type = "click"
