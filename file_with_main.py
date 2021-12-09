from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix
from GeneralNodes.NodeGenerationUtils import generate_FullNode_data_set
from Utils.GeneralUtils import ColIterator, StringContainer, matrix_col_subset, pretty_list
# from LayeredRangeTree.LayeredRangeTree import LayeredRangeTree
# from LayeredRangeTree.LayeredRangeTreeVisualization import visualize_layered_range_tree
from RangeTree.RangeTree import RangeTree
from RangeTree.RangeTreeVisualization import visualize_range_tree


from FractionalCascading.FCMatrix import FCMatrix

if __name__ == "__main__":
    # print(rand_unique_ints(10, 10, 20))
    n = 5
    dim = 2
    loc_min = 0
    loc_max = 100
    mins = [10, 10, 10]
    maxes = [90, 90, 90]
    
    target = 55
    
    consistent_generation=False
    full_nodes = generate_FullNode_data_set(n, dim, loc_min, loc_max, target, True, consistent_generation)

    # for f_t in full_nodes:
    #     print(str(f_t) + '\n')

    location_matrix = fullNode_list_to_SingleDimNode_matrix(full_nodes, locations_only=True)
    
    for f_t in location_matrix:
        print(f_t)
    
    # fc_matrix = FCMatrix(full_nodes)
    
        
    # print("-----------------------")
    # # for i in fc_matrix.get_fc_matrix():
    # #     print(str(len(i)) + " - " + str(i))
        
    # print(fc_matrix.fc_matrix_search(target))
    
    
    print("Nodes being loaded into the tree (locations in each dimension)")
    for i in full_nodes:
        print(i)
        print("-------")
        
    lrt = RangeTree(full_nodes, dim)

    print("First Dimension")
    print(visualize_range_tree(lrt.root()))
    print("\n===================\n")

    # print('\n\n')
    # rt.make_red_black_tree()
    # print(visualize_range_tree(rt.root()))

    print()
    print("\nSecond Dimension: ")
    print(visualize_range_tree(lrt.root().next_dimension_subtree()))
    print()
    
    
    print("\nFirst Dimension Left Subtree")
    print(visualize_range_tree(lrt.root().left_child()))
    print("\First Dimension Left Next Second Dimension Root")
    print(visualize_range_tree(lrt.root().left_child().next_dimension_subtree()))

    range_q = lrt.orthogonal_range_search(mins, maxes)
    print(f"Mins: {mins}, Maxes: {maxes}")
    print(range_q)