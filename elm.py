

"""
获取饿了么订单数据信息
"""
import requests
import pymongo

requests.packages.urllib3.disable_warnings()

#  mongo配置
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['ele']
clo = db['info']

# _banxia
headers = {
    'Cookie': '换成你的Cookie'
}
# user_id = 26802499
user_id = '你的user_id' # _banxia
limit = 8


# 近3个月订单
url = f'https://h5.ele.me/restapi/bos/v2/users/{user_id}/orders'

# 3个月之后的订单
old_url = f'https://h5.ele.me/restapi/bos/v2/users/{user_id}/old_orders'

import time

def time_convert(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))


import re
def clean_data(data):
    a = re.sub("\\(.*?\\)|\\（.*?\\）|\\[.*?\\]|\\【.*?\\】|[A-Za-z0-9\@\\!\/]", "", data)
    a = a.replace('盒', '').replace('克', '').replace('个', '')\
        .replace('大份', '').replace('小份', '').replace('瓶', '').replace('组', '').replace(' ','')
    return a


# 统计订单总金额
total = 0

def insert_mongo(resp_json):
    if not resp_json:
        return
    for i in resp_json:
        # 菜品
        foods_group = i['basket']['group'][0]
        for j in foods_group:
            j['name'] = clean_data(j['name'])
            with open('foods_name.txt', 'a+') as f:
                f.write(j['name'] + '\n')
        # 配送费
        deliver_price = 0
        if 'deliver_fee' in i['basket'].keys():
            deliver_price = i['basket']['deliver_fee']['price']
        # 计算总花费
        global total
        total += i['total_amount']

        # 餐馆名
        restaurant_name = clean_data(i['restaurant_name'])

        with open('restaurant_name.txt', 'a+') as f:
            f.write(restaurant_name + '\n')

        clo.insert_one({
            # 餐馆名
            'restaurant_name': restaurant_name,
            # 订单时间  formatted_created_at也可以取，但是近期的会显示xx小时之前
            'created_timestamp': time_convert(i['created_timestamp']),
            # 价格
            'total_amount': i['total_amount'],
            'foods_group': foods_group,
            'deliver_price': deliver_price
        })

"""
 获取近3个月订单
"""
def get_new_order():
    num = 0
    while 1:
        # 偏移量
        offset = num * limit
        response = requests.get(url + f'?limit={limit}&offset={offset}', headers=headers, verify=False)
        resp_json = response.json()
        insert_mongo(resp_json)
        # 当响应订单数小于8时 跳出循环
        if len(resp_json) < 8:
            print('====================')
            break
        num += 1


"""
历史订单
"""
def history_order():
    from_time = ''
    while 1:
        response = requests.get(old_url + f'?limit={limit}&from_time={from_time}', headers=headers, verify=False)
        resp_json = response.json()
        from_time = resp_json['from_time']
        orders = resp_json['orders']
        # 经过测试，最后一个订单时，会在请求一次 响应为空
        if not orders:
            break
        insert_mongo(orders)

if __name__ == '__main__':
    get_new_order()
    print('^^^^^^^^^^^^^^^^^^^^^^^^^')
    history_order()
    print(f'本次统计你在饿了么平台定外卖总共花费了{total}元')














