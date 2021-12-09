from GeneralNodes.DataNode import DataNode
from GeneralNodes.FullNode import FullNode
from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix, \
    sort_SingleDimNode_list, sort_SingleDimNode_matrix
from GeneralNodes.SingleDimNode import SingleDimNode
from LayeredRangeTree.LayeredRangeTreeNode import LayeredRangeTreeNode, \
    RangeTreeNode, LayeredRangeTreeSubNode
from Utils.CustomExceptions import InvalidDimensionalityException
from Utils.GeneralUtils import matrix_col_subset
from Utils.TypeUtils import L

LEFT, RIGHT = 0, 1

"""
Implementation is build on top of regular Range Trees. This just checks for
cases related to constructing the final dimension.  """

class LayeredRangeTree:
    
    """
    Class to represent Range Tree. Contains a pointer to the root RangeTreeNode,
    as well as construction and querying functionality.
    
    Fields:
        _dimensionality (int): 
            Dimensionality of the data set represented by this Range Tree.
        
        _root (RangeTreeNode): the root node of the Range Tree. """
    
    def __init__(self, data_set:list[FullNode], dimensionality:int) -> None:
        """
        Args:
            data_set (list[FullNode]): 
                List of FullNode instances to be preprocessed into Range Tree.
            
            dimensionality (int): The Dimensionality of data_set. """
        
        if len(data_set) == 0:
            raise Exception("data_set is empty. Cannot construct RangeTree.")
        if dimensionality < 1:
            raise Exception(f"dimensionality value ({dimensionality}) must " + \
                "be greater than 1.")
        
        self._dimensionality = dimensionality
        converted_data_set = fullNode_list_to_SingleDimNode_matrix(data_set)
        
        # Build Layered Range Tree with all but the final dimension.
        self._root = self._build_range_tree(converted_data_set)
        
        # TODO: get rid of this - figure out why it's necessary
        self._assign_all_parents()
    
        
    def root(self):
        return self._root
    
    
    def root_by_dimension(self, dimension:int) -> RangeTreeNode:
        """
        Args:
            dimension (int): The dimension of the RangeTreeNode to return.

        Returns: RangeTreeNode:
            Highest-level RangeTreeNode at dimension in Range Tree. """
                
        if not 1 <= dimension <= self._dimensionality:
            raise InvalidDimensionalityException(dimension, self._dimensionality)
        cur_root = self._root
        while cur_root.dimension() < dimension:
            cur_root = cur_root.next_dimension_subtree()
        return cur_root    
    
    
    def _build_layered_rt_component(
        self, cur_subset:list[list[SingleDimNode]]) -> LayeredRangeTreeNode:
        """
        Given the final two dimensions of a Layered Range Tree, x & y, and a
        subset of nodes associated with the range of x, construct a 
        LayeredRangeTreeNode on its y values.

        Args: cur_subset (list[list[SingleDimNode]]):
            Subset of the input data set in accordance with the range of the
            x-dimensional location values.

        Returns: LayeredRangeTreeNode:
            Containing list of LayeredRangeTreeSubNode instances, associated 
            with and sorted by y location values, all of which are in the range 
            of the range of x-dimensional location values.  """
        
        final_dim = cur_subset[-1]
        
        sub_node = [    # SDN -> SingleDimNode
            LayeredRangeTreeSubNode(final_dim[sdn])  for sdn in final_dim
        ]   # type: list[LayeredRangeTreeSubNode]
    
    
    def _build_range_tree(self, 
        cur_subset:list[list[SingleDimNode]], cur_dim:int=1) -> RangeTreeNode:
        """
        Method to construct the Range Tree.

        Args:
            cur_subset (list[list[SingleDimNode]]): 
                Subset of SingleDimNodes matrix to preprocess into Range Tree.
                
            cur_dim (int, optional): 
                The current dimension of the RangeTreeNode being constructed. 

        Returns: RangeTreeNode: The root of the RangeTree.   """
        
        # Start by considering whether or not we are in the second to last
        # dimension
        second_to_last_dim = False
        if cur_dim == self._dimensionality - 2:
            second_to_last_dim = True
        
        # If not second-to-last dimension, construct tree in higher dimensions.
        next_dim_subtree = None
        if not second_to_last_dim:
            next_dim_subtree = self._build_range_tree(cur_subset, cur_dim + 1)
        
        # Base case - check if leaf
        if len(cur_subset[cur_dim - 1]) == 1:
            return RangeTreeNode(node_data=cur_subset[cur_dim - 1][0],
                                 next_dimension_subtree=next_dim_subtree)
        
        # Always sort
        sort_SingleDimNode_matrix(cur_subset, cur_dim)
        
        # If second to last dimension, also sort on Y dimension such that it can
        # be subsetted in accordance with x.
        
        l_index = 0
        r_index = len(cur_subset[cur_dim - 1]) - 1
        m_index = r_index // 2
        
        l_subset = matrix_col_subset(cur_subset, l_index, m_index)
        r_subset = matrix_col_subset(cur_subset, m_index + 1, r_index)
        
        # If second-to-last dimension, construct final dimension 
        # LayeredRangeTree structures based off of X partition.
        # if second_to_last_dim:
            
        
        this_root = RangeTreeNode(
            node_data=l_subset[cur_dim - 1][-1],
            left_child=self._build_range_tree(l_subset, cur_dim),
            right_child=self._build_range_tree(r_subset, cur_dim),
            next_dimension_subtree=next_dim_subtree)
      
        return this_root
    
    
    def _query(self, target:L, cur_root:RangeTreeNode,
               path:list[tuple[int, RangeTreeNode]]=None,
               predecessor:bool=False) -> RangeTreeNode:
        """
        Search RangeTree for a specific Node or its successor. 
        
        Args:
            target (L): 
                Location value of the RangeTreeNode for which we are searching.
            
            cur_root (RangeTreeNode): 
                Root of the current subtree in which we are searching.
                
            path (list[tuple[int, RangeTreeNode]], optional): 
                A list of tuples with (int, RangeTreeNode) denoting the path 
                taken by this search recursively through the RangeTree.
                    int = 0 -> LEFT, int = 1 -> RIGHT
            
            predecessor (bool): 
                If True, and no node exists at L, return the node in the 
                preceding location. Otherwise, return successor (default).

        Returns:
            RangeTreeNode: The RangeTreeNode at target location, or that at its 
                preceding or succeeding target location.    """
                
        def handle_left() -> RangeTreeNode:
            if path != None: path.append((LEFT, cur_root))
            return self._query(target, cur_root.left_child(), path)
        
        def handle_right() -> RangeTreeNode:
            if path != None: path.append((RIGHT, cur_root))
            return self._query(target, cur_root.right_child(), path)
        
        if cur_root.is_leaf():
            if path != None: path.append((-1, cur_root))
            return cur_root
        elif predecessor:
            return handle_right() \
                if target >= cur_root.get_location() else handle_left()
        else:
            return handle_left() \
                if target <= cur_root.get_location() else handle_right()
    
    
    def query_range_tree(self, target:L, search_dimension:int=1,
                         print_result:bool=False,
                         predecessor:bool=False) -> list[SingleDimNode]:
        """
        Search RangeTree for a Node at a specific location or its successor (or
        predecessor if the option is enabled) should none exist.

        Args:
            target (L): 
                The Location value of the RangeTreeNode for which we are searching.
            
            search_dimension (int):
                The demension in which to search for nodes at this location. 
                Defaults to 1.
            
            print_result (bool): If True, print search result. Default False.
            
            predecessor (bool): 
                If True, and no node exists at L, return the node in the 
                preceding location. Otherwise, return successor (default).

        Returns: list[SingleDimNode]:
            A list of SingleDimNodes, each representing the data's location in 
            all dimensions including and following search_dimension.    """
                
        if not 1 <= search_dimension <= self._dimensionality:
            raise InvalidDimensionalityException(search_dimension,
                                                 self._dimensionality)
        
        cur_root = self._root   # Walk to search_dimension
        while cur_root.dimension() < search_dimension:
            cur_root = cur_root.next_dimension_subtree()
        
        ret_node = self._query(target, cur_root, predecessor=predecessor)
                
        if print_result:
            print(f"Search result for {str(target)}:\n" + \
                str(ret_node.get_single_dim_node()))
            
        ret_list = []
        while ret_node is not None:
            ret_list.append(ret_node.get_single_dim_node())
            ret_node = ret_node.next_dimension_subtree()
        
        return ret_list
    
    
    def _search_rec(
        self, cur_root:RangeTreeNode, cur_dim:int, 
        range_mins:list[type[L]], range_maxes:list[type[L]]) -> list[RangeTreeNode]:

        """
        Recursively search RangeTree to poopulate a list of RangeTreeNodes
        representing canonical subsets of the Range Tree.
        
        Args:
            cur_root (RangeTreeNode): The subtree of the current recursive call.
            
            cur_dim (int): Dimension of the subtree of the current recursive call.
            
            range_mins, range_maxes (list[type[L]]):
                Lists of L (generic location objects), each representing the low 
                and high ranges of the search for the demension correlated with 
                each list index plus one (exclusive max).
                
        Returns: list[RangeTreeNodes]: 
            List of RangeTreeNodes representing canonical subsets of this Range 
            Tree containing the data between range_mins & range_maxes.  """
        
        range_min = range_mins[cur_dim - 1]
        range_max = range_maxes[cur_dim - 1] 
        
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
        
        # Find index index at which range_min_path & range_max_path diverges.
        if paths_diverge:
            shortest_path_len = min(len(range_min_path), len(range_max_path))
            for i in range(shortest_path_len):
                min_direction, min_node = range_min_path[i]
                max_direction, max_node = range_max_path[i]
                
                if min_node.is_leaf() or max_node.is_leaf():
                    break
                elif min_direction == max_direction:
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
                    direction, subtree = range_max_path[i]
                    
                    if subtree.is_leaf() and in_range(subtree.get_location()):
                        canonical_subsets.append(subtree)
                    elif direction == RIGHT and subtree.left_child() is not None:
                        canonical_subsets.append(subtree.left_child())                    

        
        # Handle case where no nodes are in range:
        if len(canonical_subsets) == 1 and canonical_subsets[0].is_leaf():
            if not in_range(canonical_subsets[0].get_location()):
                canonical_subsets = []
        
        # Recurse on next dimension on each canonical subset
        # -> nodes_in_range should contain the RangeTreeNodes that make up the
        #    canonical subsets of the final dimension.
        nodes_in_range = []
        if cur_dim < self._dimensionality:
            for canonical_root in canonical_subsets:
                nodes_in_range.extend(
                    self._search_rec(
                        canonical_root.next_dimension_subtree(),
                        cur_dim + 1, range_mins, range_maxes))
        else:
            nodes_in_range = canonical_subsets
        
        return nodes_in_range
        
        
    def orthogonal_range_search(self,
        range_mins:list[L], range_maxes:list[L],
        sort_on_data_after_query:bool=True) -> list[DataNode]:
        """
        Perform an orthogonal range search on this RangeTree instance.

        Args:
            range_mins, range_maxes (list[type[L]]): 
                List of L (generic location objects), each representing the low
                and high ranges of the search for the demension correlated with 
                each list index plus one.
            
            sort_on_data_after_query (bool, optional): 
                If true (default), sort results of search on their data fields.
                
        Returns: list[DataNode]: 
            List of DataNode instances located between the locations specified 
            in range_mins and range_maxes.  """
        
        if len(range_mins) != len(range_maxes):
            raise Exception("orthogonal_range_search method parameters " + \
                "range_mins and range_maxes must be of equal length.")
        
        if len(range_mins) < self._dimensionality:
            raise Exception("orthogonal_range_search method parameters " + \
                "range_mins and range_maxes must be of length greater than " + \
                    "or equal to the dimensionality of this Range Tree.")
        
        # Find canonical subsets from final dimension, extract and combine lists
        # of RangeTreeNodes
        canonical_subsets_in_range = \
            self._search_rec(self._root, 1, range_mins, range_maxes)
        
        nodes_in_search_range = []  # type:list[SingleDimNode]
        for range_tree_node in canonical_subsets_in_range:
            nodes_in_search_range.extend(range_tree_node.get_leaves(mode=2))
            
        if sort_on_data_after_query:
            sort_SingleDimNode_list(nodes_in_search_range, True)
        
        return [sd_node.dataNode() for sd_node in nodes_in_search_range]
    
    
    def _assign_all_parents(self, cur_root:RangeTreeNode=None) -> None:
        """
        TODO:  This method should not be necessary.
        All parents should be assigned as the tree is created.
        """
        cur_root = self._root if cur_root is None else cur_root
        
        if cur_root.left_child() is not None:
            cur_root.left_child().set_parent(cur_root)
            self._assign_all_parents(cur_root.left_child())
            
        if cur_root.right_child() is not None:
            cur_root.right_child().set_parent(cur_root)
            self._assign_all_parents(cur_root.right_child())
    
    
    def _handle_final_dimension(self, final_dim_nodes:list[SingleDimNode]) -> LayeredRangeTreeNode:
        pass