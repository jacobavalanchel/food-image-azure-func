import pandas as pd
import json

data = pd.read_csv(r"中国居民蛋白质推荐量.csv")


def get_age_range(age):
    if age < 0.5:
        return '0~'
    elif age < 1:
        return '0.5~'
    elif age < 4:
        return '1~'
    elif age < 7:
        return '4~'
    elif age < 11:
        return '7~'
    elif age < 14:
        return '11~'
    elif age < 18:
        return '14~'
    elif age < 60:
        return '18~'
    else:
        return '60~'


def ear_rni_info(age_range, gender):
    try:
        matched_rows = data[data['年龄(岁)/生理状况'].str.contains(age_range)]
        if len(matched_rows) == 0:
            raise ValueError("输入的年龄不在数据集中，请检查。")
        else:
            if gender == "男":
                EAR = matched_rows.iloc[0, 1]
                RNI = matched_rows.iloc[0, 2]
            elif gender == "女":
                EAR = matched_rows.iloc[0, 3]
                RNI = matched_rows.iloc[0, 4]
            else:
                raise ValueError("输入的性别有误，请检查。")
        return EAR, RNI
    except ValueError as e:
        print(e)
    except Exception as e:
        print("发生了一个错误：", e)


def main():
    user_age = input("请输入年龄：\n")
    user_gender = input("请输入性别：\n")
    age = float(user_age)

    age_range = get_age_range(age)
    EAR, RNI = ear_rni_info(age_range, user_gender)

    output = {
        "EAR": EAR,
        "RNI": RNI
    }
    print(json.dumps(output, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    main()
