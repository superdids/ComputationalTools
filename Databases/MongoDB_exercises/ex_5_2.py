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

# Construct a custom object with the main data from each order. The object is key: value, where key is the order's ID
# value is custom-picked data for the order.
# Also construct a list of the order IDs, so that we can query the Order-Details just for the certain orders.
for order in raw_data_orders:
    order_ids.append(order['OrderID'])
    data[order['OrderID']] = {
        'OrderId': order['OrderID'],
        'ShipVia': order['ShipVia'],
        'ShippedDate': order['ShippedDate'],
        'EmployeeId': order['EmployeeID'],
        'ShipCity': order['ShipCity'],
        'ShipAddress': order['ShipAddress'],
        'ShipName': order['ShipName'],
        'ShipCountry': order['ShipCountry'],
        'OrderDate': order['OrderDate'],
        'Product': {
            'Id': None,
            'Name': None,
            'QuantityPerUnit': None,
            'UnitsInStock': None,
            'Quantity': None,
            'UnitPrice': None
        }
    }

# Query the Order-Details collection for only certain Orders, by the IDs we collected earlier
raw_data_order_details = order_details.find({'OrderID': {'$in': order_ids}})
product_ids = []

# For each order details record store some data in its corresponding order in our key:value custom object
# Also construct a list of the products IDs, with the purpose to know which products to query
for details in raw_data_order_details:
    product_ids.append(details['ProductID'])
    data[details['OrderID']]['Product']['Id'] = details['ProductID']
    data[details['OrderID']]['Product']['Quantity'] = details['Quantity']
    data[details['OrderID']]['Product']['UnitPrice'] = details['UnitPrice']

# Query the Products collection for only certain products, by the IDs we collected earlier
# Then for each product, loop through the custom key:value object and if the product's ID matches the product ID of an
# order - save some more custom product data
raw_data_products = products.find({'ProductID': {'$in': product_ids}})
for product in raw_data_products:
    for order_id in data:
        if product['ProductID'] == data[order_id]['Product']['Id']:
            data[order_id]['Product']['Name'] = product['ProductName']
            data[order_id]['Product']['QuantityPerUnit'] = product['QuantityPerUnit']
            data[order_id]['Product']['UnitsInStock'] = product['UnitsInStock']

print data

"""
Comment of thoughts:

The Northwind data is not suitable for a NoSQL type of database, because the data in the different collections has very
strong relations between the collections. This makes it hard to query and join data from different collections, because
it most has to happen in the application layer.
The best case scenario for a NoSQL database is if the data is stored in a single collection, or different collections
do not depend on each other.
"""

