from typing import Union
from GeneralNodes.DataNode import DataNode
from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.SingleDimNode import SingleDimNode
from Utils.GeneralUtils import pretty_list
from Utils.TypeUtils import D, L
from Utils.CustomExceptions import MissingFieldException, raise_if_none

class RangeTreeNode:
    
    def __init__(self, node_info:SingleDimNode, 
                 left_child:'RangeTreeNode'=None,
                 right_child:'RangeTreeNode'=None,
                 next_dimension_subtree:'RangeTreeNode'=None,
                 prev_dimension_subtree:'RangeTreeNode'=None) -> None:
        self._node_info = node_info
        self._l_child = left_child
        if left_child:
            self._l_child.set_parent(self)
        
        self._r_child = right_child
        if self._r_child:
            self._r_child.set_parent(self)
        
        self._next_dim_subtree = next_dimension_subtree
        self._prev_dim_subtree = prev_dimension_subtree
        self._p = None
    
    def next_dimension_subtree(self) -> 'RangeTreeNode':
        return self._next_dim_subtree
    
    def prev_dimension_subtree(self) -> 'RangeTreeNode':
        return self._prev_dim_subtree
    
    def set_prev_dim_subtree(self, prev_dim_subtree:'RangeTreeNode'):
        self._prev_dim_subtree = prev_dim_subtree
    
    def dimension(self) -> int:
        return self._node_info.dim()
    
    def left_child(self) -> 'RangeTreeNode':
        return self._l_child
    
    def set_left_child(self, left_child:'RangeTreeNode') -> None:
        self._l_child = left_child
    
    def right_child(self) -> 'RangeTreeNode':
        return self._r_child

    def set_right_child(self, right_child:'RangeTreeNode') -> None:
        self._r_child = right_child
        
    def parent(self) -> 'RangeTreeNode':
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
    
    def get_leaves(self, mode:int=1) -> list:
        """
        Recursive DFS to return all of the leaves in this subtree.

        Args:
            leaf_list (list[RangeTreeNode]): List of leaves seen so far to be
                passed between recursive calls.

        Returns:
            list['RangeTreeNode']: List of RangeTreeNodes that are leaves of
                this subtree.   """
                
        if self.is_leaf():
            if mode == 1:
                return [self]
            if mode == 2:
                return [self.get_single_dim_node()]
            if mode == 3:
                return [self.get_dataNode()]
            if mode == 4:
                return [self.get_data()]
            if mode == 5:
                return [self.get_locationNode()]
            if mode == 6:
                return [self.get_locationNode().loc()]
        
        leaf_list = []
        
        if self._l_child:
            leaf_list.extend(
                self._l_child.get_leaves(mode))
            
        if self._r_child:
            leaf_list.extend(
                self._r_child.get_leaves(mode))
        
        return leaf_list
    
    
    def lower_dim_locations(self) -> list[LocationNode]:
        locs = [self.get_locationNode().visualizer_str()]
        next_dim_root = self.next_dimension_subtree()
        while next_dim_root != None:
            locs.append(next_dim_root.get_locationNode().visualizer_str())
            next_dim_root = next_dim_root.next_dimension_subtree()
        return locs
        
    def visualizer_str(self) -> str:
        ret = f"[{str(self.get_data())}]"
        
        if self.is_leaf():
            return f"{ret} - {pretty_list(self.lower_dim_locations())}"
        
        return ret + f" {pretty_list(self.get_leaves(mode=6), '(', ')')}"
    
    def __str__(self) -> str:
        return str(self._node_info)
    
    def __repr__(self) -> str:
        return str(self)
            
    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, RangeTreeNode):
            return self.get_locationNode() == __o.get_locationNode()
        return False
    
    def __gt__(self, __o: object) -> bool:
        if isinstance(__o, RangeTreeNode):
            return self.get_locationNode() > __o.get_locationNode()
        return False
    
    def __lt__(self, __o: object) -> bool:
        if isinstance(__o, RangeTreeNode):
            return self.get_locationNode() < __o.get_locationNode()
        return False    
    
    def __ge__(self, __o: object) -> bool:
        if isinstance(__o, RangeTreeNode):
            return not self < __o.get_locationNode()
        return False
    
    def __ge__(self, __o: object) -> bool:
        if isinstance(__o, RangeTreeNode):
            return not self > __o.get_locationNode()
        return False