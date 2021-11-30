from GeneralNodes.FullNode import FullNode
from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix, sort_SingleDimNode_matrix
from GeneralNodes.SingleDimNode import SingleDimNode
from RangeTree.RangeTreeNode import RangeTreeNode
from Utils.CustomExceptions import InvalidDimensionalityException
from Utils.GeneralUtils import matrix_subset
from Utils.TypeUtils import L

LEFT, RIGHT = 0, 1

class RangeTree:
    
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
        
        # Start by constructing tree in following dimensions.
        next_dim_subtree = None
        if cur_dim < self._dimensionality:
            next_dim_subtree = self._build_range_tree(cur_subset, cur_dim + 1)
        
        # Base case - check if leaf:
        if len(cur_subset[cur_dim - 1]) == 1:
            this_leaf = RangeTreeNode(node_info=cur_subset[cur_dim - 1][0],
                                      next_dimension_subtree=next_dim_subtree)
            if next_dim_subtree:
                next_dim_subtree.set_prev_dim_subtree(this_leaf)
            
            return this_leaf
                
        sort_SingleDimNode_matrix(cur_subset, cur_dim)
        
        l_index = 0
        r_index = len(cur_subset[cur_dim - 1]) - 1
        m_index = l_index + (r_index - l_index) // 2
        
        l_subset = matrix_subset(cur_subset, l_index, m_index)
        r_subset = matrix_subset(cur_subset, m_index + 1, r_index)
                    
        this_root = RangeTreeNode(
            node_info=l_subset[cur_dim - 1][-1],
            left_child=self._build_range_tree(l_subset, cur_dim),
            right_child=self._build_range_tree(r_subset, cur_dim),
            next_dimension_subtree=next_dim_subtree)
        
        if next_dim_subtree:
            next_dim_subtree.set_prev_dim_subtree(this_root)
            
        return this_root
    
    
    def _query(self, target:L, cur_root:RangeTreeNode,
               path:list[tuple[int, RangeTreeNode]]=None,
               successor=False) -> RangeTreeNode:
        """
        Search RangeTree for a specific Node or its predecessor/successor. 

        Args:
            target (L): The Location value of the RangeTreeNode for which we are
                searching.
            cur_root (RangeTreeNode): the root of the current subtree in which 
                we are searching.
            path (list[tuple[int, RangeTreeNode]], optional): A list containing 
                (int, RangeTreeNode) denoting the path taken by this search 
                recursively through the RangeTree.
                    int = 0 -> LEFT, int = 1 -> RIGHT
            successor (bool): given that no RangeTreeNode is located at 
                target, if true, return the RangeTreeNode at the succeeding 
                location. Otherwise (and by default), return the RangeTreeNode 
                at the succeeding location.

        Returns:
            RangeTreeNode: The RangeTreeNode at target location, or that at its 
                preceding or succeeding target location.    """
        # TODO: Implement successor (currently defaults to predecessor)
        
        if cur_root.is_leaf():
            if not path is None: path.append((-1, cur_root))
            return cur_root
        
        elif target <= cur_root.get_location():
            if not path is None: path.append((LEFT, cur_root))
            return self._query(target, cur_root.left_child(), path, successor)
        
        else:
            if not path is None: path.append((RIGHT, cur_root))
            return self._query(target, cur_root.right_child(), path, successor)
        
    
    def query(self, target:L, search_dimension:int=1) -> list[SingleDimNode]:
        """
        Search RangeTree for a specific Node or its predecessor/successor. 

        Args:
            target (L): The Location value of the RangeTreeNode for which we are
                searching.
            search_dimension (int): The demension in which to search for nodes 
                at this location. Defaults to 1.

        Returns:
            list[SingleDimNode]: A list of SingleDimNodes, each representing a
                the data's location in a different dimension.
        """
        if not (1 <= search_dimension <= self._dimensionality):
            raise InvalidDimensionalityException(search_dimension,
                                                 self._dimensionality)
            
        cur_root = self._root
        while cur_root.dimension() < search_dimension:
            cur_root = cur_root.next_dimension_subtree()
        print("HELLOOO")
        print(cur_root)
        
        ret_node = self._query(target, cur_root)
        while ret_node.dimension() > 1:
            print("HERE")
            ret_node = ret_node.prev_dimension_subtree()
        
        ret_list = []
        while ret_node is not None:
            ret_list.append(ret_node.get_single_dim_node())
            ret_node = ret_node.next_dimension_subtree()
        
        return ret_list
            
    def _range_search_rec_helper(
        self, cur_root:RangeTreeNode, cur_dim:int, range_mins:list[type[L]],
        range_maxes:list[type[L]]) -> list[RangeTreeNode]:
        
        range_min, range_max = range_mins[cur_dim - 1], range_maxes[cur_dim - 1] 
        
        def in_range(loc:L) -> bool:
            return range_min <= loc <= range_max
        
        # Find leftmost and rightmost nodes in range and populate path lists
        # Note: range_max_node will either be the smallest node with location
        #       greater than low_range or equal to it.
        range_min_path = [] # type: list[tuple[int, RangeTreeNode]] 
        range_max_path = [] # type: list[tuple[int, RangeTreeNode]] 
        range_min_node = self._query(range_min, cur_root, range_min_path)
        range_max_node = self._query(range_max, cur_root, range_max_path)
        paths_diverge = range_min_node != range_max_node
        paths_diverge_index = 0
        
        # Find split_node (node at which lowRange & highRange paths diverge)
        if paths_diverge:
            shortest_path_len = min(len(range_min_path), len(range_max_path))
            for i in range(shortest_path_len):
                cur_min_direction, cur_min_node = range_min_path[i]
                cur_max_direction, cur_max_node = range_max_path[i] 
                
                if cur_min_node.is_leaf() or cur_max_node.is_leaf():
                    break
                elif cur_min_direction == cur_max_direction:
                    paths_diverge_index = i + 1
                else:
                    break
        else:
            paths_diverge_index = len(range_min_path) - 2
            
            
        # Lists of RangeTreeNodes representing canonical subsets
        # -> If current dimension is less than dimensionality, recurse on each.
        # -> Else return canonical subset (representing nodes in final dimension)
        canonical_subsets = []  # type: list[RangeTreeNode]
        
        # Find canonical subsets by separately traversing the left and right
        # subtrees of rangeSplitNode
        
        # Handle low range
        # -> check for edge case of one leaf node in path
        # -> else save roots from right subtrees when path veers left
        if len(range_min_path) == 1:
            _, subtree = range_min_path[0]
            if subtree.is_leaf() and in_range(subtree.get_location()):
                canonical_subsets.append(subtree)
        else:
            for i in range(paths_diverge_index + 1, len(range_min_path)):
                direction, subtree = range_min_path[i]
                
                # Edge case where right-most subtree is out of range
                if subtree.is_leaf() and in_range(subtree.get_location()):
                    canonical_subsets.append(subtree)
                
                # Regular case
                elif direction == LEFT and subtree.right_child() is not None:
                    canonical_subsets.append(subtree.right_child())                    
                else:
                    # TODO - add exception
                    raise Exception("WTF")
                            
        # Handle high range
        # -> Ensure that paths aren't identical (ie all of the work hasn't 
        #    already been finished in low range traversal).
        # -> If not, save roots of left subtrees when path veers right.
        if paths_diverge:
            if len(range_max_path) == 1:
                # Avoid scenario where rightmost node is out of range
                _, subtree = range_max_path[0]
                if subtree.is_leaf() and in_range(subtree.get_location()):
                    canonical_subsets.append(subtree)
            else:
                for i in range(paths_diverge_index + 1, len(range_max_path)):
                    direction, subtree = range_min_path[i]
                    
                    if subtree.is_leaf() and in_range(subtree.get_location()):
                        canonical_subsets.append(subtree)
                    elif direction == RIGHT and subtree.left_child() is not None:
                        canonical_subsets.append(subtree.left_child())                    
                    else:
                    # TODO - add exception
                        raise Exception("WTF")
        
        # Handle case where no nodes are in range:
        # TODO - add predecessor/successor settings and only perform this step 
        #        when neither are accepted
        if len(canonical_subsets) == 1 and canonical_subsets[0].is_leaf():
            if not in_range(canonical_subsets[0].get_location()):
                canonical_subsets = []
        
        # Recurse on next dimension on each canonical subset
        # -> nodesInRange should contain the RangeTreeNodes that make up the
        #    canonical subsets of the final dimension.
        nodes_in_range = []
        if cur_dim < self._dimensionality:
            for canonical_root in canonical_subsets:
                nodes_in_range.extend(
                    self._range_search_rec_helper(
                        canonical_root.next_dimension_subtree(),
                        cur_dim + 1, range_mins, range_maxes))
        else:
            nodes_in_range = canonical_subsets
        
        return canonical_subsets
        
        
        
    def orthogonal_range_search(self,
        range_mins:list[L], range_maxes:list[L],
        sort_on_data_after_query:bool=True) -> list[RangeTreeNode]:
        
        # Find canonical subsets from final dimension, extract and combine lists
        # of RangeTreeNodes
        canonical_subsets_in_range = \
            self._range_search_rec_helper(self._root, 1, range_mins, range_maxes)
        
        nodes_in_search_range = []
        for range_tree_node in canonical_subsets_in_range:
            nodes_in_search_range.extend(range_tree_node.get_leaves())
        
        return nodes_in_search_range