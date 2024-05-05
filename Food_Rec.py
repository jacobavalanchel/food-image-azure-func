from PIL import Image
from model import VIT
import torch
import torchvision.transforms as transforms

transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])


# 读取类别文件的函数
def read_file_to_list(file_path='labels.txt'):
    # 初始化一个空列表来存储每一行的内容
    line_list = []
    # 打开文件
    with open(file_path, 'r', encoding='utf-8') as file:
        # 逐行读取文件
        for line in file:
            # 将每一行的文本去除末尾的换行符并添加到列表中
            line_list.append(line.strip())
    # 返回包含每一行内容的列表
    return line_list


classes_list = read_file_to_list()


# 食物识别的函数
def food_recognition(image, model, device):
    image = transform(image)
    image.unsqueeze_(dim=0)

    # 将模型和数据放到设备上
    model = model.to(device)
    image = image.to(device)

    model.eval()
    output = model(image)
    prediction = torch.argmax(output, dim=1)
    return classes_list[prediction.item()]


# 加载模型和权重
test_model = VIT.vit_base_patch16_224(num_classes=20)
test_model.load_state_dict(torch.load("./model/vit.pth"))

# 定义设备
test_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")


# 读取图片
test_image = Image.open("sample.jpg")

result = food_recognition(image=test_image, model=test_model, device=test_device)

print("预测结果为：",result)


