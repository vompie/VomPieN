class TeleVompySettings:
    """ Configuration settings for the application """
    def __init__(self, settings: dict):
        """ Bot-related configuration settings """
        self.__set_attr(settings)

    def __set_attr(self, kwargs: dict | None) -> None:
        """ Set the attributes of the object """
        for attr in kwargs or {}:
            if hasattr(self, attr):
                setattr(self, attr, kwargs[attr])


class MessageEffectSettings(TeleVompySettings):
    """ Effect-related configuration settings """
    FIRE: str = "5104841245755180586" # 🔥
    LIKE: str = "5107584321108051014" # 👍
    DISLIKE: str = "5104858069142078462" # 👎
    HEART: str = "5159385139981059251" # ❤️
    PETARD: str = "5046509860389126442" # 🎉
    POO: str = "5046589136895476101" # 💩

class PageSettings(TeleVompySettings):
    """ Page-related configuration settings """
    SMILE: str = '👍🏻'  # Smile representing a positive action
    SMILE_NEGATIVE: str = '👎🏻'  # Smile representing a negative action
    SMILE_BLOCKED: str = '✖️'  # Smile representing a blocked action (#for_example: 🚫)
    SMILE_POINTER: str = '👉🏻' # Smile representing a pointer
    EMOJI_NUMBERS: list[str] = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']  # List of emoji numbers

    ANSWER: str = 'The button is currently blocked' # Text to answer on callback for block button
    ALERT: str = '' # Text to alert on callback button for user
    SHOW_LINK_PREVIEW: bool = False # Show link preview in the message
    BLOCKED: bool = False  # Flag indicating whether the page is blocked
    STATE: bool = True  # Flag indicating the state of the page
    EFFECT: str = ''  # Effect applied to sending a message

class ContentSettings(TeleVompySettings):
    """ Content-related configuration settings """
    PARSE_MODE: str = 'HTML'  # Parsing mode for the content

    USE_TEMP: bool = True # Should use templates for message titles and texts
    USE_EMOJI_NUMBERS_IN_TITLE: bool = False # Should use EMOJI_NUMBERS for message titles
    TITLE_TEMP: str = "<b>{title}</b>"  # Template for the title of a message
    TEXT_TEMP: str = "\n{text}"  # Template for the text of a message

class PaginationSettings(TeleVompySettings):
    """ Message-related configuration settings """
    OFFSET: int = 5  # Offset value for pagination

class MediaSettings(TeleVompySettings):
    TEXT_LENGTH: int = 4096  # Maximum length of text content
    TEXT_LENGTH_MEDIA: int = 1024  # Maximum length of text with media content
    PHOTO_PATH: str = 'photo'  # Path to the directory containing photo files
    VIDEO_PATH: str = 'video'  # Path to the directory containing video files
    AUDIO_PATH: str = 'audio'  # Path to the directory containing audio files
    DOCUMENT_PATH: str = 'document'  # Path to the directory containing document files

class ActionSettings(TeleVompySettings):
    """ Window-related configuration settings """
    DEFAULT_ACTION: str = ''  # Default action type
    
class EngineSettings(TeleVompySettings):
    """ Configuration settings for the engine of the application """
    IGNORE_MODELS_DIRS: list = []  # Dirs to ignoring
    IGNORE_MODELS_FILES: list = []  # Files to ignoring
    DEBUG: bool = False  # Flag indicating whether the engine is in debug mode
