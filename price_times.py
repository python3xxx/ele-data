
import pymongo
import matplotlib.pyplot as plt

"""
订单价格趋势
"""
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['ele']
clo = db['info']

result = clo.find({})
y = [i['total_amount'] for i in result]
x = [i for i in range(len(y))]

plt.ylabel("The unit price")
plt.xlabel("Times")
plt.plot(x, y)
plt.show()

