from ...Utils.base_class import BaseClass, dprint
from .compression import Compression

from typing import Any
from json import loads, dumps


class Payload(BaseClass):
    """
    A class to handle payload data

    Attributes
    ----------
    - __data (`str`): The callback data for the payload
    - dad (`str`): `parent` page for the `page`
    - pg (`int`): Sequential number of the `page`
    - sl (`Any`): Selected item in list page

    Methods
    -------
    * __init__(`self`, data: `str` = None, *args, **kwargs) -> `None`: Initializes the Payload object - 
    * convention() -> `None`: Provides an abbreviation of each attribute's full name for better readability   - 
    * __getattr__(`self`, name: `str`) -> `Any`: Handles attribute access for undefined attributes    - 
    * set_attrs(`self`, items: `dict` | None = None) -> `Payload`: Sets attributes from a dictionary  - 
    * del_attr(`self`, attr: `str`) -> `Payload`: Deletes an attribute from the payload   - 
    * del_all(`self`) -> `Payload`: Deletes all attributes from the payload   - 
    * copy(`self`, dad: `str` | `None` = '*') -> `Payload`:  Creates a copy of the Payload object - 
    * string(`self`) -> `str`: Returns the payload data as a string   - 
    * get(`self`) -> `Payload`: Retrieves the payload data    - 
    * __get_payload(`self`) -> `None`: Parses the callback data and sets attributes   - 
    * __public_attrs(`self`) -> `dict`: Returns a dictionary of public attributes - 
    * __to_str(data: `dict` | `None` = None) -> `str`: Converts a dictionary to a JSON string and compress data   - 
    * __to_dict(data: `str` | `None` = None) -> `dict`: Converts a JSON string to a dictionary and decompress data
    """

    def __init__(self, data: str = None):
        """ Initializes the Payload object """
        super().__init__()
        self.__special_int_attr: dict = {
            'pg': 0,
        }
        self.__data = data
        self.dad: str 
        self.pg: int
        self.sl: Any        

    @staticmethod
    def convention() -> None:
        """ Provides an abbreviation of each attribute's full name for better readability """
        ABBREVIATION_FULL_NAME = {
            'BBck': 'base class Button Back',
            'BNxt': 'base class Button Next',
            'BPrv': 'base class Button Previous',
            'BSlc': 'base class Button Select',
            'BYes': 'base class Button Yes',
            'BNah': 'base class Button No',
            'dad': '`parent` page for the `page`',
            'pg': 'sequential number of the `page`',
            'sl': 'selected item in list `page`'
        }
        print(ABBREVIATION_FULL_NAME)

    def __str__(self) -> str:
        """ Returns the `Payload` object as a string """
        return dumps(self.__dict__)

    def __getattr__(self, name: str) -> Any:
        """ Handles attribute access for undefined attributes """
        value = self.__special_int_attr.get(name, None)
        self.set_attrs(items={name: value})
        return value

    def set_attrs(self, items: dict | None = None) -> 'Payload':
        """ Sets attributes from a dictionary """
        if not items:
            return self
        for key, value in items.items():
            try:
                setattr(self, key, value)
            except Exception as e:
                dprint(self, f"setting payload attribute error: {e}")
        return self

    def del_attr(self, attr: str) -> 'Payload':
        """ Deletes an attribute from the payload """
        try:
            delattr(self, attr)
        except: 
            pass
        return self

    def del_all(self) -> 'Payload':
        """ Deletes all attributes from the payload """
        for attr in self.__public_attrs():
            self.del_attr(attr=attr)
        self.__data = ""
        return self

    def copy(self, dad: str | None = None, items: dict | None = None) -> 'Payload':
        """ Creates a copy of the Payload object """
        items['dad'] = dad if dad else self.dad
        payload = Payload(f"{items['dad']};{self.string()}").get()
        payload.set_attrs(items=items)
        return payload

    def string(self) -> str:
        """ Returns the payload data as a string """
        return self.__to_str(data=self.__public_attrs())

    def get(self) -> 'Payload':
        """ Retrieves the payload data """
        self.__get_payload()
        return self

    def __get_payload(self) -> None:
        """ Parses the callback data and sets attributes """
        if not self.__data: 
            return
        _, *payload = self.__data.split(";", maxsplit=2)
        if not payload: 
            return
        if len(payload) > 1:
            payload[0] = payload[1]
        attrs = self.__to_dict(payload[0])
        self.set_attrs(attrs)

    def __public_attrs(self) -> dict:
        """ Returns a dictionary of public attributes """
        public_attrs = {key: value for key, value in self.__dict__.items() if not key.startswith('_') and value}
        return public_attrs

    @staticmethod
    def __to_str(data: dict | None = None) -> str:
        """ Converts and Compress dictionary to a JSON string """
        try:
            return Compression(input_data=dumps(data)).compress()
        except Exception as e:
            dprint('Payload', f'to str error: {e}')
            return ''

    @staticmethod
    def __to_dict(data: str | None = None) -> dict:
        """ Converts and Decompress a JSON string to a dictionary """
        try:
            return loads(Compression(input_data=data).decompress())
        except Exception as e:
            dprint('Payload', f'to dict error: {e}')
            return {}
