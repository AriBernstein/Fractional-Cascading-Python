from FractionalCascading.FCNodeStructures import FCNode, FCList
from GeneralNodes.FullNode import FullNode
from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix, search_nodes
from Utils.CustomExceptions import NodeNotFoundInCorrectDimension
from Utils.TypeUtils import L


class FCMatrix:
    """
    In order to properly demonstrate Fractional Cascading, this matrix structure
    will be a list of linked lists with the exception of the zeroth element,
    which will be indexed so that a binary search can be performed on it.
    
    Fields:
        _n (int): number of nodes in each dimension.
        
        _k (int): dimensionality
        
        _input_data (list[list[LocationNode]]): 
            matrix of LocationNode objects to demonstrate traversal.
            
        _fc_matrix (list[FCList]): 
            The matrix created via fractional cascading. It is a list of linked
            lists of FCNodes.   
            
        _demo (bool): If true, have methods print progress reports. 
        
        _n_limit (int): 
            As this data structure exists to demonstrate performance, this is 
            for cases in which we don't need to actually store the data we find,
            just record the query time. Arbitrarily defaults to 100 """
    
    def __init__(self, data_set:list[FullNode], n_limit:int=100, demo:bool=True) -> None:
        self._n, self._k = len(data_set), data_set[0].dimensionality()
        self._input_data = fullNode_list_to_SingleDimNode_matrix(data_set, True)
        self._fc_matrix = [FCList() for _ in range(self._k)]
        self._n_limit = n_limit
        self._demo = demo
        
        # Setup after parameters have been stored.
        self._build_fractional_cascading_matrix()
        self._first_dim_list = self._fc_matrix[0].to_list()
        
        
    def get_fc_matrix(self) -> list[FCList]:
        return self._fc_matrix
    
    def _get_fc_list_head(self, dimension:int) -> FCNode:
        return self._fc_matrix[dimension - 1].head()
    
    def _get_fc_list_tail(self, dimension:int) -> FCNode:
        return self._fc_matrix[dimension - 1].tail()
        
    
    ############################### Query Methods ##############################
    def target_node(self, current_node: FCNode, target_data:L, target_dim:int) -> bool:
        return current_node is not None and \
            current_node.loc() == target_data and \
                current_node.dim() == target_dim == current_node.base_dim()
    
    def fc_matrix_search(self, x:L) -> dict[int, FCNode]:
        """
        Find FCNodes located at x (or its successor) in each dimension.

        Args: x (L): Location for which we are searching in each dimension.

        Returns: dict[int, FCNode]: key -> dimension
                                    pair -> associated FCNode   """
                                    
        data_locations = {} # type: dict[int, tuple[FCNode, int]]
        target_dim = 1
        
        # Binary search for x in first dimension:
        # -> First level must be an indexed list from a binary search.
        #    (Remaining levels are linked lists.)
        cur_node, _ = search_nodes(self._first_dim_list, x)

        # Walk through promoted node pointers, from list 2' through list (k-1)'
        while target_dim < self._k:
            
            # Ensure x_obj is in the correct dimension. If not check neighbors
            if cur_node.base_dim() != target_dim:

                # Because cur_node is not originally from the current dimension,
                # prev_fc_node and nex_fc_node are guaranteed to be.
                prev_fc_node = cur_node.prev_foreign_neighbor()
                next_fc_node = cur_node.next_foreign_neighbor()
                if self.target_node(prev_fc_node, x, target_dim):
                    cur_node = prev_fc_node

                    print(cur_node)
                    
                # These cases are for when we are looking for a value expected
                # in each dimension st. seccessors and predecessors are
                # irrelevant. Otherwise just return next_fc_node st. that it 
                # defaults to the successor of the target node.
                ################################################################
                elif self.target_node(next_fc_node, x, target_dim):
                    cur_node = next_fc_node

                else:
                    raise NodeNotFoundInCorrectDimension(target_dim)
                ################################################################
                # cur_node = next_fc_node
                ################################################################
                
            if self._k < self._n_limit:
                data_locations[target_dim] = cur_node
            
            # cur_node is now the correct version of x (initially of the the 
            # current dimension). Now, in order to find the version of x
            # local to the prior dimension, we must use the range bounded by its 
            # (guaranteed foreign) prev_foreign_neighbor and 
            # prev_foreign_neighbor. If either doesn't exist, use the head/tail 
            # of the linked lists of the prior dimension.
            target_dim += 1
            found = False
            
            low_range = self._get_fc_list_head(target_dim) if \
                cur_node.prev_foreign_neighbor() is None else \
                    cur_node.prev_foreign_neighbor().prev_dim_variant()
                    
            high_range = self._get_fc_list_tail(target_dim) if \
                cur_node.next_foreign_neighbor() is None else \
                    cur_node.next_foreign_neighbor().prev_dim_variant()
                    
            while low_range.loc() <= high_range.loc():
                if self.target_node(low_range, x, target_dim):
                    cur_node = low_range
                    found = True
                    break
                low_range = low_range.next_list_neighbor()
                
            if not found:
                raise NodeNotFoundInCorrectDimension(target_dim)
            

        return data_locations
       
            
    def trivial_solution(self, x:int) -> dict[int, tuple[LocationNode, int]]:
        """
        The trivial query solution by which to compare Fractional Cascading.
        -> k log(n) searchs in the _input_data matrix.
        
        Args: x (int): Location for which wto search in each dimension.

        Returns: dict[int, tuple[LocationNode, int]]: 
            key -> dimension, pair -> (LocationNode of x, index of x in input)
        """
        ret_dict = {}
        for i in range(self._k):
            x_node, x_index = search_nodes(self._input_data[i], x)
            
            # Memory issues, this is a stupid amount of space especially when 
            # we're only trying to record function timing
            if self._k < self._n_limit: ret_dict[i + 1] = (x_node, x_index)
        return ret_dict
        
    
    ########################### Matrix Setup Methods ###########################
    def _build_fractional_cascading_matrix(self):
        """
        1. Convert given nodes into FCNodes prior to promotion/augmentation.
           Note: this conversion is from an indexed list to a linked list.
        
        2. Walking from the highest dimension to the lowest, merge elements from
           the augmented list of the prior dimension and elements of the current 
           dimension into the augmented list of the current dimension.  """
        
        if self._demo: 
            print("Converting input into (not-yet-promoted) FCNodes.")

        # 1. SingleDimNodes -> FCNodes
        for i in range(self._k):
            this_FCList = self._fc_matrix[i]
            for j in range(self._n):
                this_FCList.append(
                    FCNode(base_node=self._input_data[i][j], dimension=i+1))
        
        # 2. Walk through linked lists in reverse order starting at index k-2
        # -> (TBC - walking through actual linked lists in order but through 
        #     list containing linked lists in reverse order.)
        # -> Always promoting from the previous demension
        if self._demo: print("Pre-processing FCNodes into matrix.")
        for i in reversed(range(self._k - 1)):
            self._fc_matrix[i] = \
                self._build_augmented_list(self._fc_matrix[i],
                                           self._fc_matrix[i + 1])
                
    
    def _build_augmented_list(self, node_list_i:FCList, node_list_j:FCList) -> FCList:
        """
        Merge all elements in node_list_i and half in node_list_j into a new 
        FCList to be added to the FrationcalCascadingMatrix.

        Args:
            node_list_i (FCList): 
                Represents values from dimension i, all of which will be merged 
                into the FCList representing the level of the Frationcal 
                Cascading Matrix being constructed, i' . Must be ordered by the
                ith dimension.
            
            node_list_j (FCList):
                Represents values from dimension (i - 1)', half of which will be 
                merged into the FCList representing the level of the Frationcal 
                Cascading Matrix being constructed, i' .
                
        Returns: FCList: 
            Augmented list i' containing all values from input dimension i and
            half of the values from dimension (i-1)'    """
            
        _last_promoted_node_stack = []  # type: list[FCNode]
        _last_local_node_stack = []     # type: list[FCNode]
        def _assign_pointers(cur_node:FCNode) -> None:
            """
            Nested method to assign pointers between promoted and local nodes,
            and vice versa.

            Args: cur_node (FCNode): 
                FCNode to which we should assign neighbors originally of other 
                dimensions.  
            """
            nonlocal _last_promoted_node_stack
            nonlocal _last_local_node_stack
            
            if cur_node.is_promoted():
                # Assign prev & next FC neighbors to closest local nodes.
                _last_promoted_node_stack.append(cur_node)
                
                last_local_node = _last_local_node_stack.pop() if \
                    len(_last_local_node_stack) > 0 else None
                
                cur_node.set_prev_f_neighbor(last_local_node)
                while last_local_node is not None:
                    # Assign next pointers until _last_local_node_stack is empty.
                    if last_local_node.next_foreign_neighbor() is None:
                        last_local_node.set_next_f_neighbor(cur_node)
                        
                    last_local_node = _last_local_node_stack.pop() if \
                        len(_last_local_node_stack) > 0 else None
                        
            elif cur_node.is_local():
                # Assign prev & next FC neighbors to closest promoted nodes.
                _last_local_node_stack.append(cur_node)
                
                last_promoted_node = _last_promoted_node_stack.pop() if \
                    len(_last_promoted_node_stack) > 0 else None
                
                cur_node.set_prev_f_neighbor(last_promoted_node)
                while last_promoted_node is not None:
                    # Assign next pointers until _last_promoted_node_stack is empty.
                    if last_promoted_node.next_foreign_neighbor() is None:
                        last_promoted_node.set_next_f_neighbor(cur_node)
                        
                    last_promoted_node = _last_promoted_node_stack.pop() if \
                        len(_last_promoted_node_stack) > 0 else None
            else:
                raise Exception("Well this shouldn't be happening :/")
        
        if self._demo:
            dim = node_list_i.head().dim()
            print(f"Promoting nodes from dimension {dim + 1} into {dim}.")
        
        # Instantitate FCNode lists to help with promotion.
        nodes_i_prime = FCList()
        nodes_to_promote = node_list_j.get_promoted_subset()
        
        # Perform transformation
        list_i_pointer = node_list_i.head()
        promoting_pointer = nodes_to_promote.head()
        
        # -> Merge elements from nodes_to_promote and node_list_i into nodes_i_prime
        # -> For each FCNode, assign pointers to all relevant foreign/local FCNodes
        while list_i_pointer is not None and promoting_pointer is not None:
            if list_i_pointer <= promoting_pointer:
                nodes_i_prime.append(list_i_pointer)
                list_i_pointer = list_i_pointer.next_list_neighbor()
            elif list_i_pointer > promoting_pointer:
                nodes_i_prime.append(promoting_pointer)
                promoting_pointer = promoting_pointer.next_list_neighbor()
            else:
                raise Exception("Well this shouldn't be happening :/")
            
            # _assign_pointers(nodes_i_prime.tail())
        
        # Take leftovers to go.
        while list_i_pointer is not None:
            nodes_i_prime.append(list_i_pointer)
            # _assign_pointers(nodes_i_prime.tail())
            list_i_pointer = list_i_pointer.next_list_neighbor()
        
        while promoting_pointer is not None:
            nodes_i_prime.append(promoting_pointer)
            # _assign_pointers(nodes_i_prime.tail())        
            promoting_pointer = promoting_pointer.next_list_neighbor()
            
        augmented_pointer = nodes_i_prime.head()
        while augmented_pointer is not None:
            _assign_pointers(augmented_pointer)
            augmented_pointer = augmented_pointer.next_list_neighbor()
            
        return nodes_i_prime