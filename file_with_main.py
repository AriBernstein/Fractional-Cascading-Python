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
    mins = [10, 10, 10]
    maxes = [90, 90, 90]
    
    target = None
    consistent_generation=False
    full_nodes = generate_FullNode_data_set(n, dim, loc_min, loc_max, target, False, consistent_generation)


    for i in full_nodes:
        print(i)
    print()

    
    rt = RangeTree(full_nodes, dim)
    print("First Dimension")
    print(visualize_range_tree(rt.root()))
    print()
    print("\nSecond Dimension: ")
    print(visualize_range_tree(rt.root().next_dimension_subtree()))
    print()
    print("\nThird Dimension: ")
    print(visualize_range_tree(rt.root().next_dimension_subtree().next_dimension_subtree()))
    print()
    print("-----------------------------")
    print("\nFirst Dimension")
    print(visualize_range_tree(rt.root()))
    print("\nFirst Dimension Left Subtree")
    print(visualize_range_tree(rt.root().left_child()))
    print("\nSecond Dimension Left Subtree")
    print(visualize_range_tree(rt.root().left_child()))

    range_q = rt.orthogonal_range_search(mins, maxes)
    print(f"Mins: {mins}, Maxes: {maxes}")
    print(range_q)