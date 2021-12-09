from enum import Enum
from typing import Union

from GeneralNodes.DataNode import DataNode
from GeneralNodes.FullNode import FullNode
from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.SingleDimNode import SingleDimNode
from Utils.GeneralUtils import pretty_list
from Utils.TypeUtils import D, L

class RangeTreeNode:
    
    """
    Class representing a node for the RangeTree structure.
    
    Fields:
        _single_dim_node (SingleDimNode): Stores all data and location objects.
        
        _l_child (RangeTreeNode): The left child of this RangeTreeNode.
        
        _r_child (RangeTreeNode): The right child of this RangeTreeNode.
        
        _next_dim_subtree (RangeTreeNode): 
            Pointer to a range tree whose root the same data but ordered by the
            following demension.
        
        _p (RangeTreeNode): The parent of this RangeTreeNode.   """
    
    def __init__(self, node_data:SingleDimNode, 
                 left_child:'RangeTreeNode'=None,
                 right_child:'RangeTreeNode'=None,
                 next_dimension_subtree:'RangeTreeNode'=None) -> None:
        
        self._single_dim_node = node_data
        self._l_child = left_child
        if left_child:
            self._l_child.set_parent(self)
        
        self._r_child = right_child
        if self._r_child:
            self._r_child.set_parent(self)
        
        self._next_dim_subtree = next_dimension_subtree
        self._p = None
    
    def next_dimension_subtree(self) -> 'RangeTreeNode':
        """
        Returns RangeTreeNode: 
            Pointer to a range tree whose root the same data but ordered by the
            following demension.    """
        
        return self._next_dim_subtree
    
    def dimension(self) -> int:
        """Returns int: the dimension of the location of this RangeTreeNode. """
        return self._single_dim_node.dim()
    
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
        return self._single_dim_node
    
    def get_dataNode(self) -> DataNode:
        return self._single_dim_node.dataNode()
    
    def get_data(self) -> D:
        return self._single_dim_node.dataNode().data()
    
    def get_locationNode(self) -> LocationNode:
        return self._single_dim_node.locationNode()
    
    def get_location(self) -> L:
        return self._single_dim_node.locationNode().loc()
    
    def is_root(self) -> bool:
        return self._p is None
    
    def is_leaf(self) -> bool:
        return self._l_child is None and self._r_child is None
    
    def get_leaves(self, mode:int=1) -> list[
        Union['RangeTreeNode', SingleDimNode, DataNode, D, LocationNode, L]]:
        """
        Recursive DFS to return all of the leaves in this subtree.

        Args leaf_list (list[RangeTreeNode]): 
            List of leaves seen so far to be passed between recursive calls.

        Returns list['RangeTreeNode']: 
            List of RangeTreeNodes that are leaves of this subtree. """
                
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
        Args visual_only (bool): 
            If true return list of locations denoted as strings (visualization 
            purposes). Otherwise (default) return list of LocationNodes.
        
        Returns list[LocationNode]: 
            List of LocationNode instances, each correlating with a location of
            this RangeTreeNode in each of the lower demensions, inclusive of 
            current dimension.  """
        
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

        Raises Exception:
            Exception if current RangeTreeNode is not of dimension 1.

        Returns FullNode: Containing this LocationNode's data and locations.
        """
        if self.dimension() > 1:
            raise Exception("Can only convert RangeTreeNodes of the 1st " + \
                f"dimension into FullNodes. Current dimension: {self.dimension()}.")
        
        loc_dict = {}
        for l_node in self.lower_dim_locations():
            loc_dict[l_node.dim()] = l_node
        
        return FullNode(self.get_dataNode(), loc_dict)
            
    def visualizer_str(self) -> str:
        """
        Returns str: String meant as a component of RangeTree visualization.    
        """
        
        ret = f"[{str(self.get_location())}]"
        
        if self.is_leaf():
            return f"{ret} - Data: {str(self.get_data())}, " + \
                f"{pretty_list(self.lower_dim_locations(visual_only=True))}"
        
        return ret + f" {pretty_list(self.get_leaves(mode=6), '(', ')')}"
    
    def __str__(self) -> str:
        if self._color is not None: # Red black tree experiment
            return f"(Color: {self._color}, " + str(self._single_dim_node)[1:]
        
        return str(self._single_dim_node)
    
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
    
    ######################## Red-black tree experiments ########################
    class rb_color(Enum):
        red = 1
        black = 0
        
        def __str__(self) -> str:
            return "red" if self.value else "black"
        
        def __repr__(self) -> str:
            return str(self)
        
    _color = None
    _black_node_quota = None
    
    def is_red(self) -> bool: return self._color == self.rb_color.red
    def is_black(self) -> bool: self._color == self.rb_color.black
        
    def color_node(self) -> None:
        
        if self.is_root():
            self._color = self.rb_color.black
            self._black_node_quota = -(-self._get_height(self) // 2) # Round up
        
        elif self.parent().is_red():
            self._color = self.rb_color.black
            self._black_node_quota = self.parent()._black_node_quota
        
        else:
            min_h = self._get_height(self, max_h=False)
            
            if min_h < self.parent()._black_node_quota:
                raise Exception("Tree is too imbalanced for Red Black form.")

            elif min_h == self.parent()._black_node_quota:
                self._color = self.rb_color.black
            
            else:   # min_h < parent black node quota
                self._color = self.rb_color.red
                
            self._black_node_quota = self.parent()._black_node_quota - 1
            
    def color_children(self, cur_node=None) -> None:
        if cur_node is None:
            cur_node = self
        
        self.color_node()
        
        if self.left_child() is not None:
            self.color_children(self.left_child)
        
        if self.right_child is not None:
            self.color_children(self.right_child())
            
            
    def _get_height(self, cur_root:'RangeTreeNode', cur_h:int=0, max_h:bool=True) -> int:
        """
        Return the height of the tree rooted at cur_node.

        Args:
            cur_root (RangeTreeNode): The subtree in the current recursive step.
           
            cur_h (int, optional): Height of our tree thus far.
           
            max_h (bool, optional):
                If true (default), find distance from cur_root to "deepest"
                leaf, else distance to "shallowest" leaf.
                
        Returns: int: height of tree.   """
        
        if cur_root.is_leaf():
            return cur_h + 1
        
        l_height, r_height = None, None
        
        if self.left_child():
            l_height = self._get_height(cur_root.left_child(), cur_h + 1, max_h)
        if self.right_child():
            r_height = self._get_height(cur_root.right_child(), cur_h + 1, max_h)
        
        if l_height is not None and r_height is not None:
            return max(l_height, r_height) if max_h else min(l_height, r_height)
        
        elif l_height is not None:
            return l_height
        else:
            return r_height  