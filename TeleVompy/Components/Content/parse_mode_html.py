class ParseModeHTML:
    """
    A class to handle HTML formatting for Telegram messages

    Attributes
    ----------
    text (`str` | `int` ): The text to be formatted

    Methods
    -------
    * husk(text: `str`) -> `str`: Replaces HTML special characters with their corresponding HTML entities
    * empty_text(text: `str`) -> `callable` | `str`: Return empty str or callable function
    * italic() -> `str`: Returns the text formatted as italic
    * bold() -> `str`: Returns the text formatted as bold
    * underline() -> `str`: Returns the text formatted as underlined
    * span() -> `str`: Returns the text wrapped in a span tag with class 'tg-spoiler'
    * code() -> `str`: Returns the text wrapped in a code tag
    * pre() -> `str`: Returns the text wrapped in a pre tag
    * pre_code(language: `str` | `None` = 'python') -> `str`: Returns the text wrapped in a pre and code tag with the specified language
    * strike() -> `str`: Returns the text formatted as strikethrough
    * link(url: `str`) -> `str`: Returns the text wrapped in an a tag with the specified URL
    * mention(user_id: `int`) -> `str`: Returns the text wrapped in an a tag with a Telegram user mention URL
    * quote() -> `str`: Returns the text wrapped in a blockquote tag
    * quote_exp() -> `str`: Returns the text wrapped in a blockquote tag with the 'expandable' attribute
    """
            
    def __init__(self, text: str | int, husk: bool = True):
        """ Initializes the ParseModeHTML object with the provided text and husk flag """
        if not isinstance(text, str):
            text = str(text)
        self.text = self.husk(text=text) if husk else text

    @staticmethod
    def husk(text: str) -> str:
        """ Used to replace unsupported characters with code """
        text = text.replace('<', '&lt;')
        text = text.replace('>', '&gt;')
        text = text.replace('&', '&amp;')
        text = text.replace('"', '&quot;')
        return text

    @staticmethod
    def empty_text(func) -> 'callable | str':
        def wrapper(self: 'ParseModeHTML', *args, **kwargs):
            return "" if not self.text else func(self, *args, **kwargs)
        return wrapper

    @empty_text
    def italic(self) -> str:
        """ Returns the text formatted as italic """
        return f"<i>{self.text}</i>"
    
    @empty_text
    def bold(self) -> str:
        """ Returns the text formatted as bold """
        return f"<b>{self.text}</b>"

    @empty_text
    def underline(self) -> str:
        """ Returns the text formatted as underlined """
        return f"<u>{self.text}</u>"

    @empty_text
    def span(self) -> str:
        """ Returns the text wrapped in a span tag with class 'tg-spoiler' """
        return f"<span class='tg-spoiler'>{self.text}</span>"

    @empty_text
    def code(self) -> str:
        """ Returns the text wrapped in a code tag """
        return f"<code>{self.text}</code>"

    @empty_text
    def pre(self) -> str:
        """ Returns the text wrapped in a pre tag """
        return f"<pre>{self.text}</pre>"
    
    @empty_text
    def pre_code(self, language: str | None = 'python') -> str:
        """ Returns the text wrapped in a pre and code tag with the specified language """
        return f"<pre><code class='language-{language}'>{self.text}</code></pre>"

    @empty_text
    def strike(self) -> str:
        """ Returns the text formatted as strikethrough """
        return f"<s>{self.text}</s>"

    @empty_text
    def link(self, url: str) -> str:
        """ Returns the text wrapped in an a tag with the specified URL """
        return f"<a href='{url}'>{self.text}</a>"

    @empty_text
    def mention(self, username: str) -> str:
        """ Returns the text wrapped in an a tag with a Telegram user mention URL """
        return f"<a href='https://t.me/{username}'>@{self.text}</a>"

    @empty_text
    def quote(self) -> str:
        """ Returns the text wrapped in a blockquote tag """
        return f"<blockquote>{self.text}</blockquote>"

    @empty_text
    def quote_exp(self) -> str:
        """ Returns the text wrapped in a blockquote tag with the 'expandable' attribute """
        return f"<blockquote expandable>{self.text}</blockquote>"
