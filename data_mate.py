
import pymongo
import re
import matplotlib.pyplot as plt

"""
统计每个月的订单次数
"""
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['ele']
clo = db['info']

data = ['2018-02', '2018-03', '2018-04', '2018-05', '2018-06', '2018-07',
        '2018-08', '2018-09', '2018-10', '2018-11', '2018-12', '2019-01',
        '2019-02', '2019-03', '2019-04', '2019-05', '2019-06', '2019-07',
        '2019-08']

# 该月定外卖次数
count = []
for i in data:
    ele_count = clo.count({'created_timestamp': re.compile(i)})
    count.append(ele_count)

plt.scatter(data, count)

plt.xticks(rotation=45)
plt.show()





