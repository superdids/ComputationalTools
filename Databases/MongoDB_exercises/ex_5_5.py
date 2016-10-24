from pymongo import MongoClient

mongod = MongoClient()
db = mongod.Northwind

# Instantiate an object for each collection we are going to use
orders = db.orders
order_details = db['order-details']
products = db.products

# Query the Order Details for the records about Product with ID 7
# Construct a list of order IDs so that we know which orders to query for, so that we can find their customers
raw_data_order_details = order_details.find({'ProductID': 7})
orders_ids = [od['OrderID'] for od in raw_data_order_details]

# Get the listed orders above
# Construct a list of customers IDs, so we know which customers have made these orders, that are of product with ID 7
raw_data_orders = orders.find({'OrderID': {'$in': orders_ids}})
customers_ids = [c['CustomerID'] for c in raw_data_orders]

# Get all orders of all selected customers (from above) that have ordered product with id=7
orders_selected_customers = orders.find({'CustomerID': {'$in': customers_ids}})
orders_sel_cust_ids = [o['OrderID'] for o in orders_selected_customers]

# Get all order details of the above orders (for the selected customers)
order_details_selected_customers_orders = order_details.find({'OrderID': {'$in': orders_sel_cust_ids}})
products_sel_cust_ids = [od['ProductID'] for od in order_details_selected_customers_orders]

# Get all products from the above order details records (for the selected customers)
sel_prod_sel_cust = products.find({'ProductID': {'$in': products_sel_cust_ids}})

# Here we extract just the names of the selected products
distinct_products = [p['ProductName'] for p in sel_prod_sel_cust]

# Then we print out the list of distinct products, and its length, which is in fact the number of distinct products
# ordered by customers who have ordered also product with id=7.
print 'The number of different products: %d' % len(distinct_products)
print 'A list of the products names: '
print distinct_products
