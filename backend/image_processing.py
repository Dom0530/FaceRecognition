import face_recognition
import numpy
import random
import linecache as lc
import io
# import matplotlib.pyplot
# from os import listdir
import shutil
import os
# from os.path import isfile, join
import json

N = 5000
BLOCK_SIZE = 1000
cwd = os.getcwd() # current working directory
processed_images_path = cwd + "/processed_dataset"
filename = "processed_images.json"
path_to_clean_1 = processed_images_path


def process_dataset(limit):

    total = 0 # this is the total number of processed images

    # distribution = []
    # final_distribution = []

    if not os.path.exists(processed_images_path): # of the path for the processed imaged folder do not exist, create it
        os.makedirs(processed_images_path)

    FACTOR = 1
    counter = 0
    block_dictionary = {}
    encodings = {}
    # aux_list = [] # this is used to load each dictionary in an entry of the list, to append each entry in one line of the file, by iterating over this list
    dataset_directory_path = cwd + "/dataset" # path for the data file
    dataset_subdirectories_list = os.listdir(dataset_directory_path) # path for the subdirectories in the data file

    for subdirectory in dataset_subdirectories_list: # list of all subdirectories names
        # print(subdirectory) # name of the las sub subdirectories
        if(total >= limit):
            load_to_memory(block_dictionary)
            return total, encodings

        subdirectory_path = dataset_directory_path + "/" + subdirectory
        for image in os.listdir(subdirectory_path): # search in all subdirectories # in most of them there are only 1
            if(total >= limit):
                load_to_memory(block_dictionary)
                return total, encodings

            image_path = subdirectory_path + "/" + image
            key = subdirectory + '/' + image
            face = face_recognition.load_image_file(image_path)
            face_encoding = face_recognition.face_encodings(face) # calculating the image encoding
            
            if len(face_encoding) != 0:
                new_face_encoding = tuple(face_encoding[0])
                # distribution.append(new_face_encoding)
                if new_face_encoding not in block_dictionary:
                    block_dictionary[key] = str(new_face_encoding)
                    encodings[key] = str(new_face_encoding)
                    total += 1
                    print(counter)
                    counter += 1
                    if counter > BLOCK_SIZE*FACTOR:
                        print("counter")
                        FACTOR += 1
                        load_to_memory(block_dictionary)
                else:
                    block_dictionary[key] += str(new_face_encoding)
                    encodings[key] = str(new_face_encoding)
                    total += 1
                    print(counter)
                    counter += 1
                    if counter > BLOCK_SIZE*FACTOR:
                        print("counter")
                        FACTOR += 1
                        load_to_memory(block_dictionary)
                
            else: # some debugging
                print("no face found in: " + str(image_path))
    # final_distribution = genDist(N, distribution)
    load_to_memory(block_dictionary)
    # matplotlib.pyplot.hist(final_distribution, bins=100)
    # matplotlib.pyplot.show()

    return total, encodings


def load_to_memory(block_dictionary):
    try:
        path = processed_images_path + '/' + filename
        with open(path, 'a', encoding="utf-8") as file: 
            print("data is: [face_image_path] -> face encoding")
            print("loading data into new directory file...")
            for keyword in block_dictionary:
                file.write(json.dumps({keyword: block_dictionary[keyword]}, ensure_ascii=False))
                file.write("\n")
            file.close()
            print("data successfully uploaded!")
        block_dictionary.clear()
        return 1
    except IOError:
        print("Problem reading: " + str(path) + " path.")
        return 0


def genDist(N, distribution):
    result = []
    
    for i in range(1, N):
        aux = () # tuple
        aux = random.sample(range(0, len(distribution)), 2)
        first = numpy.array(distribution[aux[0]])
        second = numpy.array(distribution[aux[1]])
        result.append(numpy.linalg.norm(first - second))
    return result


def clear_processed_processes_directory():
    if os.path.exists(path_to_clean_1):
        shutil.rmtree(path_to_clean_1)
    else:
        print("files not found")

def load_block_dictionary(block_dictionary, total):
    for i in range(1, total):
        PATH = cwd + "/processed_dataset/processed_images.json"
        #print(PATH)
        try:
            aux = lc.getline(PATH, i).rstrip()
            if aux != "":
                json_object = json.load(io.StringIO(aux))
                key = list(json_object.keys())
                value = tuple(json_object.values())
                block_dictionary[key[0]] = value[0]
        except:
            print("There are no processed images")
            return 0
    return block_dictionary



# clear_processed_processes_directory()
# process_dataset()