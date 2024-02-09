from ultralytics import YOLO

# 模型路径
model = YOLO("F:\\jasonadvance\\Documents\\Tencent Files\\718769082\\FileRecv\\Predict\\best.pt")

# 预测图片路径，输出结果保存
result = model(source='F:\\jasonadvance\\Documents\\Tencent Files\\718769082\\FileRecv\\Predict\\Five_tips_Stream.jpg', save=True)
