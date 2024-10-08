import os, sys
from json import loads
from .settings import MessageEffectSettings, PageSettings, ContentSettings, ActionSettings, MediaSettings, PaginationSettings, EngineSettings


class BaseClass:
    """ 
    A base class that inherits from ConfigEngine, ConfigWindow, ConfigPage, ConfigMessage and ConfigTemplate
    Used to reference configs and override basic methods (e.g. print)

    Methods
    -------
    * __init__(`self`) -> `None`: Initializes the `BaseClass`. Calls the super class's `__init__` method
    * __get_paths(`cls`) -> `None`: Get the path of project, base models, user models, TeleVompy directory and settings.json file
    * __read_settings(`cls`) -> `dict`: Read and parse the specified settings file
    * __setup_settings(`cls`) -> `None`: Setup the settings using the parsed settings data
    * __str__(`self`) -> `str`: Returns a string representation of the BaseClass instance. The string format is: "`ClassName` ->"

    Attributes
    ----------
    - __project_dir (`str`): The project directory
    - __televompy_dir (`str`): The directory of TeleVompy
    - __base_models_dir (`str`): The directory of BaseModels
    - __user_models_dir (`str`): The directory of UserModels
    """

    __is_setup_settings: bool = False
    
    def __init__(self):
        """ Initializes the BaseClass. Calls the super class's `__init__` method """
        super().__init__()
        if not BaseClass.__is_setup_settings:
            BaseClass.__get_paths()
            BaseClass.__setup_settings()    
            BaseClass.__is_setup_settings = True

    @classmethod
    def __get_paths(cls) -> None:
        """ Get the path of project, base models, user models, and TeleVompy directory """
        # Project dir
        cls.__project_dir = os.getcwd()
        if sys.platform == "win32":
            cls.__project_dir = cls.__project_dir[0].lower() + cls.__project_dir[1:]
        # TeleVompy dir
        cls.__televompy_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # BaseModels dir
        cls.__base_models_dir = os.path.join(cls.__televompy_dir, 'BaseModels')
        # UserModels dir
        cls.__user_models_dir = os.path.join(os.path.dirname(cls.__televompy_dir), 'models')
        # Settings file
        cls.__settings_file = os.path.join(os.path.dirname(cls.__televompy_dir), 'televompy.json')
        # Assets dir
        cls.__assets_dir = os.path.join(os.path.dirname(cls.__televompy_dir), 'assets')

    @classmethod
    def __read_settings(cls) -> dict:
        """ Read and parse the specified settings file """
        try:
            with open(cls.__settings_file, 'r', encoding="utf_8_sig") as f:
                return loads(f.read())
        except Exception as e:
            print(f'"BaseClass" -> Error reading settings file: {e}')
            return {}

    @classmethod
    def __setup_settings(cls) -> None:
        """ Setup settings for TeleVompy """
        settings = cls.__read_settings()
        cls.CfgMessageEffect = MessageEffectSettings(settings={})
        cls.CfgPage = PageSettings(settings=settings.get('Page', None))
        cls.CfgContent = ContentSettings(settings=settings.get('Content', None))
        cls.CfgPagination = PaginationSettings(settings=settings.get('Pagination', None))
        cls.CfgAction = ActionSettings(settings=settings.get('Action', None))
        cls.CfgMedia = MediaSettings(settings=settings.get('Media', None))
        cls.CfgEngine = EngineSettings(settings=settings.get('Engine', None))
        
    @property
    def project_dir(self) -> str:
        """ Returns the project directory path """
        return self.__project_dir
    
    @property
    def televompy_dir(self) -> str:
        """ Returns the TeleVompy directory path """
        return self.__televompy_dir

    @property
    def base_models_dir(self) -> str:
        """ Returns the base models directory path """
        return self.__base_models_dir

    @property
    def user_models_dir(self) -> str:
        """ Returns the user models directory path """
        return self.__user_models_dir 
    
    @property
    def assets_dir(self) -> str:
        """ Returns the assets directory path """
        return self.__assets_dir

    def __str__(self) -> str:
        """ Returns a string representation of the BaseClass instance. The string format is: "`ClassName` ->" """
        return f'"{type(self).__name__}" ->'


def dprint(self: object | str | None = None, *values: object, **kwargs) -> None:
    """
    Debug print function. If CfgEng.DEBUG flag is True, print the provided values

    Parameters
    ----------
    - self (`object` | `str` | `None`): The object or object name to print
    - *values: `object`: Values to print
    - **kwargs: `str` -> `object`: Keyword arguments to print
    """

    if not BaseClass().CfgEngine.DEBUG:
        return
    
    self = f'"{self}" ->' if isinstance(self, str) else self
    values = (self, *values) if self else values
    print(*values, **kwargs)
