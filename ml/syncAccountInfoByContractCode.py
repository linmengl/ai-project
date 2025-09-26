import time
import os
import requests
import readExcel

'''
发票开城：处理历史双主体实收数据
'''
def updateDoubleSubjectData4Invoice(filename):
    desktop = os.path.expanduser("~/Desktop")
    file_path = os.path.join(desktop, filename)
    cols = ['contract_code']
    contractCodes = readExcel.extract_columns_to_arrays(file_path=file_path, sheet_name='Sheet1', columns=cols)
    # contractCodes = ["TGCF2410196440"]

    for contract in contractCodes['contract_code']:
        print("处理历史双主体实收数据.contractCode={}".format(contract))
        response = requests.get(
            "http://xxx/processDoubleSubjectHistoryPaid?contractCode="+contract
        )
        print(response.json().get("data"))
        print(response.json().get("traceId"))
        time.sleep(0.1)
        print("|")


if __name__ == "__main__":
    updateDoubleSubjectData4Invoice("宁波双主体历史数据.xlsx")