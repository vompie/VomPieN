from ..messenger import Messenger, Message, dprint


class Nothing(Messenger):
    def __init__(self, *args, **kwargs):
        """ 
        Literally does nothing
        
        Parameters
        ----------
        - kwargs (`Any`): Only for parameters that WON'T DO anything!
        """
        super().__init__(*args, **kwargs)

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ Executes all the Window object code, but does not send it """
        dprint(self, f"'ok, i'm sending nothing, are you happy?'")
        return True
