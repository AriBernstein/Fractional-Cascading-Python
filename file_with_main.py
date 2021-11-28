from GeneralNodes.NodeUtils import fullNode_list_to_SingleDimNode_matrix, \
    sort_SingleDimNode_list, sort_FullNode_list, sort_SingleDimNode_matrix
from GeneralNodes.NodeGenerationUtils import generate_FullNode_data_set
from Utils.GeneralUtils import ColIterator, matrix_subset
from RangeTree.RangeTree import RangeTree


if __name__ == "__main__":
    # print(rand_unique_ints(10, 10, 20))
    n = 11
    dim = 3
    loc_min = 0
    loc_max = 100
    
    full_nodes = generate_FullNode_data_set(n, dim, loc_min, loc_max)
    rt = RangeTree(full_nodes, dim)
    
    
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
    
    # node_matrix = fullNode_list_to_SingleDimNode_matrix(fullNodes)
    
    # for i in node_matrix:
    #     print(i)
    
    # print ("------------")
   
    
    # for x in ColIterator(node_matrix, 4):
    #     print(x)  
        
    # for x in matrix_subset(node_matrix, 2, 6):
    #     print(x)
    
    # sort_SingleDimNode_matrix(node_matrix, 3)
     
    
    # for i in node_matrix:
    #     print(i)