
from typing import Type
from Utils.PrettyPrintingUtils import pretty_list


class MissingComparisonMethodsException(Exception):
    
    def __init__(self, missing_methods:list[str]) -> None:
        pr_missing_methods_str = \
            pretty_list(missing_methods, opening_brace='', closing_brace='')
            
        super().__init__("In order to use this object when creating a node," + \
            " it must have the following comparison methods implemented:\n" + \
                f"{pr_missing_methods_str}")
        

class InvalidRandUniqueIntGenerationInput(Exception):
    def __init__(self, range_min:int, range_max:int, n:int) -> None:
        super().__init__(
            f"Distance between rangeMin({range_min}) and rangeMax " + \
                f"({range_max}) is less than expected size of output list ({n}).")
        
        
class InvalidDimensionalityException(Exception):
    def __init__(self, cur_dim:int, dimensionality:int) -> None:
        super().__init__(f"Invalid dimensionality: {cur_dim} is either " + \
            f"less than 1 or greater than dimensionality ({dimensionality})")
        
        
class MissingFieldException(Exception):
    def __init__(self, class_name:str, field_name:str) -> None:
        super().__init__(
            f"Instance of class {class_name} is missing field: {field_name}.")
        
        
class InvalidTypeException(Exception):
    def __init__(self, given_type:str, expected_type:str, owner:str) -> None:
        super().__init__(f"Object or method {owner} is of type " + \
            f"{given_type} when {expected_type} is expected")
        
        
def raise_if_equal(obj_a:object, obj_b:object, invert:bool=False,
                   exception:Type[Exception]=None, params:tuple=None) -> None:
    """
    Raise an exception when two given objects are equal.

    Args:
        obj_a (object): To be compared with obj_b.
        obj_b (object): To be compared with obj_a.
        invert (bool, optional): Defaults to False. If true, raise exception if
            obj_a does not equal obj_b.
        exception (Type[Exception], optional): Exception type to be raised if
            obj_a equals obj_b. If None, use default Exception.
        params (tuple, optional): Tuple containing parameters to be used when 
            calling exception constructor.

    Raises:
        exception: Given exception, instantiated via values in params.
        Exception: Default exception if None, instantiated via values in params.
    """
    if exception != None and not \
        (isinstance(exception, Exception) or issubclass(exception, Exception)):
            # Ensure that exception is of proper type.
            raise Exception("Invalid exception param. Type must be be a " + \
                "subclass of the Exception class.")
        
    if (obj_a == obj_b and not invert) or \
        (obj_a != obj_b and invert):
        return
    
    raise exception(params) if exception else Exception(params)


def raise_if_none(obj:object, exception:Type[Exception]=None, params:tuple=None, 
                  empty_params:bool=False) -> None:
    """
    Raise an exception when a given object is None.
    
    Args:
        obj (object): To be checked if None.
        exception (Type[Exception], optional): Exception to be raised if obj is
            None. If None, uses default Exception class.
        params (tuple, optional): Tuple containing parameters to be used when 
            calling exception constructor. If None, and empty_params is False,
            defaults to a string message: "Object does not exist.".
        empty_params (bool): If true, and params is None, do not instantiate 
            exception with default messsage.    """
    if not params and not empty_params:
        params = (f"Object does not exist.")
    
    raise_if_equal(obj_a=obj, obj_b=None, exception=exception, params=params)