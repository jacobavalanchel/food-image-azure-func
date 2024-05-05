import os

from flask import (Flask, request,
                   send_file, jsonify)
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
import new_chat
import Users
import config

# from ultralytics import YOLO

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

## User init
Users.init(app, db)
CORS(app)

## Secret Key
app.secret_key = config.FlaskConfig.APP_SECRET_KEY

## jwt
app.config['JWT_SECRET_KEY'] = config.FlaskConfig.JWT_SECRET_KEY
jwt_mgr = JWTManager(app)
@app.route('/get_info', methods=['GET'])
def get_info():
    pass

@app.route('/response_json', methods=['GET'])
def return_json():
    if request.method == 'GET':
        data = {
            "Modules": 17,
            "Subject": "Data Structures and Algorithms",
        }
        return jsonify(data)


@app.route('/upload_image', methods=['POST'])
def get_image():
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({'message': 'No selected file'}), 400

    file.save('uploads/' + file.filename)

    return jsonify({'message': 'File uploaded successfully', 'filename': file.filename}), 200


@app.route('/get_result_detail', methods=['POST'])
def get_result_detail():
    food_name="apple"
    user_info="42岁，糖尿病患者"
    result_detail=new_chat.handle_food_info_get(food_name,user_info)
    return jsonify(result_detail)


# @app.route('/start_recog', methods=['POST'])
# def start_recog():
#     # 模型路径
#     model = YOLO('best.pt')
#
#     # 预测图片路径，输出结果保存
#     result = model(source='Five_tips_Stream.jpg', save=True)
#     print(result)
#
#     source_img_path_list = []
#     save_img_path_list = []
#     for item in result:
#         print(item.boxes.xyxy[0])
#         source_img_path_list.append(item.path)
#         save_img_path_list.append(item.save_dir)
#         for box in item.boxes:
#             print(box.xyxy[0])
#             print(model.names[int(box.cls)])
#
#     # read file result
#     script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
#     rel_path = "2091/data.txt"
#
#     head, tail = os.path.split(source_img_path_list[0])
#     abs_file_path = os.path.join(script_dir, save_img_path_list[0], tail)
#     print(f"abs_file_path{abs_file_path}")
#
#     return {"filename": abs_file_path}


if __name__ == '__main__':
    app.run(debug=True)
