import urllib

import requests
import json
import dd_config


def cart():
    url = "https://maicai.api.ddxq.mobi/cart/index?"
    map = {'uid': dd_config.uid, 'longitude': dd_config.longitude, 'latitude': dd_config.longitude,
           'station_id': dd_config.station_id, 'city_number': dd_config.city_number,
           'api_version': dd_config.api_version, 'app_version': dd_config.app_version,
           'is_load': 1
           }

    headers = {
        'Cookie': dd_config.cookie,
    }
    d = urllib.parse.urlencode(map)
    r = requests.get(url + d, headers=headers)
    txt = r.text
    data = json.loads(txt).get("data")
    products = data["product"]
    effective = products["effective"]
    res = []
    for i in effective:
        obj = i["products"]
        if obj:
            res = res + obj
    return res


def get_time(products):
    url = "https://maicai.api.ddxq.mobi/order/getMultiReserveTime"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'Cookie': dd_config.cookie,
    }
    product_list = []
    for i in products:
        product_item = {"type": 1, "id": i["id"], "price": i["price"], "count": i["count"], "description": "",
                        "sizes": i["sizes"], "cart_id": i["cart_id"], "activity_id": i["activity_id"],
                        "conditions_num": i["conditions_num"], "product_type": i["product_type"],
                        "small_image": i["small_image"], "price_type": i["price_type"], "sub_list": i["sub_list"],
                        "batch_type": -1, "total_origin_money": i["count"] * i["price"],
                        "product_name": i["product_name"], "is_booking": i["is_booking"],
                        "sale_batches": {'batch_type': -1}, "order_sort": "1", "supplementary_list": [], "is_gift": 0,
                        "is_presale": 0, "promotion_num": 0, "is_shared_station_product": 0, "buy_limit": 0,
                        "is_invoice": 1, "is_bulk": 0, "view_total_weight": 180, "net_weight": 90,
                        "net_weight_unit": "g", "storage_value_id": 3}
        # product_item["type"] = i["type"]
        # product_item["total_money"] = i["count"] * i["price"]
        product_item["instant_rebate_money"] = product_item["total_origin_money"]
        product_item["no_supplementary_price"] = product_item["total_origin_money"]
        product_item["no_supplementary_total_price"] = "0.00"
        product_list.append(product_item)
    obj1 = [product_list]
    map1 = {'uid': dd_config.uid, 'longitude': dd_config.longitude, 'latitude': dd_config.latitude,
            'station_id': dd_config.station_id, 'city_number': dd_config.city_number,
            'api_version': dd_config.app_version,
            'app_version': dd_config.app_version,
            'applet_source': '1', 'channel': 'applet', 'app_client_id': '4',
            'address_id': dd_config.address_id,
            'products': obj1,
            'isBridge': 'FALSE'
            }
    d = urllib.parse.urlencode(map1)
    r = requests.post(url, data=json.dumps(d), headers=headers)
    txt = r.text
    print(txt)
    abc = json.loads(txt).get("data")
    d = abc[0]
    time = d["time"][0]
    times = time["times"]
    for i in times:
        disable = i["disableType"]
        type = i["type"]
        if disable == 0 or type == 6:
            return i
    return times[-1]


