from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.SingleDimNode import SingleDimNode
from Utils.GeneralUtils import pretty_list

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
            
        _higher_dim_variant (FCNode):
            If promoted, pointer to the the FCNode representing this base node
            in _cur_dim + 1. Otherwise None (default).
            
        _l_list_neighbor (FCNode):
            Pointer to current node's left (lower) neighbor in the linked list.
            
        _r_list_neighbor (FCNode):
            Pointer to current node's right (higher) neighbor in the linked list.
            
        _l_promotional_neighbor, (FCNode), _r_promotional_neighbor (FCNode):
            Nodes in fractional cascading data structures store pointers to the 
            nearest preceding and proceeding nodes in the current dimension with 
            opposite promotional statuses to the current.   """
 
    def __init__(self, base_node:SingleDimNode, dimension:int=None,
                 left_list_neighbor:'FCNode'=None,
                 right_list_neighbor:'FCNode'=None,
                 higher_dim_variant:'FCNode'=None) -> None:
        
        self._base_node = base_node
        self._cur_dim = dimension if dimension is not None else base_node.dim()
        
        self._higher_dim_variant = higher_dim_variant
        
        self._l_list_neighbor = left_list_neighbor
        self._r_list_neighbor = right_list_neighbor
        
        self._l_promotional_neighbor = None
        self._r_promotional_neighbor = None
    
    def prev_node(self) -> 'FCNode':
        return self._l_list_neighbor
    
    def set_prev_node(self, new_prev:'FCNode') -> None:
        self._l_list_neighbor = new_prev
    
    def next_node(self) -> 'FCNode':
        return self._r_list_neighbor
    
    def set_next_node(self, new_next:'FCNode') -> None:
        self._r_list_neighbor = new_next
    
    def copy(self) -> 'FCNode':
        return FCNode(
            base_node=self._base_node, dimension=self._cur_dim,
            left_list_neighbor=self._l_list_neighbor,
            right_list_neighbor=self._r_list_neighbor, 
            higher_dim_variant=self._higher_dim_variant)
        
    def promote(self) -> 'FCNode':
        return FCNode(
            base_node=self._base_node,
            dimension=self._cur_dim + 1, 
            higher_dim_variant=self)
    
    def local(self) -> bool:
        return self.initial_dim() == self._cur_dim
    
    def promoted(self) -> bool: 
        return not self.local()
    
    def base_node(self) -> SingleDimNode:
        return self._base_node
    
    def current_dim(self) -> int:
        return self._cur_dim
    
    def prev_dim(self) -> int:
        return self._higher_dim_variant.current_dim()
    
    def initial_dim(self) -> int:
        return self._base_node.dim()
    
    def set_higher_dim_fc_node(self, hd_node:'FCNode') -> None:
        self._higher_dim_variant = hd_node
        
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
            
            
class FCNodeList:
    
    """
    Class to wrap linked list of FCNodes.
    """
    
    def __init__(self, list_head:FCNode=None, list_tail:FCNode=None, list_size:int=0) -> None:
        self._list_head = list_head
        self._list_tail = list_tail
        self._n = list_size
    
    def head(self) -> FCNode:
        return self._list_head
    
    def tail(self) -> FCNode:
        return self._list_tail
    
    def to_list(self) -> list[FCNode]:
        """
        Returns list[FCNode]:
            FCNode linked list converted into regular ordered list of the same
            type of nodes.  """
        
        fc_node_list = []
        cur_link = self._list_head
        
        while cur_link is not None:
            fc_node_list.append(cur_link)
            cur_link = cur_link.next_node()
        
        return fc_node_list
    
    
    def append(self, fc_node:FCNode) -> None:
        """
        Append fc_node to the (right) end of the linked list. Update the tail.
        
        Args fc_node (FCNode): Node to append.  """
        if self._n == 0:
            self._list_head = self._list_tail = fc_node
        else:            
            self._list_tail.set_next_node(fc_node)
            fc_node.set_prev_node(self._list_tail)
            self._list_tail = fc_node
        
        self._n += 1
    
    def append_left(self, fc_node:FCNode) -> None:
        """
        Append fc_node to the left end of the linked list. Update the head.
        
        Args fc_node (FCNode): Node to append.  """
        if self._n == 0:
            self._list_head = self._list_tail = fc_node
        else:
            self._list_head.set_prev_node(fc_node)
            fc_node.set_next_node(self._list_head)
            self._list_head = fc_node
        self._n += 1
    
    def __len__(self) -> int:
        return self._n
    
    def __str__(self) -> str:
        return pretty_list(self.to_list())