import os

from helper.tbk import request

material_response = request('taobao.tbk.dg.material.optional', {
    "adzone_id": os.getenv('TBK_ADZONE_ID'),
    "q": "【老爸抽检】英氏婴幼儿维C加铁营养米粉辅食宝宝1段高铁米糊258g"
})

url = "https:" + material_response.json()['result_list'][0]['url']

tkl_response = request('taobao.tbk.tpwd.create', {
    "url": url,
    "sub_pid": os.getenv('TBK_SUB_PID'),
})

print(tkl_response.json()['data']['password_simple'])
