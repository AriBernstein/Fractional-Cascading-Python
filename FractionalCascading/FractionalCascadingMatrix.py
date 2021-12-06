from FractionalCascading.FractionalCascadingNode import FCNode, FCNodeList
from GeneralNodes.FullNode import FullNode
from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix


class FCMatrix:
    """
    In order to properly demonstrate Fractional Cascading, this matrix structure
    will be a list of linked lists with the exception of the zeroth element,
    which will be indexed so that a binary search can be performed on it.
    
    Fields:
    """
    
    def __init__(self, data_set:list[FullNode], demo:bool=True) -> None:
        
        self._n, self._k = len(data_set), data_set[0].dimensionality()
        self._input_data = fullNode_list_to_SingleDimNode_matrix(data_set)
        self._fc_matrix = [FCNodeList()] * self._k
        
    
    def _build_augmented_list(self, fc_node_list_1:FCNodeList, fc_node_list_2:FCNodeList, demo:bool=False) -> FCNodeList:
        
        last_promoted_node = None   # type: FCNode
        last_local_node = None      # type: FCNode
        
        def assign_pointers(cur_node:FCNode,
                            last_promoted_node:FCNode=last_promoted_node, 
                            last_local_node:FCNode=last_local_node) -> None:
            """
            Nested method to handle pointer assignment.

            Args:
                cur_node (FCNode): [description]
                last_promoted_node (FCNode): [description]
                last_local_node (FCNode): [description]
            """
            if cur_node.is_promoted():
                # Assign prev & next FC neighbors to closest non-promoted nodes.
                last_promoted_node = cur_node
                cur_node.set_prev_fc_neighbor(last_local_node)
                if last_local_node is not None:
                    if last_local_node.next_fc_neighbor() is None:
                        last_local_node.set_next_fc_neighbor(cur_node)
            else:
                last_local_node = cur_node
                cur_node.set_prev_fc_neighbor(last_promoted_node)
                if last_promoted_node is not None:
                    if last_promoted_node.next_fc_neighbor is None:
                        last_promoted_node.set_next_fc_neighbor(last_promoted_node)
        
        # Instantitate FCNode lists to help with promotion.
        nodes_prime = FCNodeList()
        nodes_to_promote = fc_node_list_2.get_promoted_subset()
        
        # Perform transformation
        # -> Merge elements from nodes_to_promote and fc_node_list_1 into nodes_prime
        # -> For each fc_node, assign pointers to the relevant prev & next fc nodes
        list_1_pointer, nodes_promote_pointer = \
            fc_node_list_1.head(), nodes_to_promote.head()
        
        while list_1_pointer is not None and nodes_promote_pointer is not None:
                if list_1_pointer < nodes_promote_pointer:
                    nodes_prime.append(list_1_pointer)
                    list_1_pointer = list_1_pointer.next_list_neighbor()
                else:
                    nodes_prime.append(nodes_promote_pointer)
                    nodes_promote_pointer = nodes_promote_pointer.next_list_neighbor()
                assign_pointers(nodes_prime.tail())
        
        # Take leftovers to go.
        while list_1_pointer is not None:
            nodes_prime.append(list_1_pointer)
            assign_pointers(nodes_prime.tail())
            list_1_pointer = list_1_pointer.next_list_neighbor()
        
        while nodes_promote_pointer is not None:
            nodes_prime.append(nodes_promote_pointer)
            assign_pointers(nodes_prime.tail())        
            nodes_promote_pointer = nodes_promote_pointer.next_list_neighbor()
            
        return nodes_prime
            
            
            
    def _build_fc_matrix(self, demo:bool=False):
                
        if demo:
            print("Instantiating (not-yet) FCNodes from data_set.")

        # SingleDimNodes -> FCNodes
        for i in range(self._k):
            this_list = self._fc_matrix[i]
            for j in range(self._n):
                this_list.append(
                    FCNode(base_node=self._input_data[i][j], dimension=i + 1))
        
        # Begin transformation
        if demo:
            print("Performing Fractional Cascading pre-process on FCNode matrix.")
        
        # Walk through linked lists in reverse order starting at index k-2
        # -> Always promoting from the previous demension
        for i in reversed(range(self._k - 2)):
            self._fc_matrix[i] = \
                self._build_augmented_list(
                    self._fc_matrix[i], 
                    self._fc_matrix[i - 1])
        