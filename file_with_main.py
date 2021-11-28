from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix, sort_SingleDimNode_list, sort_FullNode_list, sort_SingleDimNode_matrix
from GeneralNodes.NodeGenerationUtils import generate_FullNode_data_set


if __name__ == "__main__":
    # print(rand_unique_ints(10, 10, 20))
    n = 10
    dim = 3
    loc_min = 0
    loc_max = 100
    
    fullNodes = generate_FullNode_data_set(n, dim, loc_min, loc_max)
    # for i in fullNodes:
    #     print(i)
        
    # sort_FullNode_list(fullNodes, 3)
    # print("------------------\n\n\n")
    # for i in fullNodes:
    #     print(i)
        
    
    # dim_1_list, dim_2_list, dim_3_list = [], [], []
    # for fn in fullNodes:
    #     n1, n2, n3 = fn.to_SingleDimNode_list()
    #     dim_1_list.append(n1)
    #     dim_2_list.append(n2)
    #     dim_3_list.append(n3)
    
    
    # for i in fullNodes:
    #     print(i)
        
    # print ("------------")
    
    # for i in dim_2_list:
    #     print(i)
    # print ("------------")

    # sort_SingleDimNode_list(dim_2_list)
        
    # for i in dim_2_list:
    #     print(i)
    
    # print ("------------")
        
    # sort(dim_1_list)
    # for i in dim_1_list:
    #     print(i)
        
    # print ("------------")
    
    node_matrix = fullNode_list_to_SingleDimNode_matrix(fullNodes)
    for i in node_matrix:
        print(i)
        
    sort_SingleDimNode_matrix(node_matrix, 3)
    
    print ("------------")
    
    
    for i in node_matrix:
        print(i)