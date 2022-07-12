import os
from decimal import Decimal

from helper.tbk import request

query = "【老爸抽检】英氏婴幼儿维C加铁营养米粉辅食宝宝1段高铁米糊258g"

material_response = request('taobao.tbk.dg.material.optional', {
    "adzone_id": os.getenv('TBK_ADZONE_ID'),
    "q": query
}).json()

result = next(result for result in material_response['result_list'] if result['title'] == query)

# url = "https:" + material_response['result_list'][0]['url']
# num_iid = material_response['result_list'][0]['num_iid']

print("money get", Decimal(result['zk_final_price']) * Decimal(result['commission_rate']) / Decimal(10000))

# tkl_response = request('taobao.tbk.tpwd.create', {
#     "url": url,
#     "sub_pid": os.getenv('TBK_SUB_PID'),
# }).json()
#
# print(tkl_response.json()['data']['password_simple'])
