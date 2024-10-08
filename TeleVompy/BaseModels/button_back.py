from ..Interface.window import Window


class BBck(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.Content.title = "Назад" 
        self.Page.smile = "↩️"
        self.Page.answer = "back_button_block"
        self.Action.set_action(ActionType=self.Action.types.CLICK)
