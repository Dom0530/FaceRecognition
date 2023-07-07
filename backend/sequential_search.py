# indexacion y busqueda - KNN - Secuencial

# KNN-Secuencial: Implementación de los algoritmos de búsqueda sin indexación
# o Búsqueda KNN con cola de prioridad, el cual recibe como parámetro el objeto de 
# consulta y la cantidad de objetos a recuperar K.
# o Búsqueda  por  Rango,  el  cual  recibe  como  parámetro  el  objeto  de  consulta  y  un 
# radio  de  búsqueda.    Incluir  el  análisis  de  la  distribución  de  la  distancia  para 
# experimentar con 3 valores de radio diferente. 

import time
import os
import numpy
import face_recognition
from queue import PriorityQueue 

def range_search(file_name, radius, cwd, block_dictionary):
    #image_path = cwd + '/test_images/' + file_name
    image_path = cwd + '/instance/uploads/' + file_name
    radius = 0.5
    if not os.path.exists(image_path):
        print("No path")
        return []
    else:
        face = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(face) # calculating the image encoding
        if len(face_encoding) == 0:
            print("no face founnd")
            return []
        else:
            new_face_encoding = tuple(face_encoding)
            result = []
            #gather info
            info = []
            print("searching...")
            time1 = time.time()
            # for i in range(total):
            for path in block_dictionary:
                # print(block_dictionary[path])
                # print(type(block_dictionary[path]))
                # print(new_face_encoding[0])
                # print(type(new_face_encoding[0]))
                first = numpy.array(list(map(float, block_dictionary[path].strip("()").split(', '))))
                second = numpy.array(list(map(float, new_face_encoding[0])))
                distance = numpy.linalg.norm(first - second)
                if distance < radius:
                    result.append((path, distance))
                    person = path
                    info.append((person, round(distance,3)))
            time2 = time.time()
            print("reange_search took " + str(round((time2 - time1) * 1000)) + " ms.")
            print("displaying results:")
            return info

def knn_search(file_name, k, cwd, block_dictionary):
    pq = PriorityQueue(False)
    #image_path = cwd + '/test_images/' + file_name
    image_path = cwd + '/instance/uploads/' + file_name
    if not os.path.exists(image_path):
        print("No path")
        return []
    else:
        face = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(face) # calculating the image encoding
        if len(face_encoding) == 0:
            print("no face found")
            return []
        else:
            new_face_encoding = tuple(face_encoding)
            result = []
            #gather info
            info = []
            print("searching...")
            time1 = time.time()
            for path in block_dictionary:
                first = numpy.array(list(map(float, block_dictionary[path].strip("()").split(', '))))
                second = numpy.array(list(map(float, new_face_encoding[0])))
                distance = numpy.linalg.norm(first - second)
                person = path
                pq.put((round(distance,3), person))
                info.append((round(distance,3),person))
            for i in range(k):
                result.append(pq.get())
            time2 = time.time()
            tiempo = str(round((time2 - time1) * 1000))
            print("knn_search took " + tiempo + " ms.")
            print("displaying results:")
            return result, tiempo

# we pass a file, a photo or image we have to compare to the ones we processed

# si no existe un path hacia el file, retoranmos error de file no encontrado
# we load and encode the image file using the face_recognition module
# if len == 0, return bc we did not find any face in the image
# else, we load the encoding in a tuple
# start time
# for i in range(13333) 
#     first = procesed image encoding
#     second = our image encoding
#     distancia = numpy.linalg.norm(first-second)
#     if distanci menor que radio:
#         hacemos append a nuestra lista de resultados(i, dist)
# hacemos sort de los resultados. o podriamos usar un priority queue aqui.
# end time
# get info like path, file_name, and dist
# append to result
# return

