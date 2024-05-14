import os

from PIL import Image
from flask import (Flask, request,
                   jsonify)
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from nutri_details.balanced_diet import balanced_diet_info

import Food_Rec
import Users
import config
import new_chat

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
user_info = {
    "gender": "男",
    "username": "张三峰",
    "age": "18",
    "email": "trial-email@163.com",
    "isPregnant": "否",
    "PA": "中",
    "userLabelData": [
        "高血压患者",
        "注重精神健康",
    ],
    "userLabelCandidates": [
        "中年人",
        "糖尿病患者",
        "高血压患者",
        "注重精神健康",
    ]
}



@app.route('/get_info', methods=['POST'])
def get_info():
    return jsonify(user_info)


@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    return jsonify(balanced_diet_info)


@app.route('/update_info', methods=['POST'])
def update_info():
    global user_info
    user_info = request.json
    print(user_info)
    if user_info:
        return jsonify({"message": user_info})
    else:
        return jsonify({"error": "User not found"}), 404


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
    test_image = Image.open('uploads/' + file.filename)
    test_image = test_image.convert("RGB")
    result = Food_Rec.food_recognition(test_image)
    return jsonify({'result': result}), 200


@app.route('/get_result_detail', methods=['POST'])
def get_result_detail():
    # food_name = request.json["food_name"]
    food_name ="apple"
    user_desc = new_chat.gen_user_desc(user_info)
    result_detail = new_chat.handle_food_info_get(food_name, user_desc, user_info)
    return jsonify(result_detail)


if __name__ == '__main__':
    app.run(debug=True)
