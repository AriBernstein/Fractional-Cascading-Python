from GeneralNodes.LocationNode import LocationNode
from Utils.CustomExceptions import InvalidInputException
from Utils.GeneralUtils import pretty_list
from Utils.TypeUtils import L

class FCNode:
    
    """
    Vocabulary -> given a node x in a list k: 
        FCNode: Stands for Fractional Cascading Node
        
        Promoted: 
            If x was initially of dimension d, and "promoted" into list k, such
            that it exists in between 0 and (n - k) higher dimensions.
            
        Local:
            If x was initially of dimension k st it does not exist in any higher
            dimensions, it is considered "Local". (Opposite of promoted.)
            
        Foreign:
            Of a different original dimension dimension.
            
        Left, Right:
            Nodes to the left & right of x share a current dimension value and 
            have locations in the current dimension less-than/equal-to and
            greater-than that of x, respectively.
            
    Fields:
        _base_node (LocationNode):
            Contains location & data of initial node.
        
        _cur_dim (int): 
            The current dimension in which the RangeTreeNode is located. Can 
            also be thought of as the dimension in which it was either 
            instantiated or promoted into. If None, defaults to location of the
            given _base_node upon instantiation.
            
        _higher_dim_variant (FCNode):
            If promoted, pointer to the the FCNode representing this base node
            in _cur_dim + 1. Otherwise None (default).
            
        _l_list_neighbor (FCNode), _r_list_neighbor (FCNode):
            Pointer to current node's left (lower) neighbor and right (higher) 
            neighbor respectively in the linked list.
            
        _l_f_neighbor, (FCNode), _r_f_neighbor (FCNode):
            _l_f_neighbor -> left_foreign_neighbor
            _r_f_neighbor -> right_forign_neighbor.
            
            Nodes in fractional cascading data structures store pointers to the 
            nearest preceding and proceeding nodes in the current dimension with 
            opposite promotional statuses to the current.   """
 
    def __init__(self, base_node:LocationNode, dimension:int=None,
                 left_list_neighbor:'FCNode'=None,
                 right_list_neighbor:'FCNode'=None,
                 higher_dim_variant:'FCNode'=None) -> None:
        if dimension is not None and dimension <= 0:
            raise InvalidInputException(
                "dimension", str(dimension), "greater than 1", "FCNode")
        
        self._base_node = base_node
        self._cur_dim = dimension if dimension is not None else base_node.dim()
        
        self._higher_dim_variant = higher_dim_variant
        
        self._l_list_neighbor = left_list_neighbor
        self._r_list_neighbor = right_list_neighbor
        
        self._l_f_neighbor = None
        self._r_f_neighbor = None
    
    def dim(self) -> int:
        """
        Returns: int: Current dimension of this FCNode. """
        return self._cur_dim
    
    def base_dim(self) -> int:
        """
        Returns: int: Initial dimension of the LocationNode of this FCNode. """
        return self._base_node.dim()
    
    def loc(self) -> L:
        """
        Returns: L: The location in the LocationNode in this FCNode.    """
        return self._base_node.loc()
    
    def prev_list_neighbor(self) -> 'FCNode':
        """
        Returns: FCNode: the previous (or left) linked list element. (Assigned 
        during node promotion.)  """
        return self._l_list_neighbor
    
    def set_prev_list_neighbor(self, new_prev:'FCNode') -> None:
        self._l_list_neighbor = new_prev
    
    def next_list_neighbor(self) -> 'FCNode':
        """
        Returns: FCNode: the next (or right) linked list element. (Assigned 
        during node promotion.)  """
        return self._r_list_neighbor
    
    def set_next_list_neighbor(self, new_next:'FCNode') -> None:
        self._r_list_neighbor = new_next
        
    def prev_foreign_neighbor(self) -> 'FCNode':
        """
        Returns: FCNode: the prev (or left) foreign linked list element (not
        from the original dimension stored in _base_node. of this instance. """
        return self._l_f_neighbor
    
    def set_prev_f_neighbor(self, left_foreign_neighbor:'FCNode') -> None:
        self._l_f_neighbor = left_foreign_neighbor
                
    def next_foreign_neighbor(self) -> 'FCNode':
        """
        Returns: FCNode: the next (or right) foreign linked list element (not
        from the original dimension stored in _base_node. of this instance. """
        return self._r_f_neighbor
    
    def set_next_f_neighbor(self, right_foreign_neighbor:'FCNode') -> None:
        self._r_f_neighbor = right_foreign_neighbor
    
    def copy(self) -> 'FCNode':
        """
        Returns: FCNode: 
            New FCNode instance with the exact same field values as this.   """
        return FCNode(
            base_node=self._base_node, dimension=self._cur_dim,
            left_list_neighbor=self._l_list_neighbor,
            right_list_neighbor=self._r_list_neighbor, 
            higher_dim_variant=self._higher_dim_variant)
        
    def promote(self) -> 'FCNode':
        """
        Returns: FCNode: 
            New FCNode instance with same _base_node, decremented current dim, 
            and no pointers to other list elements. The _higher_dim_variant of
            this new instance is the current instance (self).   """
        return FCNode(
            base_node=self._base_node,
            dimension=self._cur_dim - 1, 
            higher_dim_variant=self)
    
    def is_local(self) -> bool:
        return self.initial_dim() == self._cur_dim
    
    def is_promoted(self) -> bool:
        return not self.is_local()
    
    def base_node(self) -> LocationNode:
        return self._base_node
    
    def current_dim(self) -> int:
        return self._cur_dim
    
    def prev_dim_variant(self) -> 'FCNode':
        """
        Returns: FCNode: The FCNode representing the current in a higher 
        (previous) dimension.   """
        return self._higher_dim_variant
    
    def prev_dim(self) -> int:
        return self._higher_dim_variant.current_dim()
    
    def initial_dim(self) -> int:
        return self._base_node.dim()
    
    def set_higher_dim_fc_node(self, h_d_node:'FCNode') -> None:
        self._higher_dim_variant = h_d_node
        
    def __hash__(self) -> int:
        return hash(self._base_node)
    
    def __str__(self) -> str:
        cur_dim_label = self._cur_dim
        if self._cur_dim <= 3 and self.base_node()._dim_label is not None:
            cur_dim_label = 'x' if self._cur_dim == 1 else 'y' \
                if self._cur_dim == 2 else 'z'
        
        # return f"(Cur Dim: {cur_dim_label}, Base {self.base_node()})"
        return f"(C Dim: {cur_dim_label}, B {self.base_node()})"

    
    def __repr__(self) -> str:
        return str(self)
    
    # NOTE: These do not consider dimensionality of the base_node and may as 
    #       such equate two items as equal when the base nodes contain the same
    #       value but are of different initial dimensions.
    def __eq__(self, __o: object) -> bool:
        return self.current_dim() == __o.current_dim() and \
            self._base_node.loc() == __o.base_node().loc() \
                if isinstance(__o, FCNode) else False
    
    def __lt__(self, __o: object) -> bool:
        return self.current_dim() == __o.current_dim() and \
            self._base_node.loc() < __o.base_node().loc() \
                if isinstance(__o, FCNode) else False
                
    def __gt__(self, __o: object) -> bool:
        return self.current_dim() == __o.current_dim() and \
            self._base_node.loc() > __o.base_node().loc() \
                if isinstance(__o, FCNode) else False
                
    def __le__(self, __o: object) -> bool:
        return self.current_dim() == __o.current_dim() and not self > __o \
            if isinstance(__o, FCNode) else False
            
    def __ge__(self, __o: object) -> bool:
        return self.current_dim() == __o.current_dim() and not self < __o \
            if isinstance(__o, FCNode) else False
            

