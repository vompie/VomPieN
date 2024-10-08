from ..messenger import Messenger, Message


class Click(Messenger):
    def __init__(self, *args, **kwargs):
        """ 
        Make Click on the Page
            When Clicked, the Payload will change. 
            The `dad` parameter will specify the current Window, and it will be completely updated and rebuilt.
            This is convenient when you need to stay within the Window, but with global changes to this Window
        
        Parameters
        ----------
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """

        super().__init__(*args, **kwargs)

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ Executes all the Window object code, but does not send it """
        self.User.payload = f"{self.relayed_payload.dad};{self.relayed_payload.string()}"
        return await self.Models[self.relayed_payload.dad](user=self.User).action()
