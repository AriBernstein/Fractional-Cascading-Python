from typing import Union

from GeneralNodes.FullNode import FullNode
from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.SingleDimNode import SingleDimNode
from Utils.CustomExceptions import InvalidDimensionalityException, \
    InvalidInputException, InvalidTypeException, MissingParameterException, \
        raise_if_different_types


################## Utils for data structures containing nodes ##################
def fullNode_list_to_SingleDimNode_matrix(
    data_set:list[FullNode]) -> list[list[SingleDimNode]]:
    """
    Given a data set represented as a list of FullNodes, convert it into a
    matrix of SingleDimNodes.
    -> Each second-dimensional list represents a single dimension.
    -> Matrix[dimension][SingleDimNode] 
    
    Args:
        data_set (list[FullNode]): K-Dimensional data set represented as a list
            of n FullNodes.
    Returns:
        list[list[SingleDimNode]]: Matrix of SingleDimNodes st each
            second-dimension list represents a given dimension. """
    
    ret_matrix = [[None for _ in range(len(data_set))] \
        for _ in range(data_set[0].dimensionality())]
    
    for i, full_node in enumerate(data_set):
        for j, single_dim_node in enumerate(full_node.to_SingleDimNode_list()):
            ret_matrix[j][i] = single_dim_node
    
    return ret_matrix


############################# Merge Sort Methods ###############################
# Functions to perform an in-place merge sort on a list of SingleDimNodes. The
# resulting state of the list is in ascending order based on the values of the
# LocationNode in each SingleDimNode.

def _merge_matrices(matrix: list[list[SingleDimNode]],
                    l:int, m:int, r:int, dim:int=None) -> None:
    """
    Merge function for merge sort. Compare the LocationNode objects in each
    SingleDimNode of dimension dim.

    Args:
        matrix (list[list[SingleDimNode]]): Matrix of SingleDimNodes w/ 
            each second-dimension list representing a given dimension.
        l (int): Leftmost index of the subset in this recursive call.
        m (int): Middle index of the subset in this recursive call.
        r (int): Rightmost index of the subset in this recursive call.    
        d (int, optional): If not None, treat arr as list of FullNode instances
            to be sorted on this field. Otherwise treat arr as list of
            SingleDimNodes. """
            
    n_dims = len(matrix)    # Number of dimensions.
    
    # Sizes of two second-dimensional subarrays to be merged
    n1, n2 = m - l + 1, r - m

    # Temp arrays
    l_subset = [[matrix[d][l + i] for i in range(n1)] for d in range(n_dims)]
    r_subset = [[matrix[d][m + 1 + j] for j in range(n2)] for d in range(n_dims)]
        
    # Merge temp arrays
    i = j = 0
    k = l
    
    while i < n1 and j < n2:
        if (l_subset[dim - 1][i].locationNode() <= r_subset[dim - 1][j].locationNode()):
            for d in range(n_dims): matrix[d][k] = l_subset[d][i]
            i += 1
        else:
            for d in range(n_dims): matrix[d][k] = r_subset[d][j]
            j += 1
        k += 1
    
    # Copy remaining elements of left_matrix or right_matrix if any
    while i < n1:
        for d in range(n_dims): matrix[d][k] = l_subset[d][i]
        k += 1
        i += 1
        
    while j < n2:
        for d in range(n_dims): matrix[d][k] = r_subset[d][j]
        k += 1
        j += 1


def _merge_lists(
    arr:Union[list[SingleDimNode], list[LocationNode], list[FullNode]], 
    l:int, m:int, r:int, mode:int, dim:int=None) -> None:
    """
    Merge function for merge sort. Compare the LocationNode objects in each
    SingleDimNode or the LocationNode objects in each FullNode at dimension dim.

    Args:
        arr (Union[list[SingleDimNode], list[FullNode]]): List of SingleDimNodes
            to be sorted on their location or list of FullNodes to be sorted on 
            a given dimension.
        l (int): Leftmost index of the subset in this recursive call.
        m (int): Middle index of the subset in this recursive call.
        r (int): Rightmost index of the subset in this recursive call.
        mode (int): Correlates with one of the three types expected by arr.
            1 -> list[SingleDimNode] or list[LocationNode]
            2 -> list[FullNode]]
        dim (int, optional): If not None, treat arr as list of FullNode 
            instances to be sorted on this field. Otherwise treat arr as list of
            SingleDimNodes. """
    
    if mode != 1 and dim == None:
        raise MissingParameterException(
            "_merge_lists", "dim", "Dimensionality parameter can only be " + \
                "left None if parameter mode == 1 (meaning that arr is a " + \
                    "list of SingleDimNodes).")
    
    # Sizes of two subarrays to be merged
    n1, n2 = m - l + 1, r - m
    
    # Temp arrays
    left_arr = [arr[l + i] for i in range(n1)]
    right_arr = [arr[m + 1 + j] for j in range(n2)]
    
    # Merge temp arrays
    i = j = 0
    k = l
    
    while i < n1 and j < n2:
        
        # Compare based on input:
        # -> Get comparison weights
        if mode == 1:
            left_weight, right_weight = \
                left_arr[i].locationNode(), right_arr[j].locationNode()
        else:
            left_weight, right_weight = \
                left_arr[i].loc(dim), right_arr[j].loc(dim)
            
        # -> Compare comparison weights
        if (left_weight <= right_weight):
            arr[k] = left_arr[i]
            i += 1
        else:
            arr[k] = right_arr[j]
            j += 1
        k += 1
    
    # Copy remaining elements of left_arr or right_arr if any
    while i < n1:
        arr[k] = left_arr[i]
        k += 1
        i += 1
        
    while j < n2:
        arr[k] = right_arr[j]
        k += 1
        j += 1
    

