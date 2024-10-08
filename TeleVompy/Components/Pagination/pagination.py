from ...Utils.base_class import BaseClass

from typing import Any, TYPE_CHECKING
if TYPE_CHECKING:
    from ...Components.Page.page import Page, Content, Callback, Payload


class Pagination(BaseClass):
    def __init__(self, page: 'Page', relayed_payload: 'Payload'):
        """
        Initializes Pagination class with Window, Callback, Page, and RelayedPayload instances

        Parameters
        ----------
        - page (`Page`): Page object
        - relayed_payload (`Payload`): Payload object
        """
        
        super().__init__()
        self.__Page: Page = page
        self.__CallBack: Callback = page.CallBack
        self.__Content: Content = page.Content
        self.__relayed_payload: Payload = relayed_payload
        self.__selected_item: Any | None = None
        self.__var_name: str = ''

    @property
    def selected_item(self) -> Any | None:
        """ Returns the selected item """
        return self.__selected_item
        
    def add(self, dataset: list[object], var_name: str = '', content_setter: callable = None, id_getter: callable = None) -> None:
        """ Adds pagination to the window """
        # variable name of item 
        self.__var_name = var_name
        
        # empty dataset
        if not len(dataset): 
            return

        # setup select
        var_value = self.__relayed_payload.__getattr__(self.__var_name)
        if var_value:
            self.__relayed_payload.sl = var_value
            self.__relayed_payload.del_attr(attr=self.__var_name)

        # content setter and id getter
        self.__content_setter = content_setter if content_setter else self.__content_setter
        self.__id_getter = id_getter if id_getter else self.__id_getter

        # start, end, and slice of dataset
        start = self.__relayed_payload.pg * self.__Content.offset
        end = start + self.__Content.offset if (start + self.__Content.offset) < len(dataset) else len(dataset)
        slice_dataset = dataset[start:end]

        # pagination callback
        pagination_callback = self.__CallBack.copy(payload=self.__relayed_payload, dad=self.__CallBack.name)

        # button previously
        pagination_callback.payload.del_attr('sl')
        self.__Page.add_button('BPrv', row=0, block=(start <= 0), callback=pagination_callback)

        # buttons number
        for number, item in enumerate(slice_dataset, start=1):
            # set .sl
            pagination_callback.payload.set_attrs({'sl': self.__id_getter(item)})
            # if item is select
            is_select = self.__relayed_payload.sl and self.__relayed_payload.sl == pagination_callback.payload.sl
            if is_select:
                self.__selected_item = item
                pagination_callback.payload.del_attr('sl')
            # set content
            header, footer = self.__content_setter(item)
            self.__Content.set_content_item(number=number, is_select=is_select, header=header, footer=footer)
            # button select
            self.__Page.add_button(model='BSlc', row=0, callback=pagination_callback, smile=self.CfgPage.EMOJI_NUMBERS[number])

        # button next
        pagination_callback.payload.del_attr('sl')
        self.__Page.add_button(model='BNxt', row=0, block=(end >= len(dataset)), callback=pagination_callback)

    def get_callback(self) -> 'Callback':
        """ Returns the callback with the selected item set """
        callback = self.__CallBack.copy(payload=self.__relayed_payload, dad=self.__Page.model_name)
        callback.payload.set_attrs({self.__var_name: self.__relayed_payload.sl})
        callback.payload.del_attr(attr='sl')
        return callback

    def multiselect(self, multivalues_attr: str, max_items: int = 0) -> tuple[bool, int, 'Callback'] | tuple[None, int, None]:   
        """
        max_items = 0 means not limit, if you want to set limit to real 0, you shoud be set max_items = -1

        Adds a multiselect button to the window. Returns a `tuple` containing whether the item was selected, count of selected items and the updated callback
        1. If the item is not selected or the multiselect list is full: it will return (`None`, count_selected_items, `None`)
        2. If the item is already selected: it will remove the item from the multiselect list and return (`True`, count_selected_items, updated_callback)
        3. If the item is selected: it will return (`False`, count_selected_items, updated_callback)
        """

        # if item in selected items: True - select, False - not select, None - can't select
        in_items = None 

        # get multivalues items
        multivalues: list | None = getattr(self.__relayed_payload, multivalues_attr)
        multivalues = multivalues.copy() if multivalues else []

        # set count of selected items
        items_selected = len(multivalues)

        # if item is not select OR can't select one more item -> return None, items_selected, None
        if not self.__relayed_payload.sl:
            return in_items, items_selected, None 

        # if item in selected items 
        if self.__relayed_payload.sl in multivalues:
            multivalues.remove(self.__relayed_payload.sl)
            in_items = True
        
        # if item not in selected items and count of selected items < items limit or items limit == 0 (means no limit)
        elif items_selected < max_items or max_items == 0:
            multivalues.append(self.__relayed_payload.sl)
            in_items = False

        # set updated callback
        callback_multiselect = self.__CallBack.copy(payload=self.__relayed_payload, dad=self.__CallBack.name)
        callback_multiselect.payload.set_attrs({multivalues_attr: multivalues})
        return in_items, items_selected, callback_multiselect

    def __content_setter(self, item: object = None) -> tuple[str, str]:
        """
        Returns a tuple containing the header and footer for a given item
            The header should be a string that will be displayed at the top of the item
            The footer should be a string that will be displayed at the bottom of the item
        """
        raise NotImplementedError("Implement your header and footer initialization logic here")
    
    def __id_getter(self, item: object = None) -> int:
        """ Returns an id of an item or None if it's not possible to get an id """
        raise NotImplementedError("Implement your id getter logic here")
