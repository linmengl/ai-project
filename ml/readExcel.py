import os
import pandas as pd


def extract_columns_to_arrays(file_path, sheet_name=None, columns=None):
    """
    从 Excel 里提取指定列，返回 Python list 或 NumPy array

    参数：
        file_path: Excel 文件的路径
        sheet_name: 要读哪个 sheet（None 默认第一个）
        columns: 要提取的列名列表，例如 ['Name','Score']

    返回：
        dict，键是列名，值是 list 或 NumPy 数组；也可以返回一个二维数组（多列合并）
    """
    # 读 Excel，只拉指定列
    df = pd.read_excel(file_path, sheet_name=sheet_name, usecols=columns, engine='openpyxl')

    # 去掉含空值的行（如果你需要）
    df = df.dropna(subset=columns)

    # 准备结果
    result = {}

    for col in columns:
        # 方法 1：作为 Python list
        result[col] = df[col].tolist()

        # 如果你想要 NumPy array，可以用
        # result[col + '_array'] = df[col].to_numpy()

    # 如果你想把多个列合并为一个二维数组：
    # two_cols_array = df[columns].to_numpy()
    # result['combined'] = two_cols_array

    return result


if __name__ == "__main__":
    desktop = os.path.expanduser("~/Desktop")
    file_path = os.path.join(desktop, "宁波双主体历史数据.xlsx")

    cols = ['contract_code']
    arrays = extract_columns_to_arrays(file_path=file_path, sheet_name='Sheet1', columns=cols)

    print("Name 列为 list：", arrays['contract_code'])
    # 如果有 combined 就：
    # print("合并两列为二维 array：", arrays['combined'])