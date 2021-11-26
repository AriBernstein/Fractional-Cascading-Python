from GeneralNodes.FullNode import FullNode
from Utils.NodeGeneration import generate_FullNode_data_set
from Utils.SortNodes import sort

if __name__ == "__main__":
    # print(rand_unique_ints(10, 10, 20))
    n = 10
    dim = 3
    loc_min = 0
    loc_max = 100
    
    fullNodes = generate_FullNode_data_set(n, dim, loc_min, loc_max)
    for x in fullNodes:
        print(x)
    
    # dim_1_list = [fn.get_SingleDimNode(1) for fn in fullNodes]
    
    # for i in fullNodes:
    #     print(i)
        
    # print ("------------")
    
    # for i in dim_1_list:
    #     print(i)
    
    # print ("------------")
        
    # sort(dim_1_list)
    # for i in dim_1_list:
    #     print(i)
        
    print ("------------")
    