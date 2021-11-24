from inspect import ismethod
from typing import TypeVar

from FractionalCascadingExceptions import MissingComparisonMethodsException

# Generic for data and locations
# -> Represents any data. Just a label for consistency, no rules to enforce.
D = TypeVar('D')
# -> Represents a given location. Instances of L must be comparable.
L = TypeVar('L')

# def method_exists(class_instance:object, method_name:str) -> bool:
#         return hasattr(class_instance, method_name) and \
#             ismethod(getattr(class_instance, method_name))
            

# def check_existing_methods(class_instance:object, method_names:list[str],
#                            raise_exception:bool=False) -> bool:
#     missing_methods = []
#     all_good = True
    
#     for m in method_names:
#         if not ismethod(class_instance, m):
#             all_good = False
#             if not raise_exception:
#                 return False
#             else:
#                 missing_methods.append(m)
                
#     if not all_good and raise_exception:
#         MissingComparisonMethodsException(missing_methods)
        
# def check_for_comparison_meths(class_instance:object, only_equality:bool=False,
#                                raise_exception:bool=True) -> bool:
#     comp_meths = ["__eq__", "__ne__", "__gt__", "__lt__", "__ge__", "__le__"]
#     eq_meths = ["__eq__", "__ne__"]
#     return check_existing_methods(class_instance, 
#                                   comp_meths if only_equality else eq_meths,
#                                   raise_exception)
