from abc import ABC

class Model(ABC):
    """
    Defined here interface for model types 
    """
    def __init__(self, **kwargs):
        """
        Init generic model

        Parameters:
            kwargs: it's a dict that will contain data model from controller obj
        """
        self.__dict__.update(kwargs)

