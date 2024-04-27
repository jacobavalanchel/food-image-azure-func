import json
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import ollama

def apipei(query, choices):
    match_scores = [(choice, fuzz.ratio(query, choice)) for choice in choices]
    match_scores.sort(key=lambda x: x[1], reverse=True)
    return match_scores[0][0], match_scores[0][1]

def bpipei(query, choices):
    scorer = fuzz.QRatio
    result = process.extractOne(query, choices, scorer=scorer)
    return result[0] if result else None

food_name = input("请输入食物名称：\n")

nutrient_dataset_path = 'D:\大学生计算机设计大赛\_atest.txt'
df_nutrient = pd.read_csv(nutrient_dataset_path, encoding='utf-8')
glycemic_index_dataset_path = (r'D:\大学生计算机设计大赛\营养素数据集\food GI.csv')
df_glycemic_index = pd.read_csv(glycemic_index_dataset_path)
insulin_index_dataset_path = 'D:\大学生计算机设计大赛\营养素数据集\Insulin index.csv'

df_insulin_index = pd.read_csv(insulin_index_dataset_path)
df_glycemic_index = df_glycemic_index.dropna()
df_glycemic_index['Name'] = df_glycemic_index['Name'].str.lower()

matched_food1, match_score1 = apipei(food_name, df_nutrient['Descrip'])
matched_food2 = bpipei(food_name,df_glycemic_index['Name'])
matched_food3 = bpipei(food_name,df_insulin_index['Name'])

filtered_df1 = df_nutrient.loc[df_nutrient['Descrip'] == matched_food1, ['能量_千卡','蛋白质_克','脂肪_克','碳水化合物_克','糖_克','纤维_克','维生素A_微克','维生素B6_毫克','维生素B12_微克','维生素C_毫克','维生素E_毫克','叶酸_微克','烟酸_毫克','核黄素_毫克','硫胺素_毫克','钙_毫克','铜_毫克','铁_毫克','镁_毫克','锰_毫克','磷_毫克','硒_微克','锌_毫克','维生素A_推荐量','维生素B6_推荐量','维生素B12_推荐量','维生素C_推荐量','维生素E_推荐量','叶酸_推荐量','烟酸_推荐量','核黄素_推荐量','硫胺素_推荐量','钙_推荐量','铜_推荐量','镁_推荐量','磷_推荐量','硒_推荐量','锌_推荐量']]
filtered_df2 = df_glycemic_index[df_glycemic_index['Name'] == matched_food2]
filtered_df3 = df_insulin_index[df_insulin_index['Name'] == matched_food3]

def main():  
    user_info = input("请输入用户的个人信息 (包括年龄和所患疾病):\n")

    food_info_list = filtered_df1.to_dict(orient='records')
    GI_info_list = filtered_df2['Glycemic index'].tolist()
    Insulinindex_info_list = filtered_df3['Insulin index'].tolist()
    
    message = {
        "user_info": user_info,
        "GI_info":GI_info_list,
        "Insulinindex_info":Insulinindex_info_list,
        "food_info": food_info_list
    }

    food_info = filtered_df1.to_json(orient='records')
    GI_info = filtered_df2.to_json(orient='records')
    Insulinindex_info = filtered_df3.to_json(orient='records')

    message = f"{food_name}（营养素信息：{food_info}，升糖指数：{GI_info}，胰岛素指数：{Insulinindex_info}输出结果不需要显示）适合{user_info}的人吗？（只需要给出合理的建议）"

    response = ollama.chat(model='llama2-chinese', messages=[
      {
        'role': 'user',
        'content': message,
      },
    ])
    
    output = {
        "GI_info":GI_info_list,
        "Insulinindex_info": Insulinindex_info_list,
        "food_info": food_info_list,
        "ai_response": response['message']['content']
    }
    print(json.dumps(output, indent=4, ensure_ascii=False))

if __name__ == '__main__':
    main()