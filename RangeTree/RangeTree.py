from GeneralNodes.FullNode import FullNode
from RangeTree.RangeTreeNode import RangeTreeNode

class RangeTree:
    
    def _build_range_tree(
        self, node_data:list[FullNode], cur_dim:int=1) -> RangeTreeNode:
        
        this_node = RangeTreeNode
    
    def __init__(self, data_set:list[FullNode], dimensionality:int) -> None:
        if len(data_set) == 0:
            raise Exception("data_set is empty. Cannot construct RangeTree.")
        if dimensionality < 1:
            raise Exception(f"dimensionality value ({dimensionality}) must " + \
                "be greater than 1.")
        
        self._dim = dimensionality
        self._root = self._build_range_tree(data_set)
        