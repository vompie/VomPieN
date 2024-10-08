from ..messenger import Messenger, Message
from .delete_by_id import DeleteById
from ..Send import Send


class DeleteAndSend(Messenger):
    def __init__(self, msg_id: int | None = None, *args, **kwargs):
        """ 
        Delete message by ID and send the new text message to the chat
        
        Parameters
        ----------
        - msg_id (`int | None`): A 'msg_id' of the message to delete. If `None` -> message won't delete
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """

        super().__init__(*args, **kwargs)
        self.__msg_id = msg_id

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window """
        if self.__msg_id:
            await DeleteById(user=self.User, page=self.Page, msg_id=self.__msg_id).execute()
        return await Send(user=self.User, page=self.Page, **self.kwargs).execute()
