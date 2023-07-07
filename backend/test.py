from main import *

cwd = os.getcwd() # current working directory

 

def test():
    smt = some_class(14000, False)
    # smt.RANGE_SEARCH("Salma_Hayek.jpeg", 0.5)
    # print()
    smt.KNN_SEARCH("Salma_Hayek.jpeg", 8)
    # print()
    # smt.RANGE_SEARCH_RTREE("Salma_Hayek.jpeg", 1.21) # que radio usamos?
    print()
    smt.KNN_SEARCH_RTREE("Salma_Hayek.jpeg", 8)
    print()
    smt.KDTREE("Salma_Hayek.jpeg", 8)

test()