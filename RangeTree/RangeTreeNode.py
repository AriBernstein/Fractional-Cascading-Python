from GeneralNodes.DataNode import DataNode
from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.SingleDimNode import SingleDimNode
from Utils.FractionalCascadingUtils import D, L

class RangeTreeNode:
    
    def __init__(self, node_info:SingleDimNode):
        self._node_info = node_info
        self._p = self._l_child = self._r_child = self._next_dim_subtree = None
    
    def next_dimension_subtree(self) -> 'RangeTreeNode':
        # TODO: Perform check
        return self._next_dim_subtree
    
    def left_child(self) -> 'RangeTreeNode':
        # TODO: Perform check
        return self._l_child
    
    def set_left_child(self, left_child:'RangeTreeNode') -> None:
        self._l_child = left_child
    
    def right_child(self) -> 'RangeTreeNode':
        # TODO: Perform check
        return self._r_child

    def set_right_child(self, right_child:'RangeTreeNode') -> None:
        self._r_child = right_child
    
    def get_single_dim_node(self) -> SingleDimNode:
        return self._node_info
    
    def get_dataNode(self) -> DataNode:
        return self._node_info.dataNode()
    
    def get_data(self) -> D:
        return self._node_info.dataNode().data()
    
    def get_locationNode(self) -> LocationNode:
        return self._node_info.locationNode()
    
    def get_location(self) -> L:
        return self._node_info.locationNode().loc()
    
    
    