import face_recognition
import numpy
import time
import os


path_data = "data.json"

def knn_search_rtree(file_name, K, cwd, indexed_dictionary,idx):
      image_path = cwd + '/test_images/' + file_name
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
          new_face_encoding = tuple(face_encoding[0])
          result=[]
          print("searching...")
          start=time.time()
          KNNvalue = list(idx.nearest(coordinates=new_face_encoding, num_results=K))
          end=time.time()     
          counter = 1
      #     previous_path = " "
          for idx in KNNvalue:
            item = indexed_dictionary[idx]
            path = item[0]
            first = numpy.array(item[1])
            second = numpy.array(new_face_encoding[0])
            distance = numpy.linalg.norm(first - second)
            # if(previous_path != path):
            result.append((round(distance, 3), path))
            # previous_path = path
            if counter > K:
              break
            counter += 1
          tiempo = str(round((end-start)*1000))
          print("knn search rtree search took " + tiempo + " ms.")
          print("displaying results:")
          return result, tiempo

def range_search_rtree(file_name, radius, cwd, idx, indexed_dictionary):
      image_path = cwd + '/test_images/' + file_name
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
                  new_face_encoding = tuple(face_encoding[0])
                  limite_inferior = []
                  limite_superior = []
                  for point in new_face_encoding:
                        limite_inferior.append(point - radius)
                        limite_superior.append(point + radius)
                  bound = limite_inferior + limite_superior
                  start = time.time()
                  range_values = [n for n in idx.intersection(bound)]
                  end = time.time()
                  result = []
                  second = numpy.array(new_face_encoding[0])
                  previous_path = ""
                  for idx in range_values:
                        # dist = numpy.linalg.norm(numpy.asarray(new_face_encoding)-numpy.asarray(vectors[path]))
                        item = indexed_dictionary[idx]
                        path = item[0]
                        first = numpy.array(item[1])
                        dist = numpy.linalg.norm(first - second)
                        if dist < radius and path != previous_path:
                              result.append((path, round(dist, 3)))
                        previous_path = path
                  # result = sorted(result, key=lambda item: item[2])
                  print("range search rtree took " + str(round((end-start)*1000, 3)) + " ms.")
                  print("displaying results:")
                  return result
