from typing import Union
from GeneralNodes.DataNode import DataNode
from GeneralNodes.FullNode import FullNode
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
        self._l_child = left_child
        if left_child:
            self._l_child.set_parent(self)
        
        self._r_child = right_child
        if self._r_child:
            self._r_child.set_parent(self)
        
        self._next_dim_subtree = next_dimension_subtree
        self._p = None
    
    def next_dimension_subtree(self) -> 'RangeTreeNode':
        return self._next_dim_subtree
    
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
    
    def get_leaves(self, mode:int=1) -> list[
        Union['RangeTreeNode', SingleDimNode, DataNode, D, LocationNode, L]]:
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
            leaf_list.extend(self._l_child.get_leaves(mode))
            
        if self._r_child:
            leaf_list.extend(self._r_child.get_leaves(mode))
        
        return leaf_list
    
    
    def lower_dim_locations(self, visual_only=False) -> list[Union[LocationNode, str]]:
        """
        Args:
            visual_only (bool): If true return list of locations denoted as 
                strings. Only useful for visualization purposes. Otherwise
                (default) return list of LocationNodes.
        
        Returns:
            list[LocationNode]: List of LocationNode instances, each correlating
                with a location of this RangeTreeNode in a different demension.
                Inclusive of current dimension. """
        
        locs = [self.get_locationNode().visualizer_str()] \
            if visual_only else [self.get_locationNode()]

        next_dim_root = self.next_dimension_subtree()

        while next_dim_root != None:
            if visual_only:
                locs.append(next_dim_root.get_locationNode().visualizer_str())
            else:
                locs.append(next_dim_root.get_locationNode())
            next_dim_root = next_dim_root.next_dimension_subtree()
        return locs

    def to_full_node(self) -> FullNode:
        """
        Convert RangeTreeNode in first dimension into FullNode.

        Raises:
            Exception: Exception if current RangeTreeNode is not of dimension 1.

        Returns:
            FullNode: Containing this LocationNode's data and locations.    """
        
        if self.dimension() > 1:
            raise Exception("Can only convert RangeTreeNodes of the 1st " + \
                f"dimension into FullNodes. Current dimension: {self.dimension()}.")
        
        loc_dict = {}
        for l_node in self.lower_dim_locations():
            loc_dict[l_node.dim()] = l_node
        
        return FullNode(self.get_dataNode(), loc_dict)
        
    def visualizer_str(self) -> str:
        ret = f"[{str(self.get_location())}]"
        
        if self.is_leaf():
            return f"{ret} - Data: {str(self.get_data())}, " + \
                f"{pretty_list(self.lower_dim_locations(visual_only=True))}"
        
        return ret + f" {pretty_list(self.get_leaves(mode=6), '(', ')')}"
    
    def __str__(self) -> str:
        return str(self._node_info)
    
    def __repr__(self) -> str:
        return str(self)
    
    # Comparisons are in the context of location, not data.
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