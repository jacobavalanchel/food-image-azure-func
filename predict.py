from ultralytics import YOLO

# 模型路径
model = YOLO('last.pt')

# 预测图片路径，输出结果保存
result = model(source='Five_tips_Stream.jpg', save=True)
print(result)