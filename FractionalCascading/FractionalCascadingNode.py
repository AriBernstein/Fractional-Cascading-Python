from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.SingleDimNode import SingleDimNode
from Utils.CustomExceptions import InvalidTypeException


class FractionalCascadingNode:
    
    """
    Vocabulary:
        Given a node x in a list k, if x was promoted into k from a dimension d
            -> d > k
        Promoted: Then x is promoted. Otherwise (if it was initially in k) 
            it is not promoted.
        Foreign: Given a 
    
    
    """
    
    def __init__(self, base_node:SingleDimNode,
                 dimension:int=None, promoted:bool=False,
                 left_list_neighbor:'FractionalCascadingNode'=None,
                 right_list_neighbor:'FractionalCascadingNode'=None,
                 higher_dim_fc_node:'FractionalCascadingNode'=None) -> None:
        
        self._base_node = base_node
        self._promoted = promoted
        self._cur_dim = dimension if dimension is not None else base_node.dim()
        
        self._higher_dim_fc_node = higher_dim_fc_node
        
        self._left_list_neighbor = left_list_neighbor
        self._right_list_neighbor = right_list_neighbor
        
        self._left_higher_dim_neighbor = None
        self._right_higher_dim_neighbor = None
    
    
    def promoted(self) -> bool: return self._promoted
    def local(self) -> bool: return not self._promoted
    
    def base_node(self) -> SingleDimNode:
        return self._base_node
    
    def current_dim(self) -> int:
        return self._cur_dim
    
    def prev_dim(self) -> int:
        return self._higher_dim_fc_node.current_dim()
    
    def initial_dim(self) -> int:
        return self._base_node.dim()
    
    def set_higher_dim_fc_node(self, hd_node:'FractionalCascadingNode') -> None:
        self._higher_dim_fc_node = hd_node
    
    def higher_dim(self, __o:object) -> bool:
        if isinstance(__o, FractionalCascadingNode):
            return InvalidTypeException(str(type(__o)), "FractionalCascadingNode")
        
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
                if isinstance(__o, FractionalCascadingNode) else False

    def __lt__(self, __o: object) -> bool:
        return self.current_dim == __o.current_dim and \
            self.location().loc() < __o.location().loc() \
                if isinstance(__o, FractionalCascadingNode) else False
    
    def __gt__(self, __o: object) -> bool:
        return self.current_dim == __o.current_dim and \
            self.location().loc() > __o.location().loc() \
                if isinstance(__o, FractionalCascadingNode) else False
                
    def __le__(self, __o: object) -> bool:
        return self.current_dim == __o.current_dim and not self > __o \
            if isinstance(__o, FractionalCascadingNode) else False
            
    def __ge__(self, __o: object) -> bool:
        return self.current_dim == __o.current_dim and not self < __o \
            if isinstance(__o, FractionalCascadingNode) else False