from typing import TypeVar

# Generic for data and locations
# -> Represents any data. Just a label for consistency, no rules to enforce.
D = TypeVar('D')
# -> Represents a given location. Instances of L must be comparable.
L = TypeVar('L')







# COMPARISON_METHOD_NAMES = \
#     {"__eq__", "__ne__", "__gt__", "__lt__", "__ge__", "__le__"}

# def method_exists(class_instance:object, method_name:str) -> bool:
#     return callable(getattr(class_instance, method_name, False))

# def check_existing_methods(class_instance:object, method_names:Iterable[str],
#                            raise_exception:bool=False) -> bool:
#     missing_methods = []
#     all_good = True
    
#     for m in method_names:
#         if not hasattr(class_instance, m):
#             all_good = False
#             if not raise_exception:
#                 return False
#             else:
#                 missing_methods.append(m)
                
#     if not all_good and raise_exception:
#         MissingComparisonMethodsException(missing_methods)
    
#     return all_good
        
# def check_for_comparison_meths(class_instance:object, only_equality:bool=False,
#                                raise_exception:bool=True) -> bool:
#     eq_meths = ["__eq__", "__ne__"]
#     return check_existing_methods(class_instance, 
#                                   COMPARISON_METHOD_NAMES if only_equality else eq_meths,
#                                   raise_exception)


# class B:
#     def __init__(self) -> None:
#         self.x = 5
        
#     # def __eq__(self, __o: object) -> bool:
#     #     return self.x == __o.x
    
#     # def __ne__(self, __o: object) -> bool:
#     #     return self._x != __o.x

# if __name__ == "__main__":
#     c = check_existing_methods(B(), ["__eq__", "__ne__", "__lt__"])
#     if c:
#         print("DOPE")
#     else:
#         print("NOPE")