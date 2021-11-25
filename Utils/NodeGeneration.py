import random

from Utils.FractionalCascadingExceptions import InvalidRanUniqueIntGenerationInput

def rand_unique_ints_in_range(n:int, range_min:int, range_max:int) -> list[int]:
    if range_max - range_min < n:
        raise InvalidRanUniqueIntGenerationInput(range_min, range_max, n)
    
    return random.sample(range(range_min, range_max), n)

# def get_coord_node_list(n:int, insertData:int, )