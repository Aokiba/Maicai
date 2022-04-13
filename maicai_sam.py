import json
import requests
import sam_config
from datetime import date
import datetime


def get_capacity():
    url = 'https://api-sams.walmartmobile.cn/api/v1/sams/delivery/portal/getCapacityData'
    today = date.today()
    times_ = [today.strftime('%Y-%m-%d')]
    for i in range(6):
        time_ = today + datetime.timedelta(days=i)
        times_.append(time_.strftime('%Y-%m-%d'))
    data = {
        'storeDeliveryTemplateId': sam_config.template_id,
        'perDateList': times_
    }
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'latitude': sam_config.latitude,
        'device-type': 'ios',
        'auth-token': sam_config.token,
        'app-version': '5.0.47.0',
        'device-os-version': '15.1'
    }
    r = requests.post(url, data=json.dumps(data), headers=headers)
    txt = r.text
    abc = json.loads(txt).get("data")
    print(abc)


def getSettleInfo(d):
    url = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/settlement/getSettleInfo'
    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'latitude': sam_config.latitude,
        'device-type': 'ios',
        'auth-token': sam_config.token,
        'app-version': '5.0.47.0',
        'device-os-version': '15.1'
    }
    for i in range(10):
        r = requests.post(url, data=json.dumps(d), headers=headers)
        txt = r.text
        print(txt)


def queryUserCart():
    url = 'https://api-sams.walmartmobile.cn/api/v1/sams/trade/cart/getUserCart'
    d = {'uid': sam_config.uid, 'deliveryType': '0', 'deviceType': 'ios',
         'homePagelongitude': sam_config.longitude, 'homePagelatitude': sam_config.latitude,
         'parentDeliveryType': 1, 'storeList': [
            {'storeType': '32', 'storeId': '9991', 'areaBlockId': '42295',
             'storeDeliveryTemplateId': '1010425035346829590',
             'deliveryModeId': '1014'}, {'storeType': '2', 'storeId': '4807', 'areaBlockId': '300167894791270934',
                                         'storeDeliveryTemplateId': '305576603914796054', 'deliveryModeId': '1006'},
            {'storeType': '8', 'storeId': '9996', 'areaBlockId': '42295',
             'storeDeliveryTemplateId': '1147161263885953814',
             'deliveryModeId': '1010'}]
         }

    headers = {
        'Host': 'api-sams.walmartmobile.cn',
        'Connection': 'keep-alive',
        'Accept': '*/*',
        'Content-Type': 'application/json;charset=UTF-8',
        'latitude': sam_config.latitude,
        'device-type': 'ios',
        'auth-token': sam_config.token,
        'app-version': '5.0.47.0',
        'device-os-version': '15.1'
    }
    r = requests.post(url, data=json.dumps(d), headers=headers)
    txt = r.text
    abc = json.loads(txt).get("data")
    return abc


if __name__ == '__main__':
    # get_capacity()
    cart = queryUserCart()
    print(cart)
