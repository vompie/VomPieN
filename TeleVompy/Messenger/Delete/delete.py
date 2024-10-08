from ..messenger import Messenger, Message


class Delete(Messenger):
    def __init__(self, *args, **kwargs):
        """  Delete the message from the chat """
        super().__init__(*args, **kwargs)

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ The function that Window class will call to execute the current window """
        return await self.bot.delete_message(chat_id=self.User.chat_id, message_id=self.User.msg_id)
