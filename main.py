import os
import re
from decimal import Decimal

import werobot
from werobot.logger import logger
from werobot.messages.messages import TextMessage

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
def hello(message: TextMessage):
    logger.info(f"message from {message.source} to {message.target} is {message.content} at {message.time}")
    query = re.findall('「(.*?)」',message.content)[0]
    material_response = request('taobao.tbk.dg.material.optional', {
        "adzone_id": os.getenv('TBK_ADZONE_ID'),
        "q": query
    }).json()
    result = next(result for result in material_response['result_list'] if result['title'] == query)
    money = Decimal(result['zk_final_price']) * Decimal(result['commission_rate']) / Decimal(10000)
    return f"商品名称: {query}\n商品价格: {result['zk_final_price']}\n商品返利: {money}"


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.config["APP_ID"] = os.getenv('WECHAT_OA_APP_ID')
robot.config['ENCODING_AES_KEY'] = os.getenv('WECHAT_OA_AES')
robot.run()
