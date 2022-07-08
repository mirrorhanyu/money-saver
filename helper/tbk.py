import os
from datetime import datetime
from hashlib import md5
from urllib.parse import urlencode

import requests
from requests import Response

TBK_APP_SECRET = os.getenv("TBK_APP_SECRET")

P_APPKEY = "app_key"
P_METHOD = "method"
P_SESSION = "session"
P_VERSION = "v"
P_FORMAT = "format"
P_TIMESTAMP = "timestamp"
P_SIGN = "sign"
P_SIGN_METHOD = "sign_method"
P_PARTNER_ID = "partner_id"
P_SIMPLIFY = "simplify"


def request(method: str, param: dict) -> Response:
    public_param = {
        P_APPKEY: os.getenv("TBK_APPKEY"),
        P_FORMAT: 'json',
        P_VERSION: '2.0',
        P_TIMESTAMP: datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        P_SIGN_METHOD: 'md5',
        P_SIMPLIFY: 'true',
        P_PARTNER_ID: "new_python3_sdk"
    }
    public_param.update({
        P_METHOD: method
    })
    public_param.update(param)
    keys = list(public_param.keys())
    keys.sort()
    parameters = "%s%s%s" % (TBK_APP_SECRET,
                             "".join('%s%s' % (k, public_param[k]) for k in keys if not isinstance(public_param[k],bytes)),
                             TBK_APP_SECRET)
    sign = md5(parameters.encode("utf-8")).hexdigest().upper()
    public_param[P_SIGN] = sign
    url = "https://eco.taobao.com/router/rest" + "?" + urlencode(public_param)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8'
    }
    return requests.request("POST", url, headers=headers, data=param)
