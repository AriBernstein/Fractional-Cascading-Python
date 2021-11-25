from generalNodes.DataNode import DataNode
from generalNodes.LocationNode import LocationNode
from generalNodes.SingleDimNode import SingleDimNode
from Utils.FractionalCascadingUtils import D
from Utils.PrettyPrintingUtils import pretty_dict
from Utils.FractionalCascadingExceptions import InvalidDimensionalityException

class FullNode:
    
    """
    Fields:
        _data (DataNode): DataNode instance representing this FullNode's data.
        _locations (dict[int, LocationNode]): Dictionary with key -> integer
            representing dimension, pair -> LocationNode representing location
            of _data in given dimension.
        _dimensionality (int): Represents number of location values in which
            this FullNode exists.   """
    
    def __init__(self, data:DataNode, locations:dict[int, LocationNode]) -> None:
        self._data = data
        self._locs = locations
        self._dimensionality = len(locations)
        
    def data(self) -> D:
        return self._data.data()
    
    def dataNode(self) -> DataNode:
        return self._data
    
    def locations(self) -> dict[int, LocationNode]:
        return self._locs
    
    def loc(self, dim:int) -> LocationNode:
        if not 1 <= dim <= self.dimensionality():
            raise InvalidDimensionalityException(dim, self.dimensionality())
        return self._locs[dim]
    
    def dimensionality(self) -> int:
        return len(self._locs)
    
    def get_SingleDimNode(self, dim:int) -> SingleDimNode:
        return SingleDimNode(self._data, self._locs[dim])
    
    def get_SingleDimNode_list(self) -> list[SingleDimNode]:
        """
        Convert data stored in this FullNode object into a list of
        SingleDimNodes.

        Returns:
            list[SingleDimNode]: A list of n SingleDimNodes, one for each
                location node in self._locs """
                
        return [ SingleDimNode(self._data, self._locs[i]) \
            for i in range(1, self.dimensionality() + 1) ] 
    
    def __str__(self) -> str:
        dict_str = pretty_dict(self._locs, range(1, self.dimensionality()))
        return f"Data: {self._data}, Location:\n{dict_str}"
    
    def __repr__(self) -> str:
        return str(self)
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, FullNode):
            if not self._data == FullNode.data():
                return False
            if not self.dimensionality() == __o.dimensionality():
                return False
            for d in range(1, self.dimensionality() + 1):
                if not self._locs[d] == __o.loc(d):
                    return False
                
            return True
        return False
    
    def __ne__(self, __o: object) -> bool:
        if isinstance(__o, FullNode):
            return not self.__eq__(__o)
        return False