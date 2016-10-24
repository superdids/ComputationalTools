from pymongo import MongoClient

mongod = MongoClient()
db = mongod.Northwind

# Instantiate an object for each collection we are going to use
orders = db.orders
order_details = db['order-details']
customers = db.customers
data = {}

# Query the Order Details for the records about Product with ID 7
# Construct a list of order IDs so that we know which orders to query for, so that we can find their customers
# Construct a dict where we store and accumulate the ordered quantity of the product, for each order
raw_data_order_details = order_details.find({'ProductID': 7})
orders_ids = []
details_data = {}
for details in raw_data_order_details:
    order_id = details['OrderID']
    orders_ids.append(order_id)
    if order_id not in details_data:
        details_data[order_id] = details['Quantity']
    else:
        details_data[order_id] += details['Quantity']

# Get the listed orders above
# Construct a list of customers IDs, so we know which customers have made these orders, that are of product with ID 7
# The global data object - populate with key = the ID of each customer, and values - name an company and quantity of
# the product ordered
raw_data_orders = orders.find({'OrderID': {'$in': orders_ids}})
customers_ids = []
for order in raw_data_orders:
    customer_id = order['CustomerID']
    if customer_id not in data:
        customers_ids.append(customer_id)
        data[customer_id] = {
            'Name': None,
            'Company': None,
            'QuantityOrdered': details_data[order['OrderID']]
        }

# Query the customers listed by ID above
# Populate the global data object with name and company of each customer
raw_data_customers = customers.find({'CustomerID': {'$in': customers_ids}})
for customer in raw_data_customers:
    data[customer['CustomerID']]['Name'] = customer['ContactName']
    data[customer['CustomerID']]['Company'] = customer['CompanyName']

for c in data:
    print (c, data[c])
