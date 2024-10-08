from ..Engine.base_class import BaseClass

from ..Components.Page.page import Page, Pagination
from ..Components.Callback.callback import Callback, Payload
from ..Components.Action.action import Action
from ..Components.Subsequent.subsequent_message import SubsequentMessage

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..Engine.user import User


class Window(BaseClass):
    def __init__(self, user: 'User | None' = None, page: Page | None = None, *args, **kwargs):
        """
        Initialize Window class with User and Page instances
        
        Parameters
        ----------
        - user (`User` | `None`): User instance for sending messages
        - page (`Page` | `None`): Page instance for content of sending messages
        - *args (`Any`): Additional positional arguments for Page initialization
        - **kwargs (`Any`): Additional keyword arguments for Page initialization
        """

        super().__init__()
        self.__name: str = type(self).__name__
        self.__User: User | None = user
        __payload: str = self.__User.payload if self.__User else ''
        self.__relayed_payload: Payload = Payload(data=__payload).get()
        self.__Page: Page = self.create_page(model_name=self.__name, relayed_payload=self.__relayed_payload, *args, **kwargs) if not page else page
        self.__Action: Action = Action(user=self.__User, page=self.__Page, *args, **kwargs)
        self.__SubsequentMessage: SubsequentMessage = SubsequentMessage(user=self.__User, is_subsequent=kwargs.get('is_subsequent', False))


    """
    The basic method for changing window initialization and utilization
    -------------------------------------------------------------------
        * You need to implement your own window initialization and utilization logic
    """

    async def constructor(self) -> None:
        """ Implement your window initialization logic here """

    async def destructor(self) -> None:
        """ Implement your window destruction logic here """


    """
    Model name and Page
    -------------------
    """

    @property
    def name(self) -> str:
        """ Returns the name of using model """
        return self.__name

    @property
    def Page(self) -> Page:
        """ Returns the Page instance containing the message content and settings """
        return self.__Page

    def create_page(self, model_name: str, relayed_payload: Payload | None = None, *args, **kwargs) -> 'Page':
        """ Creates a new Page instance """
        if not relayed_payload:
            relayed_payload = self.__relayed_payload
        return Page(relayed_payload=relayed_payload, model_name=model_name, *args, **kwargs)


    """
    User object
    -----------
    """

    @property
    def User(self) -> 'User':
        """ Returns the User instance containing the chat_id, msg_id and from_user """
        return self.__User


    """
    Relayed Payload
    ---------------
    """

    @property
    def relayed_payload(self) -> Payload:
        """ Returns the relayed Payload object """
        return self.__relayed_payload

    def relayed_payload_set_attrs(self, items: dict) -> 'Window':
        """ Sets attributes to the relayed payload """
        self.__relayed_payload.set_attrs(items=items)
        return self
    
    def relayed_payload_del_attr(self, attr: str) -> 'Window':
        """ Deletes an attribute from the relayed payload """
        self.__relayed_payload.del_attr(attr=attr)
        return self

    def relayed_payload_recreate(self, items: dict | None = None) -> 'Window':
        """ Recreates the relayed payload """
        self.__relayed_payload.del_all().set_attrs(items=items)
        return self


    """
    CallBack and Pagination
    -----------------------
    """

    @property
    def CallBack(self) -> Callback:
        """ Returns the CallBack object """
        return self.__Page.CallBack

    @property
    def Pagination(self) -> Pagination:
        """ Returns the Pagination object """
        return self.__Page.Pagination


    """
    Subsequent messages 
    -------------------
    """

    @property
    def SubsequentMessage(self) -> SubsequentMessage:
        """ Returns the SubsequentMessage object """
        return self.__SubsequentMessage


    """
    Window-Action methods
    ---------------------
    """

    @property
    def Action(self) -> Action:
        """ Returns the Action object """
        return self.__Action

    async def action(self) -> 'Window':
        """ Performs the action of the window """
        await self.constructor()
        if not (action:=self.Action.get_action()):
            return
        await action()
        await self.__SubsequentMessage.action()
        await self.destructor()
        return self
