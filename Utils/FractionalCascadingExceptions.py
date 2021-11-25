# from Utils.PrettyPrintingUtils import pretty_list

class MissingComparisonMethodsException(Exception):
    
    def __init__(self, missing_methods:list[str]) -> None:
        pr_missing_methods_str = \
            print(missing_methods)
            # pretty_list(missing_methods, opening_brace='', closing_brace='')
            
        super().__init__("In order to use this object when creating a node," + \
            " it must have the following comparison methods implemented:\n" + \
                f"{pr_missing_methods_str}")
        

class InvalidRandUniqueIntGenerationInput(Exception):
    def __init__(self, range_min:int, range_max:int, n:int) -> None:
        super().__init__(
            f"Distance between rangeMin({range_min}) and rangeMax " + \
                f"({range_max}) is less than expected size of output list ({n}).")