from pymongo import MongoClient
import sqlite3 as sqlite
import sys

class week_five:

    def __init_sqlite_connection(self):
        try:
            # Initialize connection to the DB (connection() method returns a connection
            # object)
            connection = sqlite.connect('sqlite-northwind.db')
            # Set the connection's text_factory to str. This will cause the connection
            # executor to return stings instead of automatically trying to decode the
            # str with the UTF-8 codec.
            #connection.text_factory = str

            # In Windows, the above code is not working, using 'latin1' encoding instead
            # does the trick
            connection.text_factory = lambda x: str(x, 'latin1')

            # Declare and initialize a cursor object to the connection, which will be
            # used to traverse the records returned
            cursor = connection.cursor()

            return cursor
        except sqlite.Error as e:
            print(e)
            sys.exit(1)

    def __init_mongo_connection(self):
        # Initialize a client object to connect to the MongoDB server
        mongod = MongoClient()
        # Connect to a certain DB (in our case we want the "Northwind" one)
        db = mongod.Northwind

        # Initialize an object for a certain document (table). In NoSQL type databases,
        # the data is stored in documents, which could correlate to tables in relational
        # databases. In the NoSQL cases, we can instantiate each of these documents as
        # an object and query it for data.
        return db

    def exercise_one_sqlite(self):
        cursor = self.__init_sqlite_connection()
        # Run a simple query to return the first 10 records from the "Customers" table,
        # just to test the connection
        cursor.execute('SELECT * FROM Customers LIMIT 10')

        # Get all returned records.
        data = cursor.fetchall()

        # Print the data records one by one, for better readability
        for record in data:
            # Only print CustomerID and ContactName.
            print(record[0], ' ', record[2])

        # Run a simple query to return the first 5 records from the "Products" table.
        cursor.execute('SELECT * FROM Products LIMIT 5')

        # Get all returned records.
        data = cursor.fetchall()

        # Print the data records one by one, for better readability
        for record in data:
            # Only print ProductID and ProductName.
            print(record[0], ' ', record[1])

    def exercise_one_mongo(self):
        db = self.__init_mongo_connection()

        # Initialize an object for a certain document (table). In NoSQL type
        # databases, the data is stored in documents, which could correlate
        # to tables in relational databases. In the NoSQL cases, we can instantiate
        # each of these documents as an object and query it for data.
        customers = db.customers

        # Find 10 records in the Customers doc (table)
        data = customers.find().limit(10)

        # Print the data records one by one, for better readability
        for item in data:
            print(item['CustomerID'], ' ', item['ContactName'])

        # Now we perform a query on the products document
        products = db.products

        # Find 5 records in the Products doc.
        data = products.find().limit(5)

        # Print the data records one by one, for better readability
        for item in data:
            print(item['ProductID'], ' ', item['ProductName'])


    def exersise_two_sqlite(self):
        cursor = self.__init_sqlite_connection()

        # Construct the query to be executed. We use a double INNER JOIN because
        # Order-Details table is related to both Orders and Products, therefore
        # it's a middleware between the two.
        sql = '''
                  SELECT
                  o.OrderId, o.ShipVia, o.ShippedDate, o.EmployeeId, o.ShipCity,
                  o.ShipAddress, o.ShipName, o.ShipCountry, o.OrderDate,
                  od.Quantity, od.UnitPrice,
                  p.ProductId, p.UnitsInStock, p.ProductName, p.QuantityPerUnit
                  FROM Orders o
                  INNER JOIN 'Order Details' od ON od.orderId = o.orderId
                  INNER JOIN Products p ON p.ProductId = od.ProductId
                  WHERE o.CustomerId = 'ALFKI';
                  '''
        cursor.execute(sql)
        raw_data = cursor.fetchall()
        data = {}

        # Here we construct a custom object to be returned, where we pick only
        # some data from the result, just to make it more readable and
        # user-friendly. We could, by any means, return any data that is present
        # in the result. The result contains some main data about all orders
        # and their products
        for index, record in enumerate(raw_data):
            data[record[0]] = {
                'ProductName': record[13]
            }

        # Outputs the data.
        for item in data:
            name = data[item]['ProductName']
            print('OrderID: ', item, ' ProductName: ', name)

    def exersise_two_mongo(self):
        db = self.__init_mongo_connection()

        # Instantiate an object for each collection we are going to use
        orders = db.orders
        order_details = db['order-details']
        products = db.products
        data = {}

        # Query the Orders collection for records that have 'ALFKI' value
        # for the 'CustomerID' property
        raw_data_orders = orders.find({'CustomerID': 'ALFKI'})
        order_ids = []

        # Construct a custom object with the main data from each order. The
        # object is key: value, where key is the order's ID value is
        # custom-picked data for the order. Also construct a list of the order
        # IDs, so that we can query the Order-Details just for the certain orders.
        for order in raw_data_orders:
            order_ids.append(order['OrderID'])
            data[order['OrderID']] = {
                'ProductID': None,
                'ProductName': None
            }

        # Query the Order-Details collection for only certain Orders, by the IDs
        # we collected earlier
        raw_data_order_details = order_details.find({'OrderID': {'$in': order_ids}})
        product_ids = []

        # For each order details record store some data in its corresponding order
        # in our key:value custom object. Also construct a list of the products IDs,
        # with the purpose to know which products to query
        for details in raw_data_order_details:
            product_ids.append(details['ProductID'])
            data[details['OrderID']]['ProductID'] = details['ProductID']

        # Query the Products collection for only certain products, by the IDs we
        # collected earlier. Then for each product, loop through the custom
        # key:value object and if the product's ID matches the product ID of an
        # order - save some more custom product data
        raw_data_products = products.find({'ProductID': {'$in': product_ids}})
        for product in raw_data_products:
            for order_id in data:
                if product['ProductID'] == data[order_id]['ProductID']:
                    data[order_id]['ProductName'] = product['ProductName']

        # Outputs the data.
        for item in data:
            name = data[item]['ProductName']
            print('OrderID: ', item, ' ProductName: ', name)

    def exersise_three_sqlite(self):
        cursor = self.__init_sqlite_connection()

        # Construct the query to be executed. We use a double INNER JOIN because
        # Order-Details table is related to both Orders and Products, therefore
        # it's a middleware between the two.
        sql = '''
                  SELECT
                  o.OrderId, o.ShipVia, o.ShippedDate, o.EmployeeId, o.ShipCity,
                  o.ShipAddress, o.ShipName, o.ShipCountry, o.OrderDate,
                  od.Quantity, od.UnitPrice,
                  p.ProductId, p.UnitsInStock, p.ProductName, p.QuantityPerUnit
                  FROM Orders o
                  INNER JOIN 'Order Details' od ON od.orderId = o.orderId
                  INNER JOIN Products p ON p.ProductId = od.ProductId
                  WHERE o.CustomerId = 'ALFKI';
                  '''
        cursor.execute(sql)
        raw_data = cursor.fetchall()
        data = {}
        orders_occurrences = {}

        # Here we collect a dictionary of the order IDs and their occurrences,
        # because for each occurrence of an order, it means the order has another
        # product type, with different product data, but the order data is the same.
        # Also, construct a general object for the current order, with an empty list,
        # where we will put the data for the different products of the order, later on.
        for record in raw_data:
            order_id = record[0]
            if order_id not in orders_occurrences:
                orders_occurrences[order_id] = 0
            orders_occurrences[order_id] += 1

            if record[0] not in data:
                data[record[0]] = {
                    'Id': record[0],
                    'Products': []
                }


        # Loop through the result data from the DB and for each order, if it has
        # occurred > 1, then append its product data to the list of products
        for record in raw_data:
            order_id = record[0]
            if orders_occurrences[order_id] > 1:
                data[order_id]['Products'].append({
                      'Id': record[11],
                       'Name': record[13]
                 })
            else:
                del data[order_id]

        # Output the data
        for order_id in data:
            print('OrderID: ',  order_id, ', Products: ')
            products = data[order_id]['Products']
            for product in products:
                print('\t', product['Id'], ' ', product['Name'])


    def exersise_three_mongo(self):
        db = self.__init_mongo_connection()

        # Instantiate an object for each collection we are going to use
        orders = db.orders
        order_details = db['order-details']
        products = db.products
        data = {}

        # Query the Orders collection for records that have 'ALFKI' value for the
        # 'CustomerID' property
        raw_data_orders = orders.find({'CustomerID': 'ALFKI'})
        order_ids = []
        orders_occurrences = {}

        # Here we collect in a dictionary of the order IDs and their occurrences,
        # because for each occurrence of an order, it means the order has another
        # product type, with different product data, but the order data is the same.
        # Also, construct a general object for the current order, with an empty list,
        # where we will put the data for the different products of the order, later
        # on. Also, construct a list of the order ids themselves, so we know for
        # which orders to query the order details collection.
        for order in raw_data_orders:
            order_id = order['OrderID']
            order_ids.append(order_id)
            if order_id not in orders_occurrences:
                orders_occurrences[order_id] = 0
            orders_occurrences[order_id] += 1

            if order_id not in data:
                data[order_id] = {
                    'Products': {}
                }

        raw_data_order_details = order_details.find({'OrderID': {'$in': order_ids}})
        product_ids = []

        # Add some data to each product of each order
        for details in raw_data_order_details:
            product_ids.append(details['ProductID'])
            data[details['OrderID']]['Products'][details['ProductID']] = {
                'ProductId': details['ProductID']
            }

        raw_data_products = products.find({'ProductID': {'$in': product_ids}})

        # Add some data to each product of each order
        for product in raw_data_products:
            for order_id in data:
                product_id = product['ProductID']
                if product_id in data[order_id]['Products']:
                    data[order_id]['Products'][product_id]['Name'] = product['ProductName']

        # Only include orders with 2 or more products. data.items() returns each
        # key-value correspondence as tuples, which implies that
        # we need to retrieve the second item of the tuple for comparisons.
        data = dict(filter(lambda x: len(x[1]['Products']) > 1, data.items()))

        # Output the data
        for order_id in data:
            print('OrderID: ', order_id, ', Products: ')
            products = data[order_id]['Products']
            for product_id in products:
                product = products[product_id]
                print('\t', product['ProductId'], ' ', product['Name'])

    def exersise_four_sqlite(self):
        cursor = self.__init_sqlite_connection()
        # Construct the query to be executed. We use a double INNER JOIN
        # because Orders table is related to both Customers and Order-Details,
        # therefore it's a middleware between the two.
        sql = '''
                  SELECT
                  o.OrderId, o.CustomerId,
                  od.Quantity,
                  c.ContactName, c.CompanyName
                  FROM 'Order Details' od
                  INNER JOIN Orders o ON o.orderId = od.orderId
                  INNER JOIN Customers c ON c.CustomerId = o.CustomerId
                  WHERE od.ProductId = 7;
                  '''
        cursor.execute(sql)
        raw_data = cursor.fetchall()
        data = {}

        # Here we initialize a dictionary with key = the customers' IDs and
        # value = properties that we want to populate later on, but for now
        # with empty data.
        for record in raw_data:
            customer_id = record[1]
            if customer_id not in data:
                data[customer_id] = {
                    'Name': None
                }

        # Here we go through the data resulted from the query and populate
        # the already initialized dict of customer objects. Populate the
        # name and company of the customer and accumulate the ordered
        # quantity of the product.
        for record in raw_data:
            customer_id = record[1]
            for customer in data:
                if customer == customer_id:
                    data[customer]['Name'] = record[3]

        # Output the results
        for c in data:
            print(c, ' ', data[c]['Name'])
        print('Total orders of \"Uncle Bob\'s Organic dried pears\": ', len(data))

    def exersise_four_mongo(self):
        db = self.__init_mongo_connection()

        orders = db.orders
        order_details = db['order-details']
        customers = db.customers
        data = {}

        # Query the Order Details for the records about Product with ID 7
        # Construct a list of order IDs so that we know which orders to
        # query for, so that we can find their customers. Construct a
        # dict where we store and accumulate the ordered quantity of the
        # product, for each order
        raw_data_order_details = order_details.find({'ProductID': 7})
        orders_ids = []
        details_data = {}
        for details in raw_data_order_details:
            order_id = details['OrderID']
            orders_ids.append(order_id)

        # Get the listed orders above
        # Construct a list of customers IDs, so we know which customers
        # have made these orders, that are of product with ID 7. The global
        # data object - populate with key = the ID of each customer, and
        # values - name an company and quantity of the product ordered
        raw_data_orders = orders.find({'OrderID': {'$in': orders_ids}})
        customers_ids = []
        for order in raw_data_orders:
            customer_id = order['CustomerID']
            if customer_id not in data:
                customers_ids.append(customer_id)
                data[customer_id] = {
                    'Name': None
                }

        # Query the customers listed by ID above
        # Populate the global data object with name and company of each customer
        raw_data_customers = customers.find({'CustomerID': {'$in': customers_ids}})
        for customer in raw_data_customers:
            data[customer['CustomerID']]['Name'] = customer['ContactName']

        # Output the results
        for c in data:
            print(c, ' ', data[c]['Name'])
        print('Total orders of \"Uncle Bob\'s Organic dried pears\": ', len(data))


    def exersise_five_sqlite(self):
        cursor = self.__init_sqlite_connection()

        # We made the whole job in a single query with nested SELECT statements.
        # Look at the query inside-out (from the last nested query towards the
        # beginning). It goes like this: First we get the IDs of the all customers
        # that have ordered product with id=7. Then, this list of customer IDs we
        # feed to a query that gets the product IDs of all products that have been
        # ordered by all these selected customers. And at the end, we feed the resulted
        # list of product IDs to the query that will get the names of all these ordered
        # products.
        sql = '''
                SELECT ProductName
                FROM Products
                WHERE ProductId IN (
                    SELECT od.ProductId
                    FROM 'Order Details' od
                    INNER JOIN Orders o ON o.OrderId = od.OrderId
                    WHERE o.CustomerId IN (
                        SELECT o.CustomerId
                          FROM Orders o
                          INNER JOIN 'Order Details' od ON o.orderId = od.orderId
                          WHERE od.ProductId = 7))
                ;
                '''

        cursor.execute(sql)
        raw_data = cursor.fetchall()

        # Here we just format the resulted list of product names, because the
        # cursor returns a list of sets, and we want just the product names
        # as separate strings. We push them into a list and print it out.
        # Then we print out the length of this list, which is in fact the
        # number of distinct products ordered by customers who have ordered
        # also product with id=7.
        distinct_products = [p[0] for p in raw_data]
        print('The number of different products: %d' % len(distinct_products))
        print('A list of the products names: ')
        for item in distinct_products:
            print('\t', item)

    def exersise_five_mongo(self):
        db = self.__init_mongo_connection()
        # Instantiate an object for each collection we are going to use
        orders = db.orders
        order_details = db['order-details']
        products = db.products

        # Query the Order Details for the records about Product with ID 7
        # Construct a list of order IDs so that we know which orders to
        # query for, so that we can find their customers
        raw_data_order_details = order_details.find({'ProductID': 7})
        orders_ids = [od['OrderID'] for od in raw_data_order_details]

        # Get the listed orders above
        # Construct a list of customers IDs, so we know which customers
        # have made these orders, that are of product with ID 7
        raw_data_orders = orders.find({'OrderID': {'$in': orders_ids}})
        customers_ids = [c['CustomerID'] for c in raw_data_orders]

        # Get all orders of all selected customers (from above) that have
        # ordered product with id=7
        orders_selected_customers = orders.find({'CustomerID': {'$in': customers_ids}})
        orders_sel_cust_ids = [o['OrderID'] for o in orders_selected_customers]

        # Get all order details of the above orders (for the selected customers)
        order_details_selected_customers_orders = order_details.find({'OrderID': {'$in': orders_sel_cust_ids}})
        products_sel_cust_ids = [od['ProductID'] for od in order_details_selected_customers_orders]

        # Get all products from the above order details records (for the
        # selected customers)
        sel_prod_sel_cust = products.find({'ProductID': {'$in': products_sel_cust_ids}})

        # Here we extract just the names of the selected products
        distinct_products = [p['ProductName'] for p in sel_prod_sel_cust]

        # Then we print out the list of distinct products, and its length,
        # which is in fact the number of distinct products
        # ordered by customers who have ordered also product with id=7.
        print('The number of different products: %d' % len(distinct_products))
        print('A list of the products names: ')
        for item in distinct_products:
            print('\t', item)

week_five().exersise_five_mongo()