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
    logger.info(f"message from {message.source} to {message.target} is {message.content} at {message.time} \n")
    query = re.findall('「(.*?)」',message.content)[0]
    material_response = request('taobao.tbk.dg.material.optional', {
        "adzone_id": os.getenv('TBK_ADZONE_ID'),
        "q": query
    }).json()
    result = next(result for result in material_response['result_list'] if result['title'] == query)
    logger.info(f"{result} \n")
    cost = Decimal(result['zk_final_price']) if result.get('coupon_amount') is None else Decimal(result['zk_final_price']) - Decimal(result['coupon_amount'])
    money = cost * Decimal(result['commission_rate']) / Decimal(10000)
    url = "https:" + material_response['result_list'][0]['url']
    coupon_share_url = "https:" + result['coupon_share_url']
    logger.info(f"request passcode with {coupon_share_url or url}")
    tkl_response = request('taobao.tbk.tpwd.create', {
        "url": coupon_share_url if result['coupon_share_url'] != "" else url,
        "sub_pid": os.getenv('TBK_SUB_PID'),
    }).json()
    kouling = tkl_response['data']['password_simple']
    return f"商品名称: {query}\n商品价格: {result['zk_final_price']}\n商品返利: {money}\n商品口令: {kouling}\n\n长按复制整条消息，然后打开淘宝即可。"


robot.config['HOST'] = '0.0.0.0'
robot.config['PORT'] = 80
robot.config["APP_ID"] = os.getenv('WECHAT_OA_APP_ID')
robot.config['ENCODING_AES_KEY'] = os.getenv('WECHAT_OA_AES')
robot.run(server='waitress')
