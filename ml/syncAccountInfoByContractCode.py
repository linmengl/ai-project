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



def retry_entry_task():
    taskIds = [163687,163787,174323,174335,174382,174465,177902,182770,208094,212955,221682,221704,221810,222080,231963]
    # taskIds = [163599,163609,163687,163787,174323,174335,174382,174465,177902,182770,208094,212955,221682,221704,221810,222080,231963]

    for taskId in taskIds:
        print("入账任务重试.taskId={}".format(taskId))
        response = requests.post(
            "http://xxx/backdoor/entryAccount/task/retry?entryTaskId="+str(taskId)
        )
        print(response.json().get("data"))
        print(response.json().get("traceId"))
        time.sleep(0.1)
        print("|")

def dataDeduplication(filename, fieldName):
    desktop = os.path.expanduser("~/Desktop")
    file_path = os.path.join(desktop, filename)
    cols = [fieldName]
    fields = readExcel.extract_columns_to_arrays(file_path=file_path, sheet_name='Sheet1', columns=cols)
    all_fields = fields[fieldName]
    print(len(all_fields))
    unique_elements = list(dict.fromkeys(all_fields))
    print(len(unique_elements))
    print(unique_elements)
    # return contractCodes['contract_code']

if __name__ == "__main__":
    # updateDoubleSubjectData4Invoice("xxx.xlsx")
    # getContractCode("资金监管失败合同.xlsx", "contract_code")
    # dataDeduplication("taskId.xlsx", "taskId")
    retry_entry_task()