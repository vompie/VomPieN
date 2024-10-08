from ...Utils.base_class import BaseClass
from .payload import Payload


class Callback(BaseClass):
    """ A class representing a callback in the Telegram bot """

    def __init__(self, model_name: str = ''):
        """ Initialize a new Callback object """
        super().__init__()
        self.__name = model_name
    
    @property
    def name(self) -> str:
        """ Returns the name of using model """
        return self.__name

    @property
    def payload(self) -> Payload:
        """ Returns the payload data """
        return self.__payload

    @payload.setter
    def payload(self, payload: Payload) -> None:
        """ Sets the payload data """
        self.__payload = payload

    def create(self, payload: str | None = None, dad: str | None = None) -> 'Callback':
        """ 
        Creates a new callback 
        
        Parameters
        ----------
        - payload (`str` | `None`): Payload data
        - dad (`str` | `None`): Parent name of using model
        
        Returns
        -------
        `Callback`: The Callback object
        """

        callback = Callback(model_name=self.__name)
        callback.__payload = Payload(payload).get()
        callback.__set_base_data(dad=dad)
        return callback

    def copy(self, payload: Payload, dad: str | None = None, **kwargs) -> 'Callback':
        """
        Creates a copy of the callback 
        
        Parameters
        ----------
        - payload (`Payload`): Payload object
        - dad (`str` | `None`): Parent name of using model
        
        Returns
        -------
        `Callback`: The Callback object
        """
        
        callback = Callback(model_name=self.__name)
        callback.__payload = payload.copy(dad=dad, items=kwargs)
        return callback

    def __set_base_data(self, dad: str | None) -> None:
        """ Sets the base data of callback """
        base_data = {
            'dad': dad if dad else self.__name,
        }
        self.__payload.set_attrs(items=base_data)
