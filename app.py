import os
from livereload import Server
from flask import (Flask, redirect, render_template, request,
                   send_from_directory, send_file ,jsonify , url_for)

app = Flask(__name__)


@app.route('/')
def index():
   print('Request for index page received')
   return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route('/hello', methods=['POST'])
def hello():
   name = request.form.get('name')

   if name:
       print('Request for hello page received with name=%s' % name)
       return render_template('hello.html', name = name)
   else:
       print('Request for hello page received with no name or blank name -- redirecting')
       return redirect(url_for('index'))


@app.route('/response_json',methods=['GET'])
def returnJson():
     if(request.method == 'GET'): 
        data = { 
            "Modules" : 17, 
            "Subject" : "Data Structures and Algorithms", 
        } 
  
        return jsonify(data) 


@app.route('/get_image',methods=['GET'])
def get_image():
    filename = 'trial.jpg'
    return send_file(filename, mimetype='image/jpg')

if __name__ == '__main__':

   app.run()
