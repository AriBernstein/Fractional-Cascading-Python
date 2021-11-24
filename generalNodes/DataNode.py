from Utils.FractionalCascadingUtils import D


class DataNode:
    
    def __init__(self, data:D) -> None:
        self._data = data
    
    def data(self) -> D:
        return self._data
    
    def set_data(self, data) -> None:
        self._data = data
    
    def __eq__(self, __o: object) -> bool:
        if __o != None and isinstance(__o, DataNode):
            return __o.data() == self._data()
        return False
    
    def __ne__(self, __o: object) -> bool:
        if __o != None and isinstance(__o, DataNode):
            return not self.__eq__(__o)
        return False