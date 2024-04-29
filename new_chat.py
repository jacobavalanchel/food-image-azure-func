import json

import ollama
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process


def apipei(query, choices):
    match_scores = [(choice, fuzz.ratio(query, choice)) for choice in choices]
    match_scores.sort(key=lambda x: x[1], reverse=True)
    return match_scores[0][0], match_scores[0][1]


def bpipei(query, choices):
    scorer = fuzz.QRatio
    result = process.extractOne(query, choices, scorer=scorer)
    return result[0] if result else None


# food_name = input("请输入食物名称：\n")

nutrient_dataset_path = 'nutrient_dataset.txt'
df_nutrient = pd.read_csv(nutrient_dataset_path, encoding='utf-8')
glycemic_index_dataset_path = 'food_GI.csv'
df_glycemic_index = pd.read_csv(glycemic_index_dataset_path)
insulin_index_dataset_path = 'Insulin_index.csv'
df_insulin_index = pd.read_csv(insulin_index_dataset_path)
df_glycemic_index = df_glycemic_index.dropna()
df_glycemic_index['Name'] = df_glycemic_index['Name'].str.lower()


def match_info_from_db(food_name):
    matched_food1, match_score1 = apipei(food_name, df_nutrient['Descrip'])
    matched_food2 = bpipei(food_name, df_glycemic_index['Name'])
    matched_food3 = bpipei(food_name, df_insulin_index['Name'])

    filtered_df1 = df_nutrient.loc[
        df_nutrient['Descrip'] == matched_food1, ['能量_千卡', '蛋白质_克', '脂肪_克', '碳水化合物_克', '糖_克',
                                                  '纤维_克', '维生素A_微克', '维生素B6_毫克', '维生素B12_微克',
                                                  '维生素C_毫克', '维生素E_毫克', '叶酸_微克', '烟酸_毫克',
                                                  '核黄素_毫克', '硫胺素_毫克', '钙_毫克', '铜_毫克', '铁_毫克',
                                                  '镁_毫克', '锰_毫克', '磷_毫克', '硒_微克', '锌_毫克',
                                                  '维生素A_推荐量', '维生素B6_推荐量', '维生素B12_推荐量',
                                                  '维生素C_推荐量', '维生素E_推荐量', '叶酸_推荐量', '烟酸_推荐量',
                                                  '核黄素_推荐量', '硫胺素_推荐量', '钙_推荐量', '铜_推荐量',
                                                  '镁_推荐量', '磷_推荐量', '硒_推荐量', '锌_推荐量']]
    filtered_df2 = df_glycemic_index[df_glycemic_index['Name'] == matched_food2]
    filtered_df3 = df_insulin_index[df_insulin_index['Name'] == matched_food3]
    return filtered_df1, filtered_df2, filtered_df3


def parse_nutri_info(nutri_info):
    rows = []
    for item in nutri_info.keys():
        row_content = []
        if not "推荐量" in item:
            nutrient = item.split("_")[0]  # 获取营养成分名
            unit = item.split("_")[1]
            current_value = nutri_info[item]  # to ceil
            if f"{nutrient}_推荐量" in nutri_info:
                recommended_value = nutri_info[f"{nutrient}_推荐量"]  # to ceil
            else:
                recommended_value = "无推荐数据"
            row_content.append(nutrient)
            row_content.append(current_value)
            row_content.append(recommended_value)
            row_content.append(unit)
            rows.append(row_content)
    result_dict = {
        "name": "能量供给",
        "score": 3.5,
        "scoreText": "这个食品非常适合你吃",
        "RowLabels": ["项目", "当前值", "建议值", "单位"],
        "RowContents": rows,
    }
    return result_dict


def parse_sugar_info(nutri_info, gi_info_list, ii_info_list):
    gi_info_row = ["GI(升糖指数)", gi_info_list[0]]
    ii_info_row = ["II(胰岛素指数)", ii_info_list[0]]
    carb_info_row = ["碳水化合物(克)", nutri_info["碳水化合物_克"]]
    sugar_info_row = ["糖(克)", nutri_info["糖_克"]]
    fiber_info_row = ["纤维(克)", nutri_info["纤维_克"]]
    result_dict = {
        "name": "糖代谢",
        "score": 4.5,
        "scoreLabel": "适合",
        "scoreText": "这个食品糖:",
        "RowLabels": ["项目", "值"],
        "RowContents": [gi_info_row, ii_info_row, carb_info_row, sugar_info_row, fiber_info_row]
    }
    return result_dict


def gen_result_detail(nutri_info_list, gi_info_list, ii_info_list):
    result_detail = [parse_nutri_info(nutri_info_list), parse_sugar_info(nutri_info_list, gi_info_list, ii_info_list)]
    return result_detail

def ask_llm(food_name, df1, df2, df3, user_info):
    nutri_info = df1.to_json(orient='records')
    GI_info = df2.to_json(orient='records')
    II_info = df3.to_json(orient='records')
    message = f"{food_name}（营养素信息：{nutri_info}，升糖指数：{GI_info}，胰岛素指数：{II_info}输出结果不需要显示）适合{user_info}的人吗？（只需要给出合理的建议）"
    response = ollama.chat(model='llama2-chinese', messages=[
        {
            'role': 'user',
            'content': message,
        },
    ])
    return response

def handle_food_info_get(food_name, user_info):
    filtered_df1, filtered_df2, filtered_df3 = match_info_from_db(food_name)
    nutri_info_list = filtered_df1.to_dict(orient='records')
    GI_info_list = filtered_df2['Glycemic index'].tolist()
    II_info_list = filtered_df3['Insulin index'].tolist()

    # user_info = input("请输入用户的个人信息 (包括年龄和所患疾病):\n")
    response = ask_llm(food_name, filtered_df1, filtered_df2, filtered_df3, user_info)

    output = {
        "result_detail": gen_result_detail(nutri_info_list, GI_info_list, II_info_list),
        "ai_response": response['message']['content']
    }
    print(json.dumps(output, indent=4, ensure_ascii=False))

handle_food_info_get("apple","42岁，糖尿病患者")