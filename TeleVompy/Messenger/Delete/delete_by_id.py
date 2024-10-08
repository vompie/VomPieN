from ..messenger import Messenger, Message


class DeleteById(Messenger):
    def __init__(self, msg_id: int, *args, **kwargs):
        """ 
        Delete the message from the chat by it's ID
        
        Parameters
        ----------
        - msg_id (`int`): A 'msg_id' of the message to delete
        """

        super().__init__(*args, **kwargs)
        self.__msg_id = msg_id

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window """
        return await self.bot.delete_message(chat_id=self.User.chat_id, message_id=self.__msg_id)  
