from ...Engine.base_class import BaseClass


class Alert(BaseClass):
    """ A class representing a Alert """

    def __init__(self, *args, **kwargs):
        """ Initialize a new Alert object """
        super().__init__()
        self.text = self.CfgPage.ALERT # text of the alert
        self.show_alert: bool | None = None # if False notification will be shown instead of a alert
        self.url: str | None = None # url that will be opened
        self.__set_attr(**kwargs) # setting kwargs attributes

    def __set_attr(self, **kwargs) -> None:
        """ Set the attributes of the object """
        for attr in kwargs:
            if hasattr(self, attr):
                setattr(self, attr, kwargs[attr])
