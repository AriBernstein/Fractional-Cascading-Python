from GeneralNodes.DataNode import DataNode
from GeneralNodes.LocationNode import LocationNode
from Utils.FractionalCascadingUtils import D, L

class SingleDimNode:
    
    def __init__(self, data:DataNode, location:LocationNode) -> None:
        self._data = data
        self._loc = location
        
    def data(self) -> D:
        return self._data.data()
    
    def dataNode(self) -> DataNode:
        return self._data
    
    def loc(self) -> L:
        return self._loc.loc()
    
    def dim(self) -> int:
        return self._loc.dim()
    
    def locationNode(self) -> LocationNode:
        return self._loc
    
    def __str__(self) -> str:
        return f"Data: {self._data}, Location: {self._loc}"
    
    def __eq__(self, __o: object) -> bool:
        if not __o == None and isinstance(__o, SingleDimNode):
            return __o.data() == self._data and __o.locationNode() == self._loc
        return False
    
    def __ne__(self, __o: object) -> bool:
        if not __o == None and isinstance(__o, SingleDimNode):
            return not self.__eq__(__o)
        return False