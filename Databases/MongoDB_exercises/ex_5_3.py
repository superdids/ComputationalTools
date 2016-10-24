from pymongo import MongoClient

mongod = MongoClient()
db = mongod.Northwind

# Instantiate an object for each collection we are going to use
orders = db.orders
order_details = db['order-details']
products = db.products
data = {}

# Query the Orders collection for records that have 'ALFKI' value for the 'CustomerID' property
raw_data_orders = orders.find({'CustomerID': 'ALFKI'})
order_ids = []
orders_occurrences = {}

# Here we collect in a dictionary of the order IDs and their occurrences, because for each occurrence of an order, it
# means the order has another product type, with different product data, but the order data is the same.
# Also, construct a general object for the current order, with an empty list, where we will put the data for the
# different products of the order, later on.
# Also, construct a list of the order ids themselves, so we know for which orders to query the order details collection.
for order in raw_data_orders:
    order_id = order['OrderID']
    order_ids.append(order_id)
    if order_id not in orders_occurrences:
        orders_occurrences[order_id] = 0
    orders_occurrences[order_id] += 1

    if order_id not in data:
        data[order_id] = {
            'OrderId': order['OrderID'],
            'ShipVia': order['ShipVia'],
            'ShippedDate': order['ShippedDate'],
            'EmployeeId': order['EmployeeID'],
            'ShipCity': order['ShipCity'],
            'ShipAddress': order['ShipAddress'],
            'ShipName': order['ShipName'],
            'ShipCountry': order['ShipCountry'],
            'OrderDate': order['OrderDate'],
            'Products': {}
        }

raw_data_order_details = order_details.find({'OrderID': {'$in': order_ids}})
product_ids = []

# Add some data to each product of each order
for details in raw_data_order_details:
    product_ids.append(details['ProductID'])
    data[details['OrderID']]['Products'][details['ProductID']] = {
        'ProductId': details['ProductID'],
        'Quantity': details['Quantity'],
        'UnitPrice': details['UnitPrice']
    }

raw_data_products = products.find({'ProductID': {'$in': product_ids}})

# Add some data to each product of each order
for product in raw_data_products:
    for order_id in data:
        product_id = product['ProductID']
        if product_id in data[order_id]['Products']:
            data[order_id]['Products'][product_id]['Name'] = product['ProductName']
            data[order_id]['Products'][product_id]['QuantityPerUnit'] = product['QuantityPerUnit']
            data[order_id]['Products'][product_id]['UnitsInStock'] = product['UnitsInStock']

for o in data:
    print data[o]
