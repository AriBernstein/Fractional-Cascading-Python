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
                 next_dimension_subtree:'RangeTreeNode'=None) -> None:
        self._node_info = node_info
        self._next_dim_subtree = next_dimension_subtree
        self._l_child = left_child
        if left_child:
            self._l_child.set_parent(self)
        
        self._r_child = right_child
        if self._r_child:
            self._r_child.set_parent(self)
            
        self._p = None
    
    def next_dimension_subtree(self) -> 'RangeTreeNode':
        # raise_if_none(self._next_dim_subtree, MissingFieldException,
        #               ("RangeTreeNode", "_next_dim_subtree"))
        return self._next_dim_subtree
    
    def dimension(self) -> int:
        return self._node_info.dim()
    
    def left_child(self) -> 'RangeTreeNode':
        # raise_if_none(self._l_child, MissingFieldException,
        #              ("RangeTreeNode", "_l_child"))
        return self._l_child
    
    def set_left_child(self, left_child:'RangeTreeNode') -> None:
        self._l_child = left_child
    
    def right_child(self) -> 'RangeTreeNode':
        # raise_if_none(self._r_child, MissingFieldException,
        #              ("RangeTreeNode", "_r_child"))
        return self._r_child

    def set_right_child(self, right_child:'RangeTreeNode') -> None:
        self._r_child = right_child
        
    def parent(self) -> 'RangeTreeNode':
        # raise_if_none(self._p, MissingFieldException,
        #              ("RangeTreeNode", "_p (parent)"))
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
    
    def leaves(self, leaf_list:list['RangeTreeNode']=[], locations:bool=False
                ) -> Union[list['RangeTreeNode'], list[LocationNode]]:
        """
        Recursive DFS to return all of the leaves in this subtree.

        Args:
            leaf_list (list[RangeTreeNode]): List of leaves seen so far to be
                passed between recursive calls.

        Returns:
            list['RangeTreeNode']: List of RangeTreeNodes that are leaves of
                this subtree.   """
        if self.is_leaf():
            return [self] if not locations else [self.get_locationNode()]
        
        if self._l_child:
            leaf_list.extend(self._l_child.leaves_locations(leaf_list))
            
        if self._r_child:
            leaf_list.extend(self._r_child.leaves_locations(leaf_list))
        
        return leaf_list
    

    def leaves_locations(self, leaf_list:list[LocationNode]=[]) -> list[LocationNode]:
        """
        Recursive DFS to return all of the leaves in this subtree.

        Args:
            leaf_list (list[RangeTreeNode]): List of leaves seen so far to be
                passed between recursive calls.

        Returns:
            list['RangeTreeNode']: List of RangeTreeNodes that are leaves of
                this subtree.   """
        
        if self.is_leaf():
            return [self.get_locationNode()]
        
        if self._l_child:
            leaf_list.extend(self._l_child.leaves_locations(leaf_list))
            
        if self._r_child:
            leaf_list.extend(self._r_child.leaves_locations(leaf_list))
        
        return leaf_list
    
    
    def lower_dim_locations(self) -> list[LocationNode]:
        locs = [self.get_locationNode()]
        next_dim_r = self.next_dimension_subtree()
        while next_dim_r != None:
            locs.append(next_dim_r.get_locationNode())
            next_dim_r = next_dim_r.next_dimension_subtree()
        return locs
        
    def visualizer_str(self, print_str=False) -> str:
        ret = f"[{str(self)}]"
        
        if self.is_leaf():
            return f"{ret} - {self.lower_dim_locations()}"
        
        ret += f" {pretty_list(self.lower_dim_locations(), '(', ')')}"
        
        if print_str:
            print(ret)
            
        return ret
    
    def __str__(self) -> str:
        return str(self._node_info)
    
    def __repr__(self) -> str:
        return str(self)