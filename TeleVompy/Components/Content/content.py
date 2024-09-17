from ...Engine.base_class import BaseClass
from .parse_mode_html import ParseModeHTML
from ..Media.media import Media


class Content(BaseClass):
    """ A class representing a Content for Page """

    def __init__(self, *args, **kwargs):
        """ Initialize a Content instance """
        super().__init__()
        self.__content: str = '' # the content (title + text) of the page
        self._title: str= '' # title of the page
        self._text: str = '' # text of the page
        self.use_temp_for_text: bool = self.CfgContent.USE_TEMP # flag indicating use a template for the title and text
        self.html: ParseModeHTML = ParseModeHTML # object to formating text in HTML markdown
        self.parse_mode: str = self.CfgContent.PARSE_MODE # text parse mode
        self.offset: int = self.CfgPagination.OFFSET # offset for pagination on page
        self.__Media: Media = Media(content=self.content, parse_mode=self.parse_mode) # media object
        self.__set_attr(**kwargs) # setting kwargs attributes

    def __set_attr(self, **kwargs) -> None:
        """ Set the attributes of the object """
        for attr in kwargs:
            if hasattr(self, attr):
                setattr(self, attr, kwargs[attr])

    @property
    def Media(self) -> Media:
        """ Getter for the media of the content """
        return self.__Media

    @property
    def content(self) -> str:
        """ Getter for the compiled content of the content """
        return self.__content

    @property
    def title(self) -> str:
        """ Getter for the title of the content """
        return self._title

    @title.setter
    def title(self, txt: str) -> None:
        """ Setter for the title of the content """
        self._title = txt
        self.__set_content()

    @property
    def text(self) -> str:
        """ Getter for the text of the content """
        return self._text
    
    @text.setter
    def text(self, txt: str) -> None:
        """ Setter for the text of the content """
        self._text = txt
        self.__set_content()

    def __set_content(self) -> None:
        """ Clear the content and set it with the current title and text """    
        self.__content = ""
        title = self.CfgContent.TITLE if self.use_temp_for_text else '{title}'
        text = self.CfgContent.TEXT if self.use_temp_for_text else '{text}'
        if self._title:
            self.__content += f"{title.format(title=self._title)}\n"
        if self._text:
            self.__content += f"{text.format(text=self._text)}"
        self.__cut_text()
        self.__Media.update_content(content=self.__content)

    def __cut_text(self) -> None:
        """ Cut message to fit in the text length limit with some media or without it """
        if self.__Media.has_files():
            if len(self.__content) > self.CfgMedia.TEXT_LENGTH_MEDIA:
                self.__content = f"{self.__content[:self.CfgMedia.TEXT_LENGTH_MEDIA-5]}..."
                if self.CfgEng.DEBUG: print(self, "cut_text -> because message with media was too long")    
        elif len(self.__content) > self.CfgMedia.TEXT_LENGTH:
            self.__content = f"{self.__content[:self.CfgMedia.TEXT_LENGTH-5]}..."
            if self.CfgEng.DEBUG: print(self, "cut_text -> because message was too long")

    def set_content_item(self, number: int, is_select: bool = False, header: str = '', footer: str = '') -> None:
        """
        Concatenation number, header and footer

        Parameters
        ----------
        - number (`int`): The number of the item
        - is_select (`bool` | `None`): Flag indicating whether to select the item. Default is False
        - header (`str` | `None`): Header text for the item. Default is an empty string
        - footer (`str` | `None`): Footer text for the item. Default is an empty string
        """

        header: ParseModeHTML = self.html(header, husk=False)
        content = ''
        # make pointer
        if is_select:
            header = header.bold()
            content = self.CfgPage.SMILE_POINTER if self.CfgContent.USE_EMOJI_NUMBERS_IN_TITLE else f"{self.CfgPage.SMILE_POINTER} "
        else:
            header = header.text
        # make header
        if self.CfgContent.USE_EMOJI_NUMBERS_IN_TITLE:
            content += f"{self.CfgPage.EMOJI_NUMBERS[number]}: {header}\n"
        else:
            number = self.html(number, husk=False).bold() 
            content += f"{number}. {header}\n"
        # make footer
        if footer:
            content += f"{footer}\n"
        # update text
        self.text += f"{content}\n"
