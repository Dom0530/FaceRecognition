from flask import Flask, render_template, request, redirect, url_for, jsonify
from werkzeug.utils import secure_filename
import os
from main import *


cwd = os.getcwd()

app = Flask(_name_)
app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)

# Configuración CORS
def add_cors_headers(response):
    response.headers['Access-Control-Allow-Origin'] = 'http://localhost:3000'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    return response

@app.after_request
def apply_cors(response):
    return add_cors_headers(response)

@app.route("/knnkdtree/<file>/<k>", methods=['GET'])
def KNNSearchKD(file, k):
    k = int(k)  # Convertir a entero
    if k <= 0:
        k = 1
    if file == '':
        return {'ok': False, 'msg': 'Missing file'}, 400
    image_path = cwd + '/test_images/' + file
    if not os.path.exists(image_path):
        return {'ok': False, 'msg': 'Image is not in test_images'}, 422 
    
    res, tiempo = smt.KDTREE(file, k)
    
    if len(res) == 0:
        return {'ok': True, 'msg': 'No similar images found'}, 200
    
    return {'ok': True, 'data': res, 'time': tiempo}, 200


@app.route("/knnrtree/<file>/<k>", methods=['GET'])
def KNNSearchRT(file, k):
    k = int(k)
    if k <= 0:
       k = 1
    if file == '':
       return {'ok': False, 'msg': 'Missing file'}, 400
    image_path = cwd + '/test_images/' + file
    if not os.path.exists(image_path):
       return {'ok': False, 'msg': 'Image is not in test_images'}, 422 
    
    res,tiempo = smt.KNN_SEARCH_RTREE(file, k)
    
    if res is None:
       return {'ok': True, 'msg': 'No similar images found'}, 200
    
    if len(res) == 0:
       return {'ok': True, 'msg': 'No similar images found'}, 200 
    
    return  {'ok': True, 'data': res,'time': tiempo }, 200

@app.route("/knnsearch/<file>/<k>", methods=['GET'])
def KNNSearch(file, k):
    k = int(k)  # Convertir a entero
    if k <= 0:
        k = 1
    if file == '':
        return {'ok': False, 'msg': 'Missing file'}, 400
    image_path = cwd + '/test_images/' + file
    if not os.path.exists(image_path):
        return {'ok': False, 'msg': 'Image is not in test_images'}, 422 
    
    res, tiempo = smt.KNN_SEARCH(file, k)
    
    if len(res) == 0:
        return {'ok': True, 'msg': 'No similar images found'}, 200 
    
    return  {'ok': True, 'data': res, 'time': tiempo}, 200

@app.route("/upload", methods=['POST'])
def uploader():
    try:
        if 'sm' not in request.form:
            return {'ok': False, 'msg': 'Missing method'}, 400
        sm = request.form['sm']
        if sm not in ['knnsearch', 'knnrtree', 'knnkdtree']:
            return {'ok': False, 'msg': 'Invalid method'}, 422 
        f = request.files['archivo']
        k = request.form['K datos']
        filename = secure_filename(f.filename)
        f.save(os.path.join(app.instance_path, 'uploads', secure_filename(f.filename)))
        
        if sm == 'knnsearch':
            return KNNSearch(filename, k)  # Llamar directamente a la función KNNSearch
        elif sm == 'knnrtree':
            return KNNSearchRT(filename, k)  # Llamar directamente a la función KNNSearchRT
        elif sm == 'knnkdtree':
            return KNNSearchKD(filename, k)  # Llamar directamente a la función KNNSearchKD
    except Exception as e:
        return {'ok': False, 'msg': str(e)}, 422
    print(KNNSearch)
    return {'ok': True, 'sm': sm, 'file': filename, 'k': k}  # Devolver los valores sm, file y k

if _name_ == '_main_':
    smt = some_class(14500, False)  # true or false is a flag that indicates if it is needed to process all 14000 images
    app.run(debug=True, use_reloader=False)