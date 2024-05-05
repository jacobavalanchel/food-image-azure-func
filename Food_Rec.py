from PIL import Image
from model import VIT
import torch
import torchvision.transforms as transforms

transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])

# 加载模型和权重
default_model = VIT.vit_base_patch16_224(num_classes=100)
default_model.load_state_dict(torch.load('./model/CFN.pth',map_location = torch.device('cpu')))


# 读取类别文件的函数
def read_file_to_list(file_path='categories.txt'):
    line_list = []
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line_list.append(line.strip())
    return line_list


classes_list = read_file_to_list()


# 食物识别的函数
def food_recognition(image, model=default_model, device="cpu"):
    image = transform(image)
    image.unsqueeze_(dim=0)

    # 将模型和数据放到设备上
    model = model.to(device)
    image = image.to(device)

    model.eval()
    output = model(image)
    prediction = torch.argmax(output, dim=1)
    return classes_list[prediction.item()]


# 读取图片
# test_image = Image.open("sample.jpg")
#
# result = food_recognition(test_image)
#
# print("预测结果为：",result)


