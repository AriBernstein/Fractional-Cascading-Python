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
    dim_1_list, dim_2_list, dim_3_list = [], [], []
    for fn in fullNodes:
        n1, n2, n3 = fn.get_SingleDimNode_list()
        dim_1_list.append(n1)
        dim_2_list.append(n2)
        dim_3_list.append(n3)
    
    
    for i in fullNodes:
        print(i)
        
    print ("------------")
    
    for i in dim_1_list:
        print(i)
    
    print ("------------")
        
    sort(dim_1_list)
    for i in dim_1_list:
        print(i)
        