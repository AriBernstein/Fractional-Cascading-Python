from Utils.NodeGeneration import rand_unique_ints, generate_FullNode_data_set
from Utils.PrettyPrintingUtils import pretty_dict, pretty_list

if __name__ == "__main__":
    # print(rand_unique_ints(10, 10, 20))
    n = 10
    dim = 3
    loc_min = 0
    loc_max = 100
    
    x = generate_FullNode_data_set(n, dim, loc_min, loc_max)
    
    for i in x:
        print(i)