def check_order(products, reserved_time):
    product_list = []
    total_money = ''
    total_origin_money = ''
    for i in products:
        product_item = {}
        a = i["count"] * i["price"]
        product_item["id"] = i["id"]
        product_item["count"] = i["count"]
        product_item["price"] = i["price"]
        product_item["total_money"] = i["count"] * i["price"]
        product_item["instant_rebate_money"] = 0
        product_item["activity_id"] = i["activity_id"]
        product_item["conditions_num"] = i["conditions_num"]
        product_item["product_type"] = i["product_type"]
        product_item["type"] = i["type"]
        product_item["total_origin_money"] = i["count"] * i["price"]
        product_item["price_type"] = i["price_type"]
        product_item["sub_list"] = i["sub_list"]
        product_item["batch_type"] = -1
        total_money = total_money + a
        total_origin_money = total_origin_money + a
        product_list.append(product_item)
    obj1 = []
    obj2 = {"products": product_list}
    obj1.append(obj2)
    url = "https://maicai.api.ddxq.mobi/order/checkOrder?"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'Cookie': dd_config.cookie
    }
    map = {'uid': dd_config.uid, 'longitude': dd_config.longitude, 'latitude': dd_config.latitude,
           'station_id': dd_config.station_id, 'city_number': dd_config.city_number,
           'api_version': dd_config.api_version,
           'app_version': dd_config.app_version, 'channel': 'applet', 'app_client_id': '4',
           'device_token': 'WHJMrwNw1k/F0qdLNvE01AVFfgrkgrbWMYyZ2CQTclYVwp6cRY65U1yQA2QAiEZ9V+o3V06MOq3jabgs980lh0tKcq04fB4AkdCW1tldyDzmauSxIJm5Txg==1487582755342',
           'address_id': dd_config.address_id, 'user_ticket_id': 'default', 'freight_ticket_id': 'default',
           'is_use_point': '0', 'is_use_balance': '0', 'is_buy_vip': '0', 'is_buy_coupons': '0',
           # 'packages': '[{"products":[{"id":"58b8d04e916edfb44cc26a9d","category_path":"58f9e539936edf89778b567f,58fa233c916edf7c198b4972","count":1,"price":"6.99","total_money":"6.99","instant_rebate_money":"0.00","activity_id":"","conditions_num":"","product_type":0,"sizes":[],"type":1,"total_origin_money":"6.99","price_type":0,"batch_type":-1,"sub_list":[],"order_sort":1,"origin_price":"6.99"}],"total_money":"6.99","total_origin_money":"6.99","goods_real_money":"6.99","total_count":1,"cart_count":1,"is_presale":0,"instant_rebate_money":"0.00","total_rebate_money":"0.00","used_balance_money":"0.00","can_used_balance_money":"0.00","used_point_num":0,"used_point_money":"0.00","can_used_point_num":0,"can_used_point_money":"0.00","is_share_station":0,"only_today_products":[],"only_tomorrow_products":[],"package_type":1,"package_id":1,"front_package_text":"即时配送","front_package_type":0,"front_package_stock_color":"#2FB157","front_package_bg_color":"#fbfefc","reserved_time":{"reserved_time_start":null,"reserved_time_end":null}}]',
           'packages': obj1,
           'check_order_type': '0', 'is_support_merge_payment': '1', 'showData': True, 'showMsg': False,
           'nars': 'dff13755f91eb92c02ccd524405eb5b6', 'sesi': 'W86ikEdf121e3c92b57f723e703ce6efa9347c6'}

    obj2 = {'total_money': total_money, 'total_origin_money': total_origin_money, 'goods_real_money': '6.99',
            'total_count': 1,
            'cart_count': 1, 'is_presale': 0, 'instant_rebate_money': '0.00', 'total_rebate_money': '0.00',
            'used_balance_money': '0.00', 'can_used_balance_money': '0.00', 'used_point_num': 0,
            'used_point_money': '0.00', 'can_used_point_num': 0, 'can_used_point_money': '0.00', 'is_share_station': 0,
            'only_today_products': [], 'only_tomorrow_products': [], 'package_type': 1, 'package_id': 1,
            'front_package_text': '即时配送', 'front_package_type': 0, 'front_package_stock_color': '#2FB157',
            'front_package_bg_color': '#fbfefc', 'products': product_list, 'reserved_time': reserved_time}
    obj1 = [obj2]
    map["packages"] = json.dumps(obj1)
    d = urllib.parse.urlencode(map)
    # 替换cookie
    r = requests.post(url, data=json.dumps(d), headers=headers)
    txt = r.text
    abc = json.loads(txt).get("data")
    return abc["order"]


