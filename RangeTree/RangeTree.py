from GeneralNodes.FullNode import FullNode
from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix
from GeneralNodes.SingleDimNode import SingleDimNode
from RangeTree.RangeTreeNode import RangeTreeNode

class RangeTree:
    
    def _build_range_tree(self, nodes:list[list[SingleDimNode]], cur_dim:int,
                          l_sub_index:int, r_sub_index:int) -> RangeTreeNode:

        cur_node_subset = nodes[cur_dim][l_sub_index:r_sub_index + 1]
        this_rt_node = RangeTreeNode()
    
    
    def __init__(self, data_set:list[FullNode], dimensionality:int) -> None:
        if len(data_set) == 0:
            raise Exception("data_set is empty. Cannot construct RangeTree.")
        if dimensionality < 1:
            raise Exception(f"dimensionality value ({dimensionality}) must " + \
                "be greater than 1.")
        
        self._dim = dimensionality
        self._n = len(data_set)
        self._root = self._build_range_tree(
            fullNode_list_to_SingleDimNode_matrix(data_set))