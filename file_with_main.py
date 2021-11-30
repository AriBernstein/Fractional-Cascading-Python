from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix, \
    sort_SingleDimNode_list, sort_FullNode_list, sort_SingleDimNode_matrix
from GeneralNodes.NodeGenerationUtils import generate_FullNode_data_set
from Utils.GeneralUtils import ColIterator, StringContainer, matrix_subset, pretty_list
from RangeTree.RangeTree import RangeTree
from RangeTree.RangeTreeVisualization import visualize_range_tree

if __name__ == "__main__":
    # print(rand_unique_ints(10, 10, 20))
    n = 11
    dim = 1
    loc_min = 0
    loc_max = 100
    mins = [20]
    maxes = [80]
    
    target = None
    consistent_generation=True
    full_nodes = generate_FullNode_data_set(n, dim, loc_min, loc_max, target, False, consistent_generation)


    for i in full_nodes:
        print(i)
    
    rt = RangeTree(full_nodes, dim)
    print()
    # print(visualize_range_tree(rt.root().left_child()))
    print(visualize_range_tree(rt.root()))
    print()

    
    
    
    range_q = rt.orthogonal_range_search(mins, maxes)
    print(f"Mins: {mins}, Maxes: {maxes}")
    for i in range_q:
        print(i.all_locations_str() + "\n")