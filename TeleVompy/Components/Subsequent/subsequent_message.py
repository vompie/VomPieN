from ...Utils.base_class import BaseClass
from ...Engine.model import Model

from ..Page.page import Page

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ...Interface.window import Window, User


class SubsequentMessage(BaseClass):
    def __init__(self, user: 'User', is_subsequent: bool = False):
        """
        Initialize SubsequentMessage class with User and Page instances
        
        Parameters
        ----------  
        - user (`User`): User object
        - is_subsequent (`bool`): Whether the window is a subsequent window or not
        """

        super().__init__()
        self.__User: User = user
        self.__Models: Model = Model().models
        self.__is_subsequent: bool = is_subsequent
        self.__subsequent_messages: dict = {}
    
    @property
    def is_subsequent(self) -> bool:
        """ Returns True if the window is a subsequent window, False otherwise """
        return self.__is_subsequent

    @property
    def subsequent_messages(self) -> dict:
        """ Returns the subsequent messages dict """
        return self.__subsequent_messages

    def add(self, page: 'Page', position: int | None = None, **kwargs) -> None:
        """ Adds a subsequent message contains Page to the subsequent messages dict """

        # if parent message is subsequent -> cant send another subsequent message
        if self.__is_subsequent or not isinstance(page, Page):
            return
        
        # setup message
        kwargs['is_subsequent'] = True
        subsequent = {
            'page': page,
            'kwargs': kwargs
        }
        
        # set order to send the message
        if not position and not (keys:=self.__subsequent_messages.keys()):
            position = 1
        elif not position:
            position = max(keys) + 1
        # add message
        self.__subsequent_messages[position] = subsequent

    async def action(self) -> None:
        """ Use action of subsequent messages """
        # sort subsequent messages
        subsequent_messages = dict(sorted(self.__subsequent_messages.items())) if len(self.__subsequent_messages) > 1 else self.__subsequent_messages
        
        # process subsequent messages 
        for subseq in subsequent_messages.values():
            # if parent message is subsequent -> cant send another subsequent message
            if self.__is_subsequent or not self.__User or not isinstance(subseq['page'], Page):
                continue
            
            # get window for current subsequent message and send
            page: Page = subseq['page']
            if page.model_name not in self.__Models:
                continue
            window: Window = self.__Models[page.model_name](user=self.__User.copy(), page=page, **subseq['kwargs'])
            await window.action()
