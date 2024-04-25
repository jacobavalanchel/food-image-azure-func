import json
import pandas as pd
from fuzzywuzzy import fuzz
import ollama

# 定义模糊匹配函数
def fuzzy_match(query, choices):
    match_scores = [(choice, fuzz.ratio(query, choice)) for choice in choices]
    match_scores.sort(key=lambda x: x[1], reverse=True)
    return match_scores[0][0], match_scores[0][1]

# 输入食品名称
food_name = input("请输入食物名称：\n")

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

def main():  
    user_info = input("请输入用户的个人信息 (包括年龄和所患疾病):\n")

    # 假设你想要将DataFrame转换为一个字典列表
    food_info_list = filtered_df.to_dict(orient='records')

    
    # 构造请求体
    message = {
        "user_info": user_info,
        "food_info": food_info_list,
        "match_score": match_score / 100
    }

    food_info = filtered_df.to_json(orient='records')


    message = f"{food_name}（营养素信息：{food_info}，输出结果不需要显示）适合{user_info}的人吗？（只需要给出合理的建议）"

    #print(message)

    
    response = ollama.chat(model='llama2-chinese', messages=[
      {
        'role': 'user',
        'content': message,
      },
    ])
    
#print(response['message']['content'])

# 输出结果
    output = {
        "match_score": match_score / 100,
        "food_info": food_info_list,
        "ai_response": response['message']['content']
    }
    print(json.dumps(output, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
