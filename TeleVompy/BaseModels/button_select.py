from ..Interface.window import Window


class BSlc(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.Content.title = "" 
        self.Page.smile = "👌🏻"
        self.Page.answer = "select_button_block"
        self.Action.set_action(ActionType=self.Action.types.CLICK)
