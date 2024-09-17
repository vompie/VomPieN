from TeleVompy.Interface.window import Window


class BBck(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.Content.title = "Назад" 
        self.Page.smile = "↩️"
        self.Page.answer = "back_button_block"
        self.Action.action_type = "click"
