from GeneralNodes.DataNode import DataNode
from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.SingleDimNode import SingleDimNode
from Utils.FractionalCascadingUtils import D

class Node:
    
    def __init__(self, data:DataNode, locations:dict[LocationNode]) -> None:
        self._data = data
        self._locs = locations
        
    def data(self) -> D:
        return self._data.data()
    
    def dataNode(self) -> DataNode:
        return self._data
    
    def locations(self) -> dict[LocationNode]:
        return self._locs
    
    def loc(self, dim:int) -> LocationNode:
        if not 0 < dim <= self.dimensionality():
            raise Exception(f"Invalid dimensionality: {dim}")
        return self._locs[dim]
    
    def dimensionality(self) -> int:
        return len(self._locs)
    
    def getSingleDimNode(self, dim:int) -> SingleDimNode:
        return SingleDimNode(self._data, self._locs[dim])
    
    def __str__(self) -> str:
        return f"Data: {self._data}, Location:\n{self._locs}"
    
    def __eq__(self, __o: object) -> bool:
        if not __o == None and isinstance(__o, Node):
            if not self._data == Node.data():
                return False
            if not self.dimensionality() == __o.dimensionality():
                return False
            for d in range(1, self.dimensionality() + 1):
                if not self._locs[d] == __o.loc(d):
                    return False
                
            return True
        return False
    
    def __ne__(self, __o: object) -> bool:
        if not __o == None and isinstance(__o, Node):
            return not self.__eq__(__o)
        return False