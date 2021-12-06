from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.SingleDimNode import SingleDimNode

class FCNode:
    
    """
    Vocabulary - given a node x in a list k: 
        FCNode: Stands for Fractional Cascading Node
        
        Promoted: 
            If x was initially of dimension d, and "promoted" into list k, such
            that it exists in between 0 and (n - k) higher dimensions.
            
        Local:
            If x was initially of dimension k st it does not exist in any higher
            dimensions, it is considered "Local".
            
        Left, Right:
            Nodes to the left & right of x share a current dimension value and 
            have locations in the current dimension less-than/equal-to and
            greater-than that of x, respectively.
            
    Fields:
        _base_node (SingleDimNode):
            Contains location & data of initial node.
        
        _cur_dim (int): 
            The current dimension in which the RangeTreeNode is located. Can 
            also be thought of as the dimension in which it was either 
            instantiated or promoted into. If None, defaults to location of the
            given _base_node upon instantiation.
            
        _higher_dim_fc_node (FCNode):
            If promoted, pointer to the the FCNode representing
            this base node in _cur_dim + 1. Otherwise None (default).
            
        _left_list_neighbor (FCNode):
            Pointer to current node's left (lower) neighbor in the linked list.
            
        _right_list_neighbor (FCNode): Pointer to current node's
            right (higher) neighbor in the linked list.
            
        _left_promotional_neighbor (FCNode):
            Pointer to the closest FCNode in the linked list that is:
                
                1.  "Left" of current node.
                2.  "Promoted" if current node is "local", "local" if current node is promoted.
            
        _right_promotional_neighbor (FCNode): Pointer to the 
            closest FCNode in the linked list that is:
            
                1.  "Right" of current node.
                2.  "Promoted" if current node is "local",  or "local" if current node is promoted.   """
    
    def __init__(self, base_node:SingleDimNode,
                 dimension:int=None,
                 left_list_neighbor:'FCNode'=None,
                 right_list_neighbor:'FCNode'=None,
                 higher_dim_fc_node:'FCNode'=None) -> None:
        
        self._base_node = base_node
        self._cur_dim = dimension if dimension is not None else base_node.dim()
        
        self._higher_dim_fc_node = higher_dim_fc_node
        
        self._left_list_neighbor = left_list_neighbor
        self._right_list_neighbor = right_list_neighbor
        
        self._left_promotional_neighbor = None
        self._right_promotional_neighbor = None
    
    def local(self) -> bool:
        return self.initial_dim() == self._cur_dim
    
    def promoted(self) -> bool: 
        return not self.local()
    
    def base_node(self) -> SingleDimNode:
        return self._base_node
    
    def current_dim(self) -> int:
        return self._cur_dim
    
    def prev_dim(self) -> int:
        return self._higher_dim_fc_node.current_dim()
    
    def initial_dim(self) -> int:
        return self._base_node.dim()
    
    def set_higher_dim_fc_node(self, hd_node:'FCNode') -> None:
        self._higher_dim_fc_node = hd_node
        
    def location(self) -> LocationNode:
        return self._base_node.locationNode()
        
    def __hash__(self) -> int:
        return hash(self._base_node)
    
    def __str__(self) -> str:
        return f"Dim: {self._cur_dim}, Loc: {self._base_node.loc()}, " + \
            f"promoted from dim {self.initial_dim()}."
    
    def __eq__(self, __o: object) -> bool:
        return self.current_dim == __o.current_dim and \
            self.location().loc() == __o.location().loc() \
                if isinstance(__o, FCNode) else False
    
    def __lt__(self, __o: object) -> bool:
        return self.current_dim == __o.current_dim and \
            self.location().loc() < __o.location().loc() \
                if isinstance(__o, FCNode) else False
                
    def __gt__(self, __o: object) -> bool:
        return self.current_dim == __o.current_dim and \
            self.location().loc() > __o.location().loc() \
                if isinstance(__o, FCNode) else False
                
    def __le__(self, __o: object) -> bool:
        return self.current_dim == __o.current_dim and not self > __o \
            if isinstance(__o, FCNode) else False
            
    def __ge__(self, __o: object) -> bool:
        return self.current_dim == __o.current_dim and not self < __o \
            if isinstance(__o, FCNode) else False