from GeneralNodes.FullNode import FullNode
from GeneralNodes.SingleDimNode import SingleDimNode

"""
Functions to perform an in-place merge sort on a list of SingleDimNodes. The
resulting state of the list is in ascending order based on the values of the
LocationNode in each SingleDimNode. """

def _merge(arr:list[SingleDimNode], l:int, m:int, r:int) -> None:
    """
    Merge function for merge sort. Compare the LocationNode objects in each
    SingleDimNode.

    Args:
        arr (list[SingleDimNode]): List of SingleDimNodes to be sorted.
        l (int): Leftmost index of the subset in this recursive call.
        m (int): Middle index of the subset in this recursive call.
        r (int): Rightmost index of the subset in this recursive call.  """
    
    # Sizes of two subarrays to be merged
    n1, n2 = m - l + 1, r - m
    
    # Temp arrays
    left_arr = [arr[l + i] for i in range(n1)]
    right_arr = [arr[m + 1 + j] for j in range(n2)]
    
    # Merge temp arrays
    i = j = 0
    k = l
    while i < n1 and j < n2:
        if left_arr[i].locationNode() <= right_arr[j].locationNode():
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
    

def _merge_sort(arr:list[SingleDimNode], l:int, r:int) -> None:
    """
    In-place recursive merge sort.
    
    Args:
        arr (list[SingleDimNode]): List of SingleDimNodes to be sorted
        l (int): Leftmost index of the subset in this recursive call.
        r (int): Rightmost index of the subset in this recursive call.  """
    
    if l < r:
        m = l + (r - l) // 2
        _merge_sort(arr, l, m)
        _merge_sort(arr, m + 1, r)
        _merge(arr, l, m, r)
        
    
def sort(unsorted_arr:list[SingleDimNode]) -> None:
    """
    Function to sort a list of SingleDimNodes in place by their LocationNodes
    values (ascending).
    
    Args:
        unsorted_arr (list[SingleDimNode]): List of SingleDimNodes to be sorted
    """
    if len(unsorted_arr) > 1:
        _merge_sort(unsorted_arr, 0, len(unsorted_arr) - 1)