def _merge_sort(arr:Union[list[SingleDimNode], list[FullNode], list[list[SingleDimNode]]],
                l:int, r:int, mode:int=None, dim:int=None) -> None:
    """
    In-place recursive merge sort.
    
    Args:
        arr (Union[list[SingleDimNode], list[FullNode], 
             list[list[SingleDimNode]]):
                List of SingleDimNodes to be sorted on their location, list of
                FullNodes to be sorted on a given dimension, or a Matrix of
                SingleDimNodes to be sorted on a given dimension.
        l (int): Leftmost index of the subset in this recursive call.
        r (int): Rightmost index of the subset in this recursive call.
        mode (int): Correlates with one of the three types expected by arr.
            1 -> list[SingleDimNode]
            2 -> list[FullNode]]
            3 -> list[list[SingleDimNode]]
        dim (int, optional): If not None, treat arr as list of FullNode 
            instances to be sorted on this field. Otherwise treat arr as list of
            SingleDimNodes. """
            
    if not 1 <= mode <= 3:
        raise InvalidInputException(
            "mode", mode, "between 1 and 3 (inclusive)", _merge_sort)
    
    if dim != None: # Ensure that arr is a list of FullNodes
        raise_if_different_types(
            obj=arr[0], expected_type=FullNode, exception=InvalidTypeException, 
            params=[type(arr[0]), FullNode, "_merge_sort"])

    if l < r:
        m = l + (r - l) // 2
        _merge_sort(arr, l, m, mode, dim)
        _merge_sort(arr, m + 1, r, mode, dim)

        if mode == 1 or mode == 2:
            _merge_lists(arr, l, m, r, mode, dim)
        else:
            _merge_matrices(arr, l, m, r, dim)
            
def sort_SingleDimNode_list(unsorted_arr:list[SingleDimNode]) -> None:
    """
    Sort a list of SingleDimNodes in place by their LocationNode values.
    
    Args:
        unsorted_arr (list[SingleDimNode]): List of SingleDimNodes to be sorted
    """
    if len(unsorted_arr) > 1:
        _merge_sort(unsorted_arr, 0, len(unsorted_arr) - 1, 1)      


def sort_FullNode_list(unsorted_arr:list[FullNode], dimension:int) -> None:
    """
    Sort a list of SingleDimNodes in place by their LocationNode values.
    
    Args:
        unsorted_arr (list[FullNode]): List of SingleDimNodes to be sorted.
        dimension (int): The dimension on which to sort unsorted_arr.   """
        
    if len(unsorted_arr) > 1:
        if not 0 < dimension <= unsorted_arr[0].dimensionality():
            raise InvalidDimensionalityException(
                dimension, unsorted_arr[0].dimensionality())
        
        _merge_sort(unsorted_arr, 0, len(unsorted_arr) - 1, 2, dimension)
        

def sort_SingleDimNode_matrix(
    unsorted_matrix:list[list[SingleDimNode]], dimension:int) -> None:
    """
    Sort a matrix of SingleDimNodes in place by their LocationNode values in a 
    given dimension.
    
    Args:
        unsorted_matrix (list[list[SingleDimNode]]): Matrix of SingleDimNodes to
            be sorted on a given dimension.
        dimension (int): The dimension on which to sort unsorted_matrix.    """
    
    if not 0 < dimension <= len(unsorted_matrix):
        raise InvalidDimensionalityException(dimension, len(unsorted_matrix))
    
    if len(unsorted_matrix) >= 1 and len(unsorted_matrix[0]) > 1:
        _merge_sort(unsorted_matrix, 0, len(unsorted_matrix[0]) - 1, 3, dimension)
  