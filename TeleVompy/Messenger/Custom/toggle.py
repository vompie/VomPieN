from ..messenger import Messenger, Message


class Toggle(Messenger):
    def __init__(self, *args, **kwargs):
        """ 
        Make Toggle on the page
            When Toggling with the Payload parameter, no changes occur.
            The Page is simply updated and only internal changes are performed. 
            It is suitable if you need to switch something and it will not affect global Window changes.
        
        Parameters
        ----------
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """
                
        super().__init__(*args, **kwargs)

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ Executes all the Window object code, but does not send it """
        return await self.Models[self.relayed_payload.dad](user=self.User).action()  
