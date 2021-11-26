from GeneralNodes.DataNode import DataNode
from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.SingleDimNode import SingleDimNode
from Utils.FractionalCascadingUtils import D
from Utils.PrettyPrintingUtils import pretty_dict
from Utils.FractionalCascadingExceptions import InvalidDimensionalityException

class FullNode:
    """
    Node type to store all information associated with a given node,
    specifically its DataNode and all LocationNodes.
    
    Fields:
        _data (DataNode): DataNode instance representing this FullNode's data.
        _locations (dict[int, LocationNode]): Dictionary with:
            key -> integer representing dimension,
            pair -> LocationNode representing location in given dimension.
        _dimensionality (int): Represents number of location values in which
            this FullNode exists.   """
    
    def __init__(self, data:DataNode, locations:dict[int, LocationNode]) -> None:
        """
        Args:
            data (DataNode): The DataNode to be stored in this FullNode.
            locations (dict[int, LocationNode]): A dictionary representing all
                the locations of this node in each dimension.   """
        self._data = data
        self._locs = locations
        self._dimensionality = len(locations)
        
    def data(self) -> D:
        """
        Returns:
            D: Arbitrary data stored in the DataNode stored this FullNode
                instance.   """
        return self._data.data()
    
    def dataNode(self) -> DataNode:
        """
        Returns:
            DataNode: The DataNode stored in this FullNode instance.    """
        return self._data
    
    def locations(self) -> dict[int, LocationNode]:
        """
        Getter for the dictionary representing the locations of this FullNode
        instance.
            key -> integer representing dimension,
            pair -> LocationNode representing location in given dimension.
        
        Returns:
            dict[int, LocationNode]: The dictionary representing the locations
                of this FullNode instance in each dimension.    """
        return self._locs
    
    def loc(self, d:int) -> LocationNode:
        """
        Args:
            d (int): The dimension for the LocationNode in question.

        Raises:
            InvalidDimensionalityException: When d value is invalid for this
                FullNode instance.

        Returns:
            LocationNode: The LocationNode associated with the dth dimension.
        """
        if not 1 <= d <= self.dimensionality():
            raise InvalidDimensionalityException(d, self.dimensionality())
        return self._locs[d]
    
    def dimensionality(self) -> int:
        """
        Returns:
            int: Number of dimensions in which this FullNode instance is located.
        """
        return len(self._locs)
    
    def get_SingleDimNode(self, d:int) -> SingleDimNode:
        """
        Args:
            d (int): The single dimension of the returned SingleDimNode.
        Returns:
            SingleDimNode: SingleDimNode representing the data from this
                FullNode instance as well as its location in the dth dimension.
        """
        return SingleDimNode(self._data, self.loc(d))
    
    def get_SingleDimNode_list(self) -> list[SingleDimNode]:
        """
        Convert data stored in this FullNode object into a list of
        SingleDimNodes.

        Returns:
            list[SingleDimNode]: A list of n SingleDimNodes, one for each
                LocationNode in self._locs """
                
        return [ SingleDimNode(self._data, self._locs[i]) \
            for i in range(1, self.dimensionality() + 1) ]
    
    def __str__(self) -> str:
        dict_str = pretty_dict(self._locs, range(1, self.dimensionality() + 1))
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