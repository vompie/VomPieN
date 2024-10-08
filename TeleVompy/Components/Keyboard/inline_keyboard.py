from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from ...Utils.base_class import BaseClass, dprint
from uuid import uuid4

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..Page.page import Page


class InlineKeyBoard(BaseClass):
    """
    A class to create an inline keyboard for Telegram bot using aiogram library

    Attributes
    ----------
    - keyboard(`self`) -> `InlineKeyboardMarkup`: Getter for the keyboard attribute

    Methods
    -------
    * __init__(`self`, buttons: `list[dict]]` | `None` = `None`): Constructor to initialize the keyboard
    * __make_keyboard(`self`, buttons: `list[dict]]`) -> `None`: Private method to create the keyboard
    * __cut_payload_data(`self`, payload_data: `str`) -> `str`: Private method to cut the payload data
    """
        
    def __init__(self, buttons: list[dict] | None = None):
        """
        Initialize the keyboard

        Parameters
        ----------
        - buttons (`list[dict]`): A list of dictionaries representing the buttons
            Each dictionary should have the following keys: '`page`', '`name`', '`row`', '`payload`' and '`kwargs`'.
            The rest of the data is taken from the `kwargs` (if transmitted) or from the `page` by default
        """

        super().__init__()
        self.__keyboard: InlineKeyboardMarkup | None = None
        if isinstance(buttons, list) and buttons:
            self.__make_keyboard(buttons)
    
    @property
    def keyboard(self) -> InlineKeyboardMarkup:
        """
        Getter for the keyboard attribute

        Returns
        -------
        `InlineKeyboardMarkup`: The generated inline keyboard
        """
        return self.__keyboard

    def __make_keyboard(self, buttons: list[dict]) -> None:
        """
        Private method to create the keyboard

        Parameters
        ----------
        - buttons (`list[dict]`): A `list` of `dictionaries` representing the buttons.
            Each dictionary should have the following keys: '`page`', '`name`', '`row`', '`payload`' and '`kwargs`'.
            The rest of the data is taken from the `kwargs` (if transmitted) or from the `page` by default

        Raises
        ------
        Exception: If an error occurs during the keyboard creation process
        """

        cheat: str = f"{str(uuid4())[:3]};" # generating a random string and substituting into the first inline button so that the message can always be edited
        rows: dict[list] = {} # rows of buttons in order
        try:
            for button in buttons: 
                # defining the button string
                row: int = button['row']
                if row not in rows: 
                    rows[row] = []

                # properties
                page: Page = button['page']
                payload: str = button['payload']
                kwargs: dict = button['kwargs']
                block: bool = kwargs.get('block', page.block)
                state: bool = kwargs.get('state', page.state)

                # forming a callback and text
                callback_data = f"{page.model_name};{cheat}{payload}" # forming a callback from: the model name;cheat(if exist);payload
                text = f"{kwargs.get('smile', page.smile)} "
                if block: # if the window is blocked (unavailable)
                    text = f"{kwargs.get('smile_block', page.smile_block)} "
                    callback_data = f"#{kwargs.get('answer', page.answer)[:55]};{str(uuid4())[:5]}"
                elif not state: # if the window is in the False state
                    text = f"{kwargs.get('smile_negative', page.smile_negative)} "                   
                text += f"{kwargs.get('title', page.Content.title)}"
                cheat = ''

                # check callback data lenght
                if len(callback_data) > 64:
                    dprint(self, f"created callback data keyboard error: {len(callback_data)} > 64 bytes!\n{callback_data}")
                    callback_data = self.__cut_payload_data(payload_data=payload)

                # append inlinebutton
                rows[row].append(InlineKeyboardButton(text=text, callback_data=callback_data))

            # sort rows and setup keyboard
            sorted_rows = dict(sorted(rows.items()))
            self.__keyboard = InlineKeyboardMarkup(inline_keyboard=sorted_rows.values())
        except Exception as e:
            dprint(self, f"make_keyboard error: {e}")

    def __cut_payload_data(self, payload_data: str) -> str:
        """ Cut payload data """
        # so... now it's just replace payload
        return f"{uuid4()}"
