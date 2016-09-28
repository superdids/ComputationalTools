import sqlite3 as sqlite
import sys

try:
    connection = sqlite.connect('sqlite-northwind.db')
    connection.text_factory = str
    cursor = connection.cursor()

    # Construct the query to be executed. We use a double INNER JOIN because Orders table is related to both
    # Customers and Order-Details, therefore it's a middleware between the two.
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

    # Here we initialize a dictionary with key = the customers' IDs and value = properties that we want to populate
    # later on, but for now with empty data.
    for record in raw_data:
        customer_id = record[1]
        if customer_id not in data:
            data[customer_id] = {
                'Name': None,
                'Company': None,
                'QuantityOrdered': 0
            }

    # Here we go through the data resulted from the query and populate the already initialized dict of customer objects.
    # Populate the name and company of the customer and accumulate the ordered quantity of the product.
    for record in raw_data:
        customer_id = record[1]
        for customer in data:
            if customer == customer_id:
                data[customer]['Name'] = record[3]
                data[customer]['Company'] = record[4]
                data[customer]['QuantityOrdered'] += record[2]

    for c in data:
        print (c, data[c])


except sqlite.Error, e:
    print e
    sys.exit(1)
finally:
    if connection:
        connection.close()
        print "--> Connection closed."
