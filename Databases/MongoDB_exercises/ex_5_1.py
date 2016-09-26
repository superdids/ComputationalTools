from pymongo import MongoClient

# Initialize a client object to connect to the MongoDB server
mongod = MongoClient()
# Connect to a certain DB (in our case we want the "Northwind" one)
db = mongod.Northwind

# Initialize an object for a certain document (table). In NoSQL type databases, the data is stored in documents, which
# could correlate to tables in relational databases. In the NoSQL cases, we can instantiate each of these documents as
# an object and query it for data.
customers = db.customers

# Find all records in the Customers doc (table)
data = customers.find()

# Return only the first 10 records
count = 0
while count < 10:
    print data[count]
    count += 1
