from TeleVompy.Interface.window import Window


class BPrv(Window):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Page.Content.title = "" 
        self.Page.smile = "⬅️"
        self.Page.answer = "prev_button_block"
        self.Action.action_type = "click"

    async def constructor(self) -> None:
        self.relayed_payload_set_attrs(items={'pg': self.relayed_payload.pg - 1})
