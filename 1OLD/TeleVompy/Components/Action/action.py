from ...Engine.messenger import Messenger
from ...Engine.model import Model

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ...Interface.window import Window, User, Page, Payload


class Action(Messenger):    
    def __init__(self, user: 'User', page: 'Page', *args, **kwargs):
        """
        Initialize Action class with User and Page instances

        Parameters
        ----------
        - User (`User`): User object
        - page (`Page`): Page object
        """
        
        super().__init__(user=user, page=page)
        self.__User: User = user # a instance of User object
        self.__Models: Model = Model().models # a instance of Model object
        self.__relayed_payload: Payload = page.relayed_payload # relayed payload
        self.action_type: str = self.CfgAction.DEFAULT_ACTION # messenger action for window
        self.redirect_to: str = '' # name of model to redirecting
        self.__set_attr(**kwargs) # setting kwargs attributes

    def __set_attr(self, **kwargs) -> None:
        """ Set the attributes of the object """
        for attr in kwargs:
            if hasattr(self, attr):
                setattr(self, attr, kwargs[attr])
    
    def get_action(self) -> callable:
        """ Returns the action function based on the action type """
        action = getattr(self, self.action_type, None)
        return action if callable(action) else False

    async def send(self) -> None:
        return await super().send()

    async def edit(self) -> None:
        return await super().edit()

    async def delete(self) -> None:
        return await super().delete()
    
    async def invoice(self) -> None:
        return await super().invoice()
    
    async def nothing(self) -> None:
        """ Executes all the Window object code, but does not send it """
        if self.CfgEng.DEBUG: print(f"{self} 'ok, I'm sending nothing, are you happy?'")
        return await super().nothing()

    async def alert(self) -> None:
        return await super().alert()        

    async def click(self) -> None:
        self.__User.payload = f"{self.__relayed_payload.dad};{self.__relayed_payload.string()}"
        window: Window = self.__Models[self.__relayed_payload.dad](user=self.__User)
        await window.action()

    async def redirect(self) -> None:
        if not self.redirect_to:
            # if empty redirect then redirect to self -> just rebuild the window 
            self.redirect_to = self.__relayed_payload.dad 
        self.__User.payload = f"{self.__relayed_payload.dad};{self.__relayed_payload.string()}"
        window: Window = self.__Models[self.redirect_to](user=self.__User)
        await window.action()

    async def toggle(self) -> None:
        window: Window = self.__Models[self.__relayed_payload.dad](user=self.__User)
        await window.action()
