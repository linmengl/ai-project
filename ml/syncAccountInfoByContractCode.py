import time

import requests

# contractCodes = ["xxx"]
#
# for contract in contractCodes:
#     print("同步贝易转账号.contractCode={}".format(contract))
#     response = requests.post(
#         "xxx"
#         , json=[contract]
#     )
#     print(response.json().get("traceId"))
#     time.sleep(3)
#     print("｜")




contractCodes = [""]

for contract in contractCodes:
    print("ka1.0合同变更.contractCode={}".format(contract))
    response = requests.post(
        "xxx?contractCodes="+contract
    )
    print(response.json().get("data"))
    print(response.json().get("traceId"))
    time.sleep(2)
    print("｜")