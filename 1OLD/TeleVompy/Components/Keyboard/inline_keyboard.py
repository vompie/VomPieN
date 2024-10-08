from ...Engine.base_class import BaseClass
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from uuid import uuid4
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from ..Page.page import Page


class InlineKeyBoard(BaseClass):
    """
    A class to create an inline keyboard for Telegram bot using aiogram library

    Attributes
    ----------
    __keyboard (`InlineKeyboardMarkup`): The generated inline keyboard

    Methods
    -------
    __init__(`self`, buttons: `list[dict]]` | `None` = `None`): Constructor to initialize the keyboard

    __make_keyboard(`self`, buttons: `list[dict]]`) -> `None`: Private method to create the keyboard

    __cut_payload_data(`self`, payload_data: `str`) -> `str`: Private method to cut the payload data

    keyboard(`self`) -> `InlineKeyboardMarkup`: Getter for the keyboard attribute
    """
        
    def __init__(self, buttons: list[dict] | None = None):
        """
        Initialize the keyboard

        Parameters
        ----------
        buttons (`list[dict]`): A list of dictionaries representing the buttons

        Each dictionary should have the following keys: '`page`', '`name`', '`row`', '`payload`' and '`kwargs`'
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
        buttons (`list[dict]`): A `list` of `dictionaries` representing the buttons.
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
                name: str = button['name']
                payload: str = button['payload']
                kwargs: dict = button['kwargs']
                title: str = kwargs.get('title', page.Content.title)
                block: bool = kwargs.get('block', page.block)
                answer: str = kwargs.get('answer', page.answer)[:50]
                smile_block: str = kwargs.get('smile_block', page.smile_block)
                state: bool = kwargs.get('state', page.state)
                smile_negative: str = kwargs.get('smile_negative', page.smile_negative)
                smile: str = kwargs.get('smile', page.smile)
                
                # forming a callback and text
                callback_data = f"{name};{cheat}{payload}" # forming a callback from: the model name;cheat(if exist);payload
                text = f"{smile} "
                if block: # if the window is blocked (unavailable)
                    text = f"{smile_block} "
                    callback_data = f"#{answer};{str(uuid4())[:10]}"
                elif not state: # if the window is in the False state
                    text = f"{smile_negative} "                   
                text += f"{title}"
                cheat = ''

                # check callback_data lenght
                if len(callback_data) > 64: # TODO: CHANGE TO PAYLOAD LEN
                    if self.CfgEng.DEBUG: print(f"{self} created callback data keyboard error: {len(callback_data)} > 64 bytes!\n{callback_data}")
                    callback_data = self.__cut_payload_data(paylaod_data=payload)

                rows[row].append(InlineKeyboardButton(text=text, callback_data=callback_data))
            sorted_rows = dict(sorted(rows.items()))
            self.__keyboard = InlineKeyboardMarkup(inline_keyboard=sorted_rows.values())
        except Exception as e:
            if self.CfgEng.DEBUG: print(f"{self} -> make_keyboard error: {e}")

    def __cut_payload_data(self, paylaod_data: str) -> str:
        """ Cut payload data """
        # TODO: rewrite, now it's just replace payload
        return f"{uuid4()}"
