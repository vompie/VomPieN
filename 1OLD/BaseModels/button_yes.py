from TeleVompy.Interface.window import Window


class BYes(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.Content.title = "Ок" 
        self.Page.smile = "✔️"
        self.Page.answer = "yes_button_block"
        self.Action.action_type = "delete"
