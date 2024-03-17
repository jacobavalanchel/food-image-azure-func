import requests
import json
import pandas as pd
from fuzzywuzzy import fuzz

# 定义模糊匹配函数
def fuzzy_match(query, choices):
    match_scores = [(choice, fuzz.ratio(query, choice)) for choice in choices]
    match_scores.sort(key=lambda x: x[1], reverse=True)
    return match_scores[0][0], match_scores[0][1]

# 输入食品名称
food_name = input("Please enter the food name：\n")

# 读取数据集
df = pd.read_csv('D:\\deep learning\\imagine cup\\USDA National Nutrient Database\\_test.csv')

# 模糊匹配搜索
matched_food, match_score = fuzzy_match(food_name, df['Descrip'])

# 输出匹配度
#print("Matching degree：", match_score/100)

# 使用 loc 方法筛选出特定食品名称对应的营养成分
filtered_df = df.loc[df['Descrip'] == matched_food, ['Energy_kcal','Protein_g','Fat_g','Carb_g','Sugar_g','Fiber_g','VitA_mcg','VitB6_mg','VitB12_mcg','VitC_mg','VitE_mg','Folate_mcg','Niacin_mg','Riboflavin_mg','Thiamin_mg','Calcium_mg','Copper_mcg','Iron_mg','Magnesium_mg','Manganese_mg','Phosphorus_mg','Selenium_mcg','Zinc_mg','VitA_USRDA','VitB6_USRDA','VitB12_USRDA','VitC_USRDA','VitE_USRDA','Folate_USRDA','Niacin_USRDA','Riboflavin_USRDA','Thiamin_USRDA','Calcium_USRDA','Copper_USRDA','Magnesium_USRDA','Phosphorus_USRDA','Selenium_USRDA','Zinc_USRDA']]

# 打印筛选结果
#print(filtered_df)

def get_access_token():
    """
    使用 API Key，Secret Key 获取access_token，替换下列示例中的应用API Key、应用Secret Key
    """
        
    url = "https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=LXfint7ki0EIft9ED0haIpzb&client_secret=RjZY8lZWPHCKylDfibvh16GFsHk1SpV9"
    
    payload = json.dumps("")
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)
    return response.json().get("access_token")

def main():
    user_info = input("Please enter the user's personal information (including age and health issues):\n")

    # 假设你想要将DataFrame转换为一个字典列表
    food_info_list = filtered_df.to_dict(orient='records')
    
    # 构造请求体
    message = {
        "user_info": user_info,
        "food_info": food_info_list,
        "match_score": match_score / 100
    }

    food_info = filtered_df.to_json(orient='records')
    
    message = f"User Personal Information:{user_info}，Nutrients in food:{food_info}，is this food suitable for the user?(Answer in English)"
    
    access_token = get_access_token()
    url = f"https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/completions_pro?access_token=24.de94da8352f0f83c92aa6a31420e7b66.2592000.1710040063.282335-50240777"
    
    payload = json.dumps({
        "messages": [
            {
                "role": "user",
                "content": message
            }
        ]
    })
    #payload = json.dumps({
    #    "messages": [
    #        {
    #            "role": "user",
    #            "content": message
    #        },
    #        {
    #            "role": "assistant",
    #            "content": json.dumps(message)  # 将message序列化为JSON字符串
    #        }
    #    ]
    #})

    headers = {
        'Content-Type': 'application/json',
        'Accept':'application/json;lang=en'
    }
    
    response = requests.request("POST", url, headers=headers, data=payload)

    result=response.json().get("result")
    
    #print(result)

 # 输出结果
    output = {
        "match_score": match_score / 100,
        "food_info": food_info_list,
        "ai_response": result
    }
    print(json.dumps(output, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()