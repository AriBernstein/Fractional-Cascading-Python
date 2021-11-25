
from GeneralNodes.SingleDimNode import SingleDimNode


def _merge(arr:list[SingleDimNode], l:int, m:int, r:int) -> None:
    
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
            k += 1
        else:
            arr[k] = right_arr[j]
            k += 1
        i += 1
    
    # Copy remaining elements of left_arr or right_arr if any
    while i < n1:
        arr[k] = left_arr[i]
        k += 1
        i += 1
        
    while j < n2:
        arr[k] = right_arr[j]
        k += 1
        i += 1
    

def _merge_sort(arr:list[SingleDimNode], l:int, r:int) -> None:
    
    if l < r:
        m = l + (r - l) // 2
        _merge_sort(arr, l, m)
        _merge_sort(arr, m + 1, r)
        _merge(arr, l, m, r)
        
    
def sort(arr:list[SingleDimNode]) -> None:
    if len(arr) <= 1:
        _merge_sort(arr, 0, len(arr) - 1)
        