from settings import home_dir

class Cfg:
    """ Configuration settings for the application """

    class CfgPage:
        """ Page-related configuration settings """
        BLOCKED: bool = False  # Flag indicating whether the page is blocked
        ANSWER: str = '' # Text to answer on callback for block button
        ALERT: str = '' # Text to alert on callback button for user
        STATE: bool = True  # Flag indicating the state of the page
        SMILE: str = '👍🏻'  # Smile representing a positive action
        SMILE_NEGATIVE: str = '👎🏻'  # Smile representing a negative action
        SMILE_BLOCKED: str = '✖️'  # Smile representing a blocked action (#for_example: 🚫)
        SMILE_POINTER: str = '👉🏻' # Smile representing a pointer
        EMOJI_NUMBERS: list[str] = ['0️⃣', '1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']  # List of emoji numbers
        EFFECT: str = ''  # Effect applied to sending a message

    class CfgContent:
        """ Content-related configuration settings """
        PARSE_MODE: str = 'HTML'  # Parsing mode for the content
        USE_TEMP: bool = True # Should use templates for message titles and texts
        USE_EMOJI_NUMBERS_IN_TITLE: bool = False # Should use EMOJI_NUMBERS for message titles
        TITLE: str = "<b>{title}</b>"  # Template for the title of a message
        TEXT: str = "\n{text}"  # Template for the text of a message

    class CfgAction:
        """ Window-related configuration settings """
        DEFAULT_ACTION: str = 'edit'  # Default action type

    class CfgMedia:
        """ Media-related configuration settings """
        PHOTO_PATH: str = f'{home_dir}assets/photo'  # Path to the directory containing photo files
        VIDEO_PATH: str = f'{home_dir}assets/video'  # Path to the directory containing video files
        AUDIO_PATH: str = f'{home_dir}assets/audio'  # Path to the directory containing audio files
        DOCUMENT_PATH: str = f'{home_dir}assets/document'  # Path to the directory containing document files
        TEXT_LENGTH: int = 4096  # Maximum length of text content
        TEXT_LENGTH_MEDIA: int = 1024  # Maximum length of text with media content

    class CfgPagination:
        """ Message-related configuration settings """
        OFFSET: int = 5  # Offset value for pagination
        
    class CfgEng:
        """ Configuration settings for the engine of the application """
        MODELS_PATH: str = f'{home_dir}models'  # Path to the directory containing the models files
        IGNORE_MODELS_DIRS: list = []  # Dirs to ignoring
        IGNORE_MODELS_FILES: list = []  # Files to ignoring
        DEBUG: bool = True  # Flag indicating whether the engine is in debug mode
