from random import sample, shuffle

from Utils.FractionalCascadingExceptions import InvalidRanUniqueIntGenerationInput
from GeneralNodes.DataNode import DataNode
from GeneralNodes.LocationNode import LocationNode
from GeneralNodes.Node import Node

def rand_unique_ints_in_range(
    n:int, range_min:int, range_max:int,
    insert_val_one:int=None, insert_val_two:int=None) -> list[int]:
    
    if range_max - range_min < n or n <= 0:
        raise InvalidRanUniqueIntGenerationInput(range_min, range_max, n)
    
    ret = sample(range(range_min, range_max), n)
    
    if insert_val_one and len(ret) >= 1: ret[0] = insert_val_one
    if insert_val_two and len(ret) >= 2: ret[1] = insert_val_two
    shuffle(ret)
    
    return ret

def get_node_list(n:int, dimensionality: int, loc_min:int, loc_max:int,
                  insert_val_one:int, insert_val_two:int) -> list[Node]:
    
    node_data_matrix = [
        rand_unique_ints_in_range(
            n, loc_min, loc_max, insert_val_one, insert_val_two)
        for _ in range(dimensionality + 1)]
    
    node_list = []
    
    for node_data_set in node_data_matrix:
        # Use 0th element for data, following for location
        loc_dict = {}
        for i in range(1, len(node_data_set)):
            loc_dict[i] = LocationNode(node_data_set[i], i)
        node_list.append(Node(DataNode(node_data_set[0]), loc_dict))     
        
    return node_list
    