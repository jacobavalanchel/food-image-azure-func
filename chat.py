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
dataset_path = 'D:\大学生计算机设计大赛\_atest.txt'
df = pd.read_csv(dataset_path, encoding='utf-8')

# 模糊匹配搜索
matched_food, match_score = fuzzy_match(food_name, df['Descrip'])

# 输出匹配度
#print("Matching degree：", match_score/100)

# 使用 loc 方法筛选出特定食品名称对应的营养成分
filtered_df = df.loc[df['Descrip'] == matched_food, ['能量_千卡','蛋白质_克','脂肪_克','碳水化合物_克','糖_克','纤维_克','维生素A_微克','维生素B6_毫克','维生素B12_微克','维生素C_毫克','维生素E_毫克','叶酸_微克','烟酸_毫克','核黄素_毫克','硫胺素_毫克','钙_毫克','铜_毫克','铁_毫克','镁_毫克','锰_毫克','磷_毫克','硒_微克','锌_毫克','维生素A_推荐量','维生素B6_推荐量','维生素B12_推荐量','维生素C_推荐量','维生素E_推荐量','叶酸_推荐量','烟酸_推荐量','核黄素_推荐量','硫胺素_推荐量','钙_推荐量','铜_推荐量','镁_推荐量','磷_推荐量','硒_推荐量','锌_推荐量']]

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