class FCList:
    
    """
    Class to wrap linked list of FCNodes.
    """
    
    def __init__(self) -> None:
        self._list_head = None
        self._list_tail = None
        self._n = 0
    
    def head(self) -> FCNode:
        """
        Returns: FCNode: The FCNode at the head of the linked list of nodes.
        """
        return self._list_head
    
    def tail(self) -> FCNode:
        """
        Returns: FCNode: The FCNode at the tail of the linked list of nodes.
        """
        return self._list_tail
    
    def to_list(self) -> list[FCNode]:
        """
        Returns: list[FCNode]:
            FCNode linked list converted into regular ordered list of the same
            type of nodes.  """
        
        fc_node_list = []
        cur_link = self._list_head
        
        while cur_link is not None:
            fc_node_list.append(cur_link)
            cur_link = cur_link.next_list_neighbor()
        
        return fc_node_list
    
    def append(self, fc_node:FCNode) -> None:
        """
        Append fc_node to the (right) end of the linked list. Update the tail.
        
        Args: fc_node (FCNode): Node to append.  """
        if self._n == 0:
            self._list_head = self._list_tail = fc_node
        else:            
            self._list_tail.set_next_list_neighbor(fc_node)
            fc_node.set_prev_list_neighbor(self._list_tail)
            self._list_tail = fc_node
        self._n += 1
    
    def get_promoted_subset(self) -> 'FCList':
        """
        Returns: FCList: 
            FCList containing every second element of this one, relative
            ordering maintained.    """
        add_node = True
        subset = FCList()
        subset_pointer = self._list_head
        
        while(subset_pointer is not None):
            if add_node:
                subset.append(subset_pointer.promote())
                add_node = False
            else:
                add_node = True
                
            subset_pointer = subset_pointer.next_list_neighbor()
        
        return subset
    
    def copy(self) -> 'FCList':
        cp, cp_pointer = FCList(), self._list_head        
        while cp_pointer is not None:
            cp.append(cp_pointer.copy())
            cp_pointer = cp_pointer.next_list_neighbor()
        return cp
    
    def __len__(self) -> int:
        return self._n
    
    def __str__(self) -> str:
        return pretty_list(self.to_list())
    
    def __repr__(self) -> str:
        return str(self)