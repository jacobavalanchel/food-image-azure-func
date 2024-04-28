from flask import (Flask, request,
                   send_file, jsonify)
from flask_cors import CORS

# from ultralytics import YOLO

app = Flask(__name__)
CORS(app)


@app.route('/response_json', methods=['GET'])
def returnJson():
    if request.method == 'GET':
        data = {
            "Modules": 17,
            "Subject": "Data Structures and Algorithms",
        }
        return jsonify(data)


@app.route('/get_image', methods=['POST'])
def get_image():
    file_name = request.form.get('file_name')
    return send_file(str(file_name), mimetype='image/jpg')


@app.route('/get_result_detail', methods=['POST'])
def get_result_detail():
    result_detail = [{
        "name": "能量供给",
        "score": 3.5,
        "scoreText": "这个食品非常适合你吃",
        "RowLabels": ["项目", "当前值", "建议值", "单位"],
        "RowContents": [
            ["碳水化合物", 6, 12, "mg"],
            ["脂肪", 6, 12, "mg"],
            ["蛋白质", 6, 12, "mg"]
        ]
    }, {
        "name": "糖代谢",
        "score": 4.5,
        "scoreLabel": "适合",
        "scoreText": "这个食品糖:",
        "RowLabels": ["项目", "当前值", "建议值", "单位"],
        "RowContents": [
            ["纤维素", 6, 12, "mg"],
            ["游离糖", 6, 12, "mg"],
            ["GI数", 6, 12, "mg"],
        ],
    },
    ]
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
