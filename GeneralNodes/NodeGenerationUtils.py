from random import sample, shuffle

from Utils.CustomExceptions import InvalidRandUniqueIntGenerationInput
from GeneralNodes.DataNode import DataNode
from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.FullNode import FullNode


def rand_unique_ints(
    n:int, range_min:int, range_max:int,
    insert_val:int=None, rand_insert_loc:bool=False) -> list[int]:
    """
    Generate a list of random unique integers in a given range.

    Args:
        n (int): Size of the output.
        range_min (int): Smallest possible random value in output (inclusive).
        range_max (int): Largest possible random value in output (exclusive).
        insert_val( int, optional): If not none, place inject into output.
        rand_insert_loc (bool): If true, place insert_val into random location
            in output list. Otherwise (default), place at middle index. This
            way, if used to create a FullNode, its data and location values will
            be the same integer.

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
    
    
    if insert_val and rand_insert_loc:
        ret[len(ret) // 2] = insert_val
    
    shuffle(ret)
    
    if insert_val and not rand_insert_loc:
        ret[len(ret) // 2] = insert_val
    
    return ret


def generate_FullNode_data_set(
    n:int, dim: int, loc_min:int, loc_max:int, insert_one:int=None,
    insert_two:int=None, xyz_label:bool=True) -> list[FullNode]:
    
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
        xyz_label (bool): If true, and dim is <= 3, then label dimension 1 as 
            'x', dimension 2 as 'y', dimension 3 as 'z' (given that they exist).

    Returns:
        list[FullNode]: List of n FullNode objects with randomized integer data
            and location values, all unique in their own dimensions and between
            loc_min and loc_max.    """
    xyz_dict = {1:'x', 2: 'y', 3: 'z'}
    
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
            d_label = xyz_dict[j] if dim <= 3 and xyz_label else None
            loc_dict[j] = LocationNode(node_data_matrix[j][i], j, d_label)
        node_list.append(FullNode(DataNode(node_data_matrix[0][i]), loc_dict))
                
    return node_list
