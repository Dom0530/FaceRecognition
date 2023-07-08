from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
import os
from main import *

#app = Flask(__name__, template_folder='../frontend/templates', static_folder= "../frontend/static")
app = Flask(__name__, template_folder='../frontend/templates/', static_folder= os.getcwd()) 


app.config['UPLOAD_FOLDER'] = './uploads'
os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)

smt = some_class(14500, False) # true or false is a flag that indicates if it is needed to process al 14000 images


@app.route("/")
def index():
    return render_template('index.html') 

'''
@app.route("/rangeSearch/<file>/<radius>", methods=['GET'])
def rangeSearch(file, radius):
    res = smt.RANGE_SEARCH(file, radius)
    return res
'''
@app.route("/knnkdtree/<file>/<k>", methods=['GET'])
def KNNSearchKD(file, k):
    if k <= 0:
       k = 1
    if file == '':
       return {'ok':False, 'msg': 'Missing file'}, 400
    image_path = cwd + '/test_images/' + file
    if not os.path.exists(image_path):
       return {'ok':False, 'msg': 'Image are not in test_images'}, 422 
    
    res, tiempo = smt.KDTREE(file, k)
    
    if len(res) == 0:
       return {'ok':True, 'msg': 'No similar images found'}, 200
    
    return {'ok':True, 'data':res, 'time': tiempo },200

'''
@app.route("/ind/<file>/<radius>", methods=['GET'])
def rangeSearchInd(file, radius):
    res = smt.RANGE_SEARCH_RTREE(file, radius)
    return res
'''

@app.route("/knnrtree/<file>/<k>", methods=['GET'])
def KNNSearchRT(file, k):
    if k <= 0:
       k = 1
    if file == '':
       return {'ok':False, 'msg': 'Missing file'}, 400
    image_path = cwd + '/test_images/' + file
    if not os.path.exists(image_path):
       return {'ok':False, 'msg': 'Image are not in test_images'}, 422 
    
    res = smt.KNN_SEARCH_RTREE(file, k)
    
    if len(res) == 0:
       return {'ok':True, 'msg': 'No similar images found'}, 200 
    
    return  {'ok':True, 'data':res },200


@app.route("/knnsearch/<file>/<k>", methods=['GET'])
def KNNSearch(file, k):
    if k <= 0:
       k = 1
    if file == '':
       return {'ok':False, 'msg': 'Missing file'}, 400
    image_path = cwd + '/test_images/' + file
    if not os.path.exists(image_path):
       return {'ok':False, 'msg': 'Image are not in test_images'}, 422 
    
    res, tiempo = smt.KNN_SEARCH(file, k)
    
    if len(res) == 0:
       return {'ok':True, 'msg': 'No similar images found'}, 200 
    
    return  {'ok':True, 'data':res , 'time': tiempo},200


@app.route("/upload", methods=['POST'])
def uploader():
 if request.method == 'POST':
    # obtenemos el archivo del input "archivo"
    sm = request.form.get['metodo']
    if sm == '':
       return {'ok':False, 'msg': 'Missing method'}, 400
    if sm not in ['knnsearch', 'knnrtree', 'knnkdtree']:
       return {'ok':False, 'msg': 'Invalid method'}, 422 
    f = request.files['archivo']
    k = request.form['K datos']
    print(k)
    filename = secure_filename(f.filename)
    f.save(os.path.join(app.instance_path, 'uploads', secure_filename(f.filename)))
    # Si se quiere eliminar el archivo usar remove(UPLOADS_PATH + filename)
    return redirect(url_for(sm, file = filename, k = k))


if __name__ == '__main__':
    #smt = some_class(14500, True) # true or false is a flag that indicates if it is needed to process al 14000 images
    app.run(debug=True, use_reloader = False)
    app.add_url_rule('/favicon.ico', redirect_to=url_for('static', filename='../frontend/static/images/logo_utec.png'))
    