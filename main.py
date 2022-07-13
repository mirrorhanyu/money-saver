import logging
import os
from decimal import Decimal

import werobot
from werobot.logger import logger

from helper.tbk import request

# url = "https:" + material_response['result_list'][0]['url']
# num_iid = material_response['result_list'][0]['num_iid']

# tkl_response = request('taobao.tbk.tpwd.create', {
#     "url": url,
#     "sub_pid": os.getenv('TBK_SUB_PID'),
# }).json()
#
# print(tkl_response.json()['data']['password_simple'])

robot = werobot.WeRoBot(token=os.getenv('WECHAT_OA_TOKEN'))


@robot.handler
def hello(message):
    return "hello world"


@robot.subscribe
def subscribe(message):
    return 'Hello My Friend!'


@robot.text
def hello(message):
    logger.info(message)
    query = "【老爸抽检】英氏婴幼儿维C加铁营养米粉辅食宝宝1段高铁米糊258g"
    material_response = request('taobao.tbk.dg.material.optional', {
        "adzone_id": os.getenv('TBK_ADZONE_ID'),
        "q": query
    }).json()
    result = next(result for result in material_response['result_list'] if result['title'] == query)
    money = Decimal(result['zk_final_price']) * Decimal(result['commission_rate']) / Decimal(10000)
    print("money get", money)
    return str(money)


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.config["APP_ID"] = os.getenv('WECHAT_OA_APP_ID')
robot.config['ENCODING_AES_KEY'] = os.getenv('WECHAT_OA_AES')
robot.run()
