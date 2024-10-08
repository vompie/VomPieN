from ..messenger import Messenger, Message


class Redirect(Messenger):
    def __init__(self, redirect_to: str | None = None, *args, **kwargs):
        """ 
        Redirect to another Page
        
        Parameters
        ----------
        - redirect_to (`str | None`): Name of Page to redirect. If empty then redirect to self (just rebuild the window)
        """

        super().__init__(*args, **kwargs)
        self.__redirect_to = redirect_to if redirect_to else self.relayed_payload.dad

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ Executes all the Window object code, but does not send it """
        self.User.payload = f"{self.relayed_payload.dad};{self.relayed_payload.string()}"
        return await self.Models[self.__redirect_to](user=self.User).action()
