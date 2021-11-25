from typing import Optional

from Utils.FractionalCascadingUtils import L


class LocationNode:
    
    def __init__(self, location:L, dimension:int, 
                 dimension_label:Optional[str]=None) -> None:
        
        # check_for_comparison_meths(location)  # Raise exception if can't compare
        self._loc = location
        self._dim = dimension
        self._dim_label = dimension_label
    
    def loc(self) -> L:
        return self._loc
    
    def set_loc(self, loc:L) -> None:
        self._loc = loc
        
    def dim(self) -> int:
        return self._dim
    
    def dim_str(self) -> str:
        return self._dim_label if self._dim_label else str(self._dim)
    
    def __str__(self) -> str:
        return f"Dim: {self.dim_str()}, Loc: {self._loc}"
        
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, __o: object) -> bool:
        """
        Checks if two location nodes share the same location. Note that this
        ignores data value.

        Args:
            __o (object): some object for which to check equality.

        Returns:
            bool: True if the location value for this object equals that of __o,
            false otherwise.
        """
        if isinstance(__o, LocationNode):
            return self._loc == __o.loc()
            
        return False
    
    def __ne__(self, __o: object) -> bool:
        if isinstance(__o, LocationNode):
            return not self.__eq__(__o)
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