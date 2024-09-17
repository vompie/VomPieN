from TeleVompy.config import Cfg


class BaseClass(Cfg):
    """ 
    A base class that inherits from ConfigEngine, ConfigWindow, ConfigPage, ConfigMessage and ConfigTemplate
    Used to reference configs and override basic methods (e.g. print)

    Methods
    -------
    __init__(`self`) -> `None`: Initializes the `BaseClass`. Calls the super class's `__init__` method

    __str__(`self`) -> `str`: Returns a string representation of the BaseClass instance. The string format is: "`ClassName` ->"
    """

    def __init__(self):
        """ Initializes the BaseClass. Calls the super class's `__init__` method """
        super().__init__()

    def __str__(self) -> str:
        """ Returns a string representation of the BaseClass instance. The string format is: "`ClassName` ->" """
        return f'"{type(self).__name__}" ->'
