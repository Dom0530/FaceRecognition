import time
import os
import numpy
import face_recognition
import pandas as pd

# PCA
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.neighbors import KDTree


def kdtree(file_name, k, cwd, block_dictionary):
    image_path = cwd + '/test_images/' + file_name
    if not os.path.exists(image_path):
        print("No path")
        return []
    else:
        face = face_recognition.load_image_file(image_path)
        face_encoding = face_recognition.face_encodings(face)
        face_encoding = numpy.array(face_encoding)
        if len(face_encoding) == 0:
            print("no face founnd")
            return []
        else:

            isFile = os.path.isfile(cwd+'/KD-TREE.csv')
            
            if not isFile:
                print("a")
                # Tener todo en un dataframe
                col = [str(i) for i in range(128)]
                temp1 = pd.DataFrame(columns=col)
                img = pd.DataFrame(columns=["img"])
                for path in block_dictionary:
                    first = numpy.array(list(map(float, block_dictionary[path].strip("()").split(', '))))
                    first = pd.DataFrame(first.reshape(1,-1), columns=list(col))
                    temp1 = pd.concat( [temp1, first]) 
                    second = pd.DataFrame(numpy.array([path]), columns=["img"])
                    img = pd.concat([img,second])
                temp1["img"] = img
                temp1.to_csv(cwd+'/KD-TREE.csv',index=False, encoding='utf-8')    
                temp1.reset_index(drop=True, inplace=True)
                tree = KDTree(temp1.iloc[:, 0:-1])
                dist, ind = tree.query(face_encoding,k)
                result = []
                for i in range(len(dist[0])):
                    result.append((round(dist[0][i],3),temp1.iloc[ind[0][i]].values.tolist()[-1]))
                return result
            else:
                print("searching...")
                time1 = time.time()
                #temp1.to_csv('KD-TREE.csv',index=False, encoding='utf-8')    
                temp1 = pd.read_csv(cwd+'/KD-TREE.csv')
                temp1.reset_index(drop=True, inplace=True)
                tree = KDTree(temp1.iloc[:, 0:-1])
                dist, ind = tree.query(face_encoding,k)
                result = []
                for i in range(len(dist[0])):
                    result.append((round(dist[0][i],3),temp1.iloc[ind[0][i]].values.tolist()[-1]))
                time2 = time.time()
                tiempo = str(round((time2 - time1) * 1000))
                print("reange_search took " + tiempo + " ms.")
                print("displaying results:")
                return result, tiempo