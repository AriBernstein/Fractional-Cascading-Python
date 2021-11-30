from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix, \
    sort_SingleDimNode_list, sort_FullNode_list, sort_SingleDimNode_matrix
from GeneralNodes.NodeGenerationUtils import generate_FullNode_data_set
from Utils.GeneralUtils import ColIterator, StringContainer, matrix_subset, pretty_list
from RangeTree.RangeTree import RangeTree
from RangeTree.RangeTreeVisualization import visualize_range_tree

if __name__ == "__main__":
    # print(rand_unique_ints(10, 10, 20))
    n = 5
    dim = 3
    loc_min = 0
    loc_max = 100
    mins = [25, 25, 25]
    maxes = [75, 75, 75]
    
    full_nodes = generate_FullNode_data_set(n, dim, loc_min, loc_max, 50)
    
    for i in full_nodes:
        print(i)
    
    rt = RangeTree(full_nodes, dim)
    target = 50
    print(f"Target: {target}")
    
    print(visualize_range_tree(rt))
    
    print(rt.query(target))