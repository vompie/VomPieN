from ..Interface.window import Window


class BNxt(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.Content.title = "" 
        self.Page.smile = "➡️"
        self.Page.answer = "next_button_block"
        self.Action.set_action(ActionType=self.Action.types.CLICK)

    async def constructor(self) -> None:
        self.relayed_payload_set_attrs(items={'pg': self.relayed_payload.pg + 1})
