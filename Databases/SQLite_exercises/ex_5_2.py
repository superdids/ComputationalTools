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

    # Here we construct a custom object to be returned, where we pick only some data from the result, just to make it
    # more readable and user-friendly. We could, by any means, return any data that is present in the result.
    # The result contains some main data about all orders and their products
    for index, record in enumerate(raw_data):
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
            'Product': {
                'Id': record[11],
                'Name': record[13],
                'QuantityPerUnit': record[14],
                'UnitsInStock': record[12],
                'Quantity': record[9],
                'UnitPrice': record[10]
            }
        }

    print data

except sqlite.Error, e:
    print e
    sys.exit(1)
finally:
    if connection:
        connection.close()
        print "--> Connection closed."
