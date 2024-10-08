from ..Utils.base_class import BaseClass, dprint

import os
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
    * __init__(`self`) -> `None`: Initializes the Model clas
    * __get_models(`self`) -> `None`: Load model classes from the models subdirectories
    * __read_directory(`self`) -> `None`: Recursively walk through the specified directory and load model classes from the.py files found
    * __load_classes_from_file(`self`, filepath: str) -> None: Loads model classes from a given Python source code file
    * models(`self`) -> `dict`: Returns the loaded model classes
    """

    __instance: 'Model' = None
    __models: dict = {}

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Model, cls).__new__(cls)
            cls.__instance.__get_models()
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

    def __read_directory(self, directory: str) -> None:
        """ Recursively walk through the specified directory and load model classes from the.py files found """
        for root, _, files in os.walk(directory):
            dir_name = os.path.basename(root)
            # Use only directories starting with a capital letter and not being ignored
            if not dir_name[0].isupper() or dir_name in self.CfgEngine.IGNORE_MODELS_DIRS:
                continue
            for filename in files:
                # Use only files ending with .py
                if not filename.endswith(".py") or filename in self.CfgEngine.IGNORE_MODELS_FILES:
                    continue
                # Get the full path of the file and load the model classes from it
                filepath = os.path.join(root, filename)
                # Loads model classes from a given Python source code file
                self.__load_classes_from_file(filepath)

    def __load_classes_from_file(self, filepath: str) -> None:
        """
        Loads model classes from a given Python source code file
        
        Parameters
        ----------
        - filepath (`str`): The full path of the Python source code file
        """

        try:
            # Parse the Python source code file and get the names of the defined classes
            with open(filepath, 'r', encoding="utf_8_sig") as f:
                tree = parse(f.read())
            # Get the names of the defined classes in the file
            classes = [node.name for node in tree.body if isinstance(node, ClassDef)]
            # If the file defines any model classes, load them and add them to the dictionary
            for class_name in classes:
                # Get the module path of the class and load it                
                module_path = filepath.replace(self.project_dir + os.path.sep, '')
                module_name = module_path.replace('.py', '').replace(os.path.sep, '.')
                module = import_module(module_name)
                # If model with same class name already exist
                if class_name in self.__models:
                    dprint(self, f"a model with the same name '{class_name}' has already been added. It will be replaced by model from file: {filepath}")
                # Add class name and module to models dictionary
                self.__models[class_name] = getattr(module, class_name)
        except Exception as e:
            dprint(self, f"get model moduls from file {filepath} error: {e}")

    def __get_models(self) -> None:
        """ Load model classes from the models subdirectories """
        # Read BaseModels directory at first
        self.__read_directory(self.base_models_dir)
        # Read UserModels directory
        self.__read_directory(self.user_models_dir)    
