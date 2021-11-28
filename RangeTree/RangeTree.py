from GeneralNodes.FullNode import FullNode
from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix, sort_SingleDimNode_matrix
from GeneralNodes.SingleDimNode import SingleDimNode
from RangeTree.RangeTreeNode import RangeTreeNode
from Utils.GeneralUtils import matrix_subset

class RangeTree:
    
    def _build_range_tree(self, nodes:list[list[SingleDimNode]], cur_dim:int,
                          l_index:int, r_index:int, sort=True) -> RangeTreeNode:
        
        next_dim_subtree = self._build_range_tree(
            nodes, cur_dim + 1, l_index, r_index) if cur_dim < self._dim else None
        
        # Base case - check if leaf:
        if len(nodes[cur_dim]) == 1:
            return RangeTreeNode(nodes[cur_dim][0], next_dim_subtree)
                
        if sort:
            sort_SingleDimNode_matrix(nodes, cur_dim)
        
        m_index = l_index + (r_index - l_index) // 2
        l_subset = matrix_subset(nodes, l_index, m_index)
        r_subset = matrix_subset(nodes, m_index + 1, r_index)
        
        return RangeTreeNode(
            node_info=l_subset[cur_dim][-1],
            left_child=self._build_range_tree(
                l_subset, cur_dim, l_index, m_index, False),
            right_child=self._build_range_tree(
                r_subset, cur_dim, m_index + 1, r_index, False),
            next_dimension_subtree=next_dim_subtree)
    
    
    def __init__(self, data_set:list[FullNode], dimensionality:int) -> None:
        if len(data_set) == 0:
            raise Exception("data_set is empty. Cannot construct RangeTree.")
        if dimensionality < 1:
            raise Exception(f"dimensionality value ({dimensionality}) must " + \
                "be greater than 1.")
        
        self._dim = dimensionality
        self._n = len(data_set)
        self._root = self._build_range_tree(
            fullNode_list_to_SingleDimNode_matrix(data_set), 
            0, self._n - 1, sort=True)