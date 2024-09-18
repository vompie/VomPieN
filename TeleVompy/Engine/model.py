from .base_class import BaseClass

from os import walk, path
from importlib import import_module
from ast import parse, ClassDef


class Model(BaseClass):
    """
    A class to manage and load models from a specified directory

    Attributes
    ----------
    __models (`dict`): A dictionary containing loaded model classes

    Methods
    -------
    __init__(`self`) -> `None`: Initializes the Model class

    __get_object(`self`) -> `None`: Loads model classes from the subdirectories

    models(`self`) -> `dict`: Returns the loaded model classes
    """

    __instance: 'Model' = None
    __models: dict | None = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Model, cls).__new__(cls)
            cls.__models: dict = cls.__instance.__get_object()
        return cls.__instance

    def __init__(self):
        """ Initializes the Model class and loads model classes from the models subdirectories """
        super().__init__()
        
    @property
    def models(self) -> dict:
        """
        Returns the loaded model classes

        Returns
        -------
        `dict`: A dictionary containing loaded model classes
        """
        return self.__models
    
    def __get_object(self) -> dict:
        """
        Load model classes from the subdirectories
        
        Returns
        -------
        `dict`: A dictionary containing loaded model classes
        """
        
        # Initialize an empty dictionary to store loaded model classes
        models = {}
        # Load model classes from the subdirectories using ast module to parse Python source code
        for root, _, files in walk(self.CfgEng.MODELS_PATH):
            # Use only directories starting with a capital letter and not being ignored
            slash = '\\' if "\\" in root else '/'
            dir = root.split(slash)[-1]
            if not dir[0].isupper() or dir in self.CfgEng.IGNORE_MODELS_DIRS:
                continue
            for filename in files:
                # Use only files ending with .py
                if not filename.endswith(".py") or filename in self.CfgEng.IGNORE_MODELS_FILES:
                    continue
                # Get the full path of the file and load the model classes from it
                filepath = path.join(root, filename)
                try:
                    # Parse the Python source code file and get the names of the defined classes
                    with open(filepath, 'r', encoding="utf_8_sig") as f:
                        tree = parse(f.read())
                    # Get the names of the defined classes in the file
                    classes = [node.name for node in tree.body if isinstance(node, ClassDef)]
                    # If the file defines any model classes, load them and add them to the dictionary
                    for class_name in classes:
                        # Get the full path of the class and load it
                        module = import_module(filepath.split('.')[0].replace(slash, "."))
                        # If model with same class name already exist
                        if class_name in models and self.CfgEng.DEBUG:
                            print(f"{self} a model with the same name '{class_name}' has already been added. It will be replaced by model from file: {filepath}")
                        models[class_name] = getattr(module, class_name)
                except Exception as e:
                    if self.CfgEng.DEBUG: 
                        print(f"{self} get model moduls from file {filepath} error: {e}")
        return models
