import os

from flask import (Flask, redirect, render_template, request,
                   send_from_directory, send_file, jsonify, url_for)
from flask_cors import CORS
from ultralytics import YOLO

app = Flask(__name__)
CORS(app)


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
        return render_template('hello.html', name=name)
    else:
        print('Request for hello page received with no name or blank name -- redirecting')
        return redirect(url_for('index'))


@app.route('/response_json', methods=['GET'])
def returnJson():
    if (request.method == 'GET'):
        data = {
            "Modules": 17,
            "Subject": "Data Structures and Algorithms",
        }

        return jsonify(data)


@app.route('/get_image', methods=['GET'])
def get_image():
    filename = 'trial.jpg'
    return send_file(filename, mimetype='image/jpg')


@app.route('/start_recog', methods=['POST'])
def start_recog():
    name = request.form.get('name')
    if name:
        print('Request for hello page received with name=%s' % name)

    # 模型路径
    model = YOLO('best.pt')

    # 预测图片路径，输出结果保存
    result = model(source='Five_tips_Stream.jpg', save=True)
    print(result)

    source_img_path_list = []
    save_img_path_list = []
    for item in result:
        print(item.boxes.xyxy[0])
        source_img_path_list.append(item.path)
        save_img_path_list.append(item.save_dir)
        for box in item.boxes:
            print(box.xyxy[0])
            print(model.names[int(box.cls)])

    # read file result
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    rel_path = "2091/data.txt"

    head, tail = os.path.split(source_img_path_list[0])
    abs_file_path = os.path.join(script_dir, save_img_path_list[0],tail)
    print(f"abs_file_path{abs_file_path}")
    return send_file(str(abs_file_path), mimetype='image/jpg')

    # return {"filename": abs_file_path}


if __name__ == '__main__':
    app.run()
