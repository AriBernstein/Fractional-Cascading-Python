from GeneralNodes.DataNode import DataNode
from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.SingleDimNode import SingleDimNode
from Utils.TypeUtils import D, L
from Utils.FractionalCascadingExceptions import MissingFieldException, raise_if_none

class RangeTreeNode:
    
    def __init__(self, node_info:SingleDimNode):
        self._node_info = node_info
        self._p = self._l_child = self._r_child = self._next_dim_subtree = None
    
    def next_dimension_subtree(self) -> 'RangeTreeNode':
        raise_if_none(self._next_dim_subtree, MissingFieldException,
                      ("RangeTreeNode", "_next_dim_subtree"))
        return self._next_dim_subtree
    
    def dimension(self) -> int:
        return self._node_info.dim()
    
    def left_child(self) -> 'RangeTreeNode':
        raise_if_none(self._l_child, MissingFieldException,
                     ("RangeTreeNode", "_l_child"))
        return self._l_child
    
    def set_left_child(self, left_child:'RangeTreeNode') -> None:
        self._l_child = left_child
    
    def right_child(self) -> 'RangeTreeNode':
        raise_if_none(self._r_child, MissingFieldException,
                     ("RangeTreeNode", "_r_child"))
        return self._r_child

    def set_right_child(self, right_child:'RangeTreeNode') -> None:
        self._r_child = right_child
        
    def parent(self) -> 'RangeTreeNode':
        raise_if_none(self._p, MissingFieldException,
                     ("RangeTreeNode", "_p (parent)"))
        return self._p
    
    def set_parent(self, parent:'RangeTreeNode') -> None:
        self._p = parent
    
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
    
    def is_leaf(self) -> bool:
        return self._l_child == None and self._r_child == None
    
    def leaves(self, leaf_list:list['RangeTreeNode']=[]) -> list['RangeTreeNode']:
        """
        Recursive DFS to return all of the leaves in this subtree.

        Args:
            leaf_list (list[RangeTreeNode]): List of leaves seen so far to be
                passed between recursive calls.

        Returns:
            list['RangeTreeNode']: List of RangeTreeNodes that are leaves of
                this subtree.   """
        
        if self.is_leaf():
            return [self]
        
        if self._l_child:
            leaf_list.extend(self._l_child.leaves(leaf_list))
            
        if self._r_child:
            leaf_list.extend(self._r_child.leaves(leaf_list))
        
        return leaf_list
    
    def __str__(self) -> str:
        return str(self._node_info)
    
    def __repr__(self) -> str:
        return str(self)