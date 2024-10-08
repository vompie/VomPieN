from ..messenger import Messenger, Message


class Alert(Messenger):
    def __init__(self, text: str | None = None, show_alert: bool = False, url: str | None = None, *args, **kwargs):
        """ 
        Send the alert to the chat
        
        Parameters
        ----------
        - text (`str | None`): The text of the alert. If `None`, the default text from the config page will be used
        - show_alert (`bool`): If False, a notification will be shown instead of an alert. Default is False
        - url (`str | None`): The URL that will be opened. Default is None
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the `aiogram.Bot` object!
        """
        
        super().__init__(*args, **kwargs)
        self.__text = text if text else self.CfgPage.ALERT
        self.__show_alert = show_alert
        self.__url = url

    @Messenger.messenger_execute
    async def execute(self) -> 'Message | bool':
        """ Executes all the Window object code, but does not send it """
        return await self.User.query.answer(text=self.__text, show_alert=self.__show_alert, url=self.__url, **self.kwargs)
