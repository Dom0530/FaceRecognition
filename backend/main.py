from sequential_search import *
from image_processing import *
from rtree_search import *
from kdtree import *
from rtree import index
import os

cwd = os.getcwd() # current working directory
processed_images_path = cwd + "/processed_dataset"
filename = "processed_images.json"

class some_class():
    total = 13175
    block_dictionary = {}
    indexed_dictionary = {}

    def __init__(self, limit, flag):
        if flag:
            self.PROCESS_IMAGES(limit)
        self.PROCESS_RTREE()
        #self.LOAD_RTREE()

    # def LOAD_RTREE(self):
    #     try:
    #         with

    #     expect:
    #         print("error loading rtree")

    def PROCESS_RTREE(self):
        # clear_rtree_directory()
        # 128d rtree index
        p = self.load_rtree_properties()
        self.idx128d = index.Index('128d_index', properties=p)
        # print(type(self.idx128d))
        if(len(self.block_dictionary) == 0):
            self.block_dictionary = load_block_dictionary(self.block_dictionary, self.total)
            if(len(self.block_dictionary) == 0):
                print("data has not been processed..")
                return 0
        # insert points in rtree
        items =  list(self.block_dictionary.items())
        counter = 1
        for item in items:
            val = tuple(numpy.array(list(map(float, item[1].strip("()").split(', ')))))
            # print("Inserting point " + str(counter))
            self.idx128d.insert(counter, val)
            self.indexed_dictionary[counter] = (str(item[0]), val)
            counter += 1
        # store it in file
        # self.idx128d.close()
    
    def load_rtree_properties(self):
        p = index.Property()
        p.dimension = 128 
        p.buffering_capacity = 4
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        return p

    def PROCESS_IMAGES(self, limit):
        clear_processed_processes_directory()
        self.total, self.block_dictionary = process_dataset(limit)
        
    def RANGE_SEARCH_RTREE(self, file_name, radius):
        if hasattr(self, 'idx128d'):
            info = range_search_rtree(file_name, radius, cwd, self.idx128d, self.indexed_dictionary)
            self.printing(info)
        else:
            # if it is stored in a file, unpack it and use it
            pass
            # p = self.load_rtree_properties()
            # self.idx128d = index.Index('128d_index', properties=p)

    def KNN_SEARCH_RTREE(self, file_name, k):
        print('KNN_SEARCH_TREE')
        if hasattr(self, 'idx128d'):
            info = knn_search_rtree(file_name, k, cwd, self.indexed_dictionary, self.idx128d)
            self.printing(info)       
        else:
            # if it is stored in a file, unpack it and use it
            pass

    def RANGE_SEARCH(self, file_name, radius):
        if(len(self.block_dictionary) == 0):
            # try to load with what is in the files
            self.block_dictionary = load_block_dictionary(self.block_dictionary, self.total)
            if(len(self.block_dictionary) == 0):
                print("data has not been processed..")
                return []
        info = range_search(file_name, radius, cwd, self.block_dictionary)
        self.printing(info)
        return info
    
    def KNN_SEARCH(self, file_name, k):
        print('KNN_SEARCH')
        if(len(self.block_dictionary) == 0):
            # try to load with what is in the files
            self.block_dictionary = load_block_dictionary(self.block_dictionary, self.total)
            if(len(self.block_dictionary) == 0):
                print("data has not been processed..")
                return []
        info, tiempo = knn_search(file_name, k, cwd, self.block_dictionary)
        self.printing(info)
        return info, tiempo

    def KDTREE(self, file_name, k):
        print('KDTREE')
        if(len(self.block_dictionary) == 0):
            self.block_dictionary = load_block_dictionary(self.block_dictionary, self.total)
            if(len(self.block_dictionary) == 0):
                print("data has not been processed..")
                return []
        info, tiempo = kdtree(file_name, k, cwd, self.block_dictionary)
        self.printing(info)  
        return info, tiempo

    def printing(self, info):
        counter = 0
        for key in info:
            # print(key)
            print(str(counter) + ") -> (" + str(key[0]) + ", " + str(key[1]) + ")")
            counter += 1


# filename is provided
#  radius is provided
# cwd must be calculated before
# total must be calculated in init, is the number of encodings we have
# encodings is a list (example) with a relative order with the indexes
# paths is a list with a relative order with the indexes
#   it means that for index 0, encodings have an code, and paths have the name of that code in specific
# all of that calculated in init