def create_order(products, time, checked_order):
    product_list = []
    for i in products:
        product_item = {}
        product_item["id"] = i["id"]
        product_item["parent_id"] = ""
        product_item["count"] = i["count"]
        product_item["cart_id"] = i["cart_id"]
        product_item["price"] = i["price"]
        product_item["product_type"] = i["product_type"]
        product_item["small_image"] = i["small_image"]
        product_item["order_sort"] = 1
        product_item["sizes"] = i["sizes"]
        product_item["product_name"] = i["product_name"]
        product_item["is_booking"] = i["is_booking"]
        product_item["sale_batches"] = {'batch_type': -1}
        product_list.append(product_item)

    start_timestamp = time["reserved_time_start"]
    end_timestamp = time["reserved_time_end"]
    url = "https://maicai.api.ddxq.mobi/order/addNewOrder"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        'Cookie': dd_config.cookie
    }

    conf = {'key_onion': 'C'}
    map = {'uid': dd_config.uid, 'longitude': dd_config.longitude, 'latitude': dd_config.latitude,
         'station_id': dd_config.station_id, 'city_number': dd_config.city_number, 'api_version': dd_config.api_version,
         'app_version': dd_config.app_version, 'channel': 'applet', 'app_client_id': '4',
         's_id': '11891ec18707943ef93d105a605cfb0a',
         'address_id': dd_config.address_id, 'isBridge': False,
         'nars': 'bce3861c096a5571a0d512003c731e6b',
         'showData': True, 'showMsg': False, 'ab_config': conf,
         'sesi': 'SceJpIa5f0c7ebfbb5756064fc9f9a1a51ccf61'}

    payment_order = {'reserved_time_start': start_timestamp, 'reserved_time_end': end_timestamp,
                     'price': checked_order["total_money"],
                     'freight_discount_money': '5.00', 'freight_money': '5.00', 'order_freight': '0.00',
                     'parent_order_sign': '67977726a220be3223e2be1a3c301528', 'product_type': 1,
                     'address_id': dd_config.address_id,
                     'receipt_without_sku': 0, 'pay_type': 6, 'vip_money': '', 'vip_buy_user_ticket_id': '',
                     'coupons_money': '', 'coupons_id': ''}

    obj2 = {'total_money': checked_order["total_money"], 'total_origin_money': checked_order["goods_origin_money"],
            'goods_real_money': checked_order["goods_origin_money"], 'total_count': 1,
            'cart_count': 1, 'is_presale': 0, 'instant_rebate_money': '0.00', 'total_rebate_money': '0.00',
            'used_balance_money': '0.00', 'can_used_balance_money': '0.00', 'used_point_num': 0,
            'used_point_money': '0.00', 'can_used_point_num': 0, 'can_used_point_money': '0.00', 'is_share_station': 0,
            'package_type': 1, 'package_id': 1, 'front_package_text': '即时配送', 'front_package_type': 0,
            'front_package_stock_color': '#2FB157', 'front_package_bg_color': '#fbfefc',
            'eta_trace_id': '1649151696463734055150', 'reserved_time_start': start_timestamp,
            'reserved_time_end': end_timestamp, 'soon_arrival': '', 'first_selected_big_time': 0,
            'products': product_list}

    obj1 = {"payment_order": payment_order}
    obj3 = [obj2]
    obj1["packages"] = obj3

    map["package_order"] = json.dumps(obj1)
    d = urllib.parse.urlencode(map)
    r = requests.post(url, data=json.dumps(d), headers=headers)
    txt = r.text
    abc = json.loads(txt).get("data")
    print(abc)


if __name__ == '__main__':
    products = cart()
    time = get_time(products)
    print(time)
    reserved_time = {
        'reserved_time_start': time["start_timestamp"],
        'reserved_time_end': time["end_timestamp"]
    }
    checked_order = check_order(products, reserved_time)
    create_order(products, reserved_time, checked_order)
