import sqlite3 as sqlite
import sys

try:
    connection = sqlite.connect('sqlite-northwind.db')
    connection.text_factory = str
    cursor = connection.cursor()

    # Construct the query to be executed. We use a double INNER JOIN because Order-Details table is related to both
    # Orders and Products, therefore it's a middleware between the two.
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

    # Here we collect a dictionary of the order IDs and their occurrences, because for each occurrence of an order, it
    # means the order has another product type, with different product data, but the order data is the same.
    # Also, construct a general object for the current order, with an empty list, where we will put the data for the
    # different products of the order, later on.
    for record in raw_data:
        order_id = record[0]
        if order_id not in orders_occurrences:
            orders_occurrences[order_id] = 0
        orders_occurrences[order_id] += 1

        if record[0] not in data:
            data[record[0]] = {
                'Id': record[0],
                'ShipVia': record[1],
                'ShippedDate': record[2],
                'EmployeeId': record[3],
                'ShipCity': record[4],
                'ShipAddress': record[5],
                'ShipName': record[6],
                'ShipCountry': record[7],
                'OrderDate': record[8],
                'Products': []
            }

    # Loop through the result data from the DB and for each order, if it has occurred > 1, then append its product data
    # to the list of products
    for record in raw_data:
        order_id = record[0]
        if orders_occurrences[order_id] > 1:
            data[order_id]['Products'].append({
                'Id': record[11],
                'Name': record[13],
                'QuantityPerUnit': record[14],
                'UnitsInStock': record[12],
                'Quantity': record[9],
                'UnitPrice': record[10]
            })

    for order in data:
        print data[order]

except sqlite.Error, e:
    print e
    sys.exit(1)
finally:
    if connection:
        connection.close()
        print "--> Connection closed."
