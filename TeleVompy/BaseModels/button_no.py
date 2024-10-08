from ..Interface.window import Window


class BNah(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.Content.title = "Не" 
        self.Page.smile = "💩"
        self.Page.answer = "nah_button_block"
        self.Action.set_action(ActionType=self.Action.types.DELETE)
