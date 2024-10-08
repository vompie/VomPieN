from ...Utils.base_class import BaseClass
from .action_types import ActionTypes

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ....TeleVompy import User
    from ....TeleVompy.Components import Page


class Action(BaseClass):
    def __init__(self, user: 'User', page: 'Page'):
        """
        Initialize Action class with User and Page instances

        Parameters
        ----------
        - user (`User`): User object
        - page (`Page`): Page object
        - kwargs (`Any`): Only for parameters that EXIST in the called methods of the Bot object!
        """

        super().__init__()
        self.__User: User = user # a instance of User object
        self.__Page: Page = page # a instance of Page object
        self.__types = ActionTypes # types of an actions
        self.__action: object = None # current action type
        self.set_action(ActionType=self.CfgAction.DEFAULT_ACTION) # set the default action

    @property
    def types(self):
        """ Returns the EnumTypes of an actions """
        return self.__types    

    @property
    def action(self) -> object:
        """ Returns the action object associated with the current action type """
        return self.__action

    def set_action(self, ActionType: object | ActionTypes, *args, **kwargs) -> None:
        """ Set the action type """
        if isinstance(ActionType, str):
            ActionType = self.__types[ActionType]
        if isinstance(ActionType, ActionTypes):
            ActionType = ActionType.value
        self.__action = ActionType(user=self.__User, page=self.__Page, *args, **kwargs)  

    def get_action_type(self) -> str:
        """ Returns the action type as a string """
        return self.__action.__class__.__name__
