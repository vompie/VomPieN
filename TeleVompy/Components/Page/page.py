from ...Engine.base_class import BaseClass
from ...Engine.model import Model

from ..Keyboard.inline_keyboard import InlineKeyBoard, InlineKeyboardMarkup
from ..Content.content import Content, Media
from ..Callback.callback import Callback, Payload
from ..Pagination.pagination import Pagination
from ..Alert.alert import Alert


class Page(BaseClass):
    """ A class representing a page in the Telegram bot """

    def __init__(self, relayed_payload: Payload, model_name: str = '', *args, **kwargs):
        """ Initialize a new Page object """
        super().__init__()
        self.buttons: list[dict] = [] # a list of dictionaries representing the buttons for the keyboard
        # instances
        self.__model_name: str = model_name # the name of using model
        self.__relayed_payload: Payload = relayed_payload # a relayed payload
        self.__Content: Content = Content(*args, **kwargs) # a instance of Content object
        self.__CallBack: Callback = Callback(model_name=self.__model_name) # a Callback object
        self.__Pagination: Pagination = Pagination(relayed_payload=self.__relayed_payload, page=self) # a instance of Pagination object
        self.__Alert: Alert = Alert(*args, **kwargs) # alert object on callback button to user
        # parameters
        self.smile: str = self.CfgPage.SMILE # smile representing a positive action
        self.smile_negative: str = self.CfgPage.SMILE_NEGATIVE # smile representing a negative action
        self.smile_block: str = self.CfgPage.SMILE_BLOCKED # smile representing a blocked action
        self.effect: str = self.CfgPage.EFFECT # message sending effect
        self.show_link_preview: bool = self.CfgPage.SHOW_LINK_PREVIEW # link preview in the message
        self.state: bool = self.CfgPage.STATE # flag indicating the state of the window
        self.block: bool = self.CfgPage.BLOCKED # flag indicating whether the window is blocked
        self.answer: str = self.CfgPage.ANSWER # text to answer on callback for block button
        self.__set_attr(**kwargs) # setting kwargs attributes

    def __set_attr(self, **kwargs) -> None:
        """ Set the attributes of the object """
        for attr in kwargs:
            if hasattr(self, attr):
                setattr(self, attr, kwargs[attr])

    @property
    def model_name(self) -> str:
        """ Returns the name of the model used in the page """
        return self.__model_name

    @property
    def relayed_payload(self) -> Payload:
        """ Returns the relayed Payload object """
        return self.__relayed_payload

    @property
    def Content(self) -> Content:
        """ Getter for the content object of the page """
        return self.__Content

    @property
    def CallBack(self) -> Callback:
        """ Getter for the callback object of the page """
        return self.__CallBack

    @property
    def Pagination(self) -> Pagination:
        """ Returns the Pagination object """
        return self.__Pagination

    @property
    def Alert(self) -> Alert:
        """ Returns the Alert object """
        return self.__Alert

    @property
    def Media(self) -> Media:
        """ Getter for the media object of the page """
        return self.__Content.Media

    @property
    def keyboard(self) -> InlineKeyboardMarkup | None:
        """
        Getter for the keyboard for the page

        Returns
        -------
        `InlineKeyboardMarkup` | `None`: The keyboard for the page or None if no buttons are available
        """
        return InlineKeyBoard(self.buttons).keyboard if self.buttons else None

    def add_button(self, model: str, row: int | None = 0, callback: Callback | None = None, block: bool | None = None, **kwargs) -> None:
        """  Adds a button to the page """
        if self.__model_name and isinstance(model, str) and (model in Model().models): 
            callback = self.__CallBack.create() if not callback else callback
            payload_string = callback.payload.string()
            kwargs['block'] = block
            window: Page = Model().models[model]().Page
            self.buttons.append(window.__get(row, payload_string, **kwargs))
            
    def __get(self, row: int | None = 0, payload_string: str | None = '', **kwargs) -> dict:
        """ Get base inforamtion about the page """
        window = {
            'page': self,
            'name': self.__model_name,
            'row': row,
            'payload': payload_string,
            'kwargs': kwargs,
        }
        return window
