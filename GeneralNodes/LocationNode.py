from typing import Optional

from Utils.TypeUtils import L


class LocationNode:
    """
    Node object representing a single location in a single dimension.
    Fields:
        _loc (L): Object of any orderable type representing the location value.
        _dim (int): An integer representing the dimension value.
        _dim_label (str): A string further representing the dimension for cases
            in which it is indicative of something other than a number. (Only
            used for printing purposes.)    """
            
    def __init__(self, location:L, dimension:int, 
                 dimension_label:Optional[str]=None) -> None:
        """
        Args:
            location (L): Object of any sortable type representing the location
                of this LocationNode.
            dimension (int): Dimension value of this LocationNode.
            dimension_label (Optional[str], optional): String further   
                representing the dimension for cases in which it is indicative
                of something other than a number.   """
        
        # check_for_comparison_meths(location)  # Raise exception if can't compare
        self._loc = location
        self._dim = dimension
        self._dim_label = dimension_label
    
    def loc(self) -> L:
        """
        Returns:
            L: The location value of this LocationNode. """
        return self._loc
    
    def set_loc(self, loc:L) -> None:
        """
        Set a location value loc as the location for this node.
        Args:
            loc (L): A location variable of any orderable type. """
        self._loc = loc
        
    def dim(self) -> int:
        """
        Returns:
            int: Integer representing the dimension in which the location in
                this LocationNode refers.   """
        return self._dim
    
    def dim_str(self) -> str:
        """
        Returns:
            str: _dim_label if the field exists, else the dimension integer of
                the current node as a string.   """
        return self._dim_label if self._dim_label else str(self._dim)
    
    def visualizer_str(self) -> str:
        return f"{self.dim_str()}: {self._loc}"
    
    def __str__(self) -> str:
        return f"Dim: {self.dim_str()}, Loc: {self._loc}"
        
    def __repr__(self) -> str:
        return str(self)
    
    # Comparison method overrides are all in context of _loc field.
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, LocationNode):
            return self._loc == __o.loc()
            
        return False
    
    def __gt__(self, __o: object) -> bool:
        if isinstance(__o, LocationNode):
            return self._loc > __o.loc()
        return False
    
    def __lt__(self, __o: object) -> bool:
        if isinstance(__o, LocationNode):
            return self._loc < __o.loc()
        return False
    
    def __ge__(self, __o: object) -> bool:
        if isinstance(__o, LocationNode):
            return not self.__lt__(__o)
        return False
    
    def __le__(self, __o: object) -> bool:
        if isinstance(__o, LocationNode):
            return not self.__gt__(__o)
        return False