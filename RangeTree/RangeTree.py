from GeneralNodes.FullNode import FullNode
from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix, sort_SingleDimNode_matrix
from GeneralNodes.SingleDimNode import SingleDimNode
from RangeTree.RangeTreeNode import RangeTreeNode
from Utils.GeneralUtils import matrix_subset
from Utils.TypeUtils import L

LEFT, RIGHT = 0, 1

class RangeTree:
    
    def _query_range_tree(self, target:L, cur_root:RangeTreeNode,
                          path:list[tuple[int, RangeTreeNode]]=None,
                          predecessor=True) -> RangeTreeNode:
        """
        Search RangeTree for a specific Node or its predecessor/successor. 

        Args:
            target (L): The Location value for which we are searching.
            cur_root (RangeTreeNode): the root of the current subtree in which 
                we are searching.
            path (list[tuple[int, RangeTreeNode]], optional): A list containing 
                (int, RangeTreeNode) denoting the path taken by this search 
                recursively through the RangeTree.
                    int = 0 -> LEFT, int = 1 -> RIGHT
            predecessor (bool): given that no RangeTreeNode is located at 
                target, if true, return the RangeTreeNode and the preceding 
                location, otherwise return the RangeTreeNode at the succeeding,

        Returns:
            RangeTreeNode: The RangeTreeNode at target location, or that at its 
                preceding or succeeding target location.    """
        
        if cur_root.is_leaf():
            if path != None: path.append((-1, cur_root))
            return cur_root
        
        elif target <= cur_root:
            if path != None: path.append((LEFT, cur_root))
            return self._query_range_tree(cur_root.left_child(), target, path)
        
        else:
            if path != None: path.append((RIGHT, cur_root))
            return self._query_range_tree(cur_root.right_child(), target, path)
                
            
    def _build_range_tree(self, 
        cur_subset:list[list[SingleDimNode]], cur_dim:int=1) -> RangeTreeNode:
        """
        Method to construct the Range Tree.

        Args:
            cur_subset (list[list[SingleDimNode]]): Subset of the matrix of 
                SingleDimNodes being preprocessed into a Range Tree.
            cur_dim (int, optional): The current dimension of the RangeTreeNode
                being constructed. 

        Returns:
            RangeTreeNode: The root of the RangeTree.   """
        
        next_dim_subtree = self._build_range_tree(cur_subset, cur_dim + 1)   \
            if cur_dim < self._dimensionality else None
        
        # Base case - check if leaf:
        if len(cur_subset[cur_dim - 1]) == 1:
            return RangeTreeNode(node_info=cur_subset[cur_dim - 1][0],
                                 next_dimension_subtree=next_dim_subtree)
                
        sort_SingleDimNode_matrix(cur_subset, cur_dim)
        
        l_index = 0
        r_index = len(cur_subset[cur_dim - 1]) - 1
        m_index = l_index + (r_index - l_index) // 2
        
        l_subset = matrix_subset(cur_subset, l_index, m_index)
        r_subset = matrix_subset(cur_subset, m_index + 1, r_index)
                    
        return RangeTreeNode(
            node_info=l_subset[cur_dim - 1][-1],
            left_child=self._build_range_tree(l_subset, cur_dim),
            right_child=self._build_range_tree(r_subset, cur_dim),
            next_dimension_subtree=next_dim_subtree)
    
    
    def __init__(self, data_set:list[FullNode], dimensionality:int) -> None:
        if len(data_set) == 0:
            raise Exception("data_set is empty. Cannot construct RangeTree.")
        if dimensionality < 1:
            raise Exception(f"dimensionality value ({dimensionality}) must " + \
                "be greater than 1.")
        
        self._dimensionality = dimensionality
        self._n = len(data_set)
        self._root = self._build_range_tree(
            fullNode_list_to_SingleDimNode_matrix(data_set))
    
    def root(self):
        return self._root