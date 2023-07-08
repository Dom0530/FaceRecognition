from main import *

cwd = os.getcwd() # current working directory

 

def test():
    smt = some_class(14000, False)
    # smt.RANGE_SEARCH("Salma_Hayek.jpeg", 0.5)
    # print()
    res, tiempo = smt.KNN_SEARCH("Salma_Hayek.jpeg", 8)
    print(res)
    print(tiempo)
    # smt.RANGE_SEARCH_RTREE("Salma_Hayek.jpeg", 1.21) # que radio usamos?
    print()
    res = smt.KNN_SEARCH_RTREE("Salma_Hayek.jpeg", 8)
    print(res)
    
    print()
    res, tiempo = smt.KDTREE("Salma_Hayek.jpeg", 8)
    print(res)
    print(tiempo)
test()