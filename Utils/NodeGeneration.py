from random import sample, shuffle

from Utils.FractionalCascadingExceptions import \
    InvalidRandUniqueIntGenerationInput
from generalNodes.DataNode import DataNode
from generalNodes.LocationNode import LocationNode
from generalNodes.FullNode import FullNode


def rand_unique_ints(
    n:int, range_min:int, range_max:int,
    insert_one:int=None, insert_two:int=None) -> list[int]:
    """
    Generate a list of random unique integers in a given range.

    Args:
        n (int): Size of the output.
        range_min (int): Smallest possible random value in output (inclusive).
        range_max (int): Largest possible random value in output (exclusive).
        insert_one, insert_two (int, optional): If not none, place in random
            location in output.

    Raises:
        InvalidRandUniqueIntGenerationInput: If input is invalid - ie n is less
            than zero or the difference between range_min and range_max is less
            than n.

    Returns:
        list[int]: list of n unique integers, each greater than or equal to
            range_min and less than range_max.  """
    
    if range_max - range_min < n or n <= 0 or range_min < 0 or range_max < 0:
        raise InvalidRandUniqueIntGenerationInput(range_min, range_max, n)
    
    ret = sample(range(range_min, range_max), n)
    
    if insert_one and len(ret) >= 1: ret[0] = insert_one
    if insert_two and len(ret) >= 2: ret[1] = insert_two
    shuffle(ret)
    
    return ret


def generate_FullNode_data_set(
    n:int, dim: int, loc_min:int, loc_max:int,
    insert_one:int=None, insert_two:int=None) -> list[FullNode]:
    
    """
    Generate list of FullNode objects with randomized data and locations.
    -> Each value is an integer unique in its own dimension (ie. data values
       will always be unique, 1st-dimension locations will always be unique,
       etc. But a data value can equal any location value, any location value 
       can equal any location value in another dimension, etc.).

    Args:
        n (int): Number of FullNodes in output.
        dim (int): Number of locations in each FullNode in output.
        loc_min (int): The smallest integer representing any FullNode's data or
            location value (inclusive). 
        loc_max (int): The largest integer representing any FullNode's data or
            location value (exclusive).
        insert_one, insert_two (int, optional): If not none, place in a random
            location in output.

    Returns:
        list[FullNode]: List of n FullNode objects with randomized integer data
            and location values, all unique in their own dimensions and between
            loc_min and loc_max.    """
            
    dim += 1    # Account for zero-indexing
    
    node_data_matrix = [    # dim + 1 -> extra integer for data
        rand_unique_ints(n, loc_min, loc_max, insert_one, insert_two)
    for _ in range(dim + 1)]
    
    node_list = []

    # Iterate through node_data_matrix column-wise to create FullNodes one at a
    # time. Use 0th element of each column for data, following for locations.
    # Consider parallelization? 
    for i in range(n):
        loc_dict = {}
        for j in range(1, dim + 1):
            loc_dict[j] = LocationNode(node_data_matrix[j][i], j)
        node_list.append(FullNode(DataNode(node_data_matrix[j][0]), loc_dict))
                
    return node_list
