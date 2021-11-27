from Utils.TypeUtils import D


class DataNode:
    """
    Node type to act as a container for arbitrary data to be stored in some
    other data structure.
    
    Fields:
        _data (D): Arbitrary piece of information stored in this node.  """
        
    
    def __init__(self, data:D) -> None:
        self._data = data
    
    def data(self) -> D:
        """
        Getter for the data in this node.
        
        Returns:
            D: Arbitrary piece of information stored in this node.  """
        return self._data
    
    def set_data(self, data) -> None:
        """
        Setter for the data in this node.
        
        Args:
            data (D): Arbitrary information to be stored in this node. """
        self._data = data
        
    def __str__(self) -> str:
        return str(self._data)
    
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, DataNode):
            return __o.data() == self._data()
        return False
    
    def __ne__(self, __o: object) -> bool:
        if isinstance(__o, DataNode):
            return not self.__eq__(__o)
        return False