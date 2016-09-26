from pymongo import MongoClient

mongod = MongoClient()
db = mongod.Northwind

orders = db['products']
data = orders.find()
print data[0]

# count = 0
# while count < 2:
#     print data[count]
#     count += 1
