import sqlite3 as sqlite
import sys
import json

try:
    connection = sqlite.connect('sqlite-northwind.db')
    # This does not work in windows.
    # connection.text_factory = str
    connection.text_factory = lambda x: str(x, 'latin1')
    cursor = connection.cursor()

    sql = '''
            SELECT
            o.CustomerID, c.ContactName,od.ProductID, p.ProductName--or od.ProductId
            FROM 'Order details' od
            INNER JOIN Orders o ON o.OrderID = od.OrderID
            INNER JOIN Customers c ON c.CustomerID = o.CustomerID
            INNER JOIN Products p ON p.ProductId = od.ProductId
            '''

    cursor.execute(sql)
    raw_data = cursor.fetchall()

    data = {}

    # Populates the dictionaries with OrderID as key. Associates each order
    for record in raw_data:
        product_id = record[2]
        if record[0] not in data:
            data[record[0]] = {
                'ContactName': record[1],
                'Products': {}
            }
        data[record[0]]['Products'][product_id] = record[3]


    def condition(key):
        return 7 in data[key]['Products'] and len(data[key]['Products']) > 2


    # Retrieves every person that has ordered the product with id 7 as
    # as well as at least another product.
    data = {key: value for key, value in data.items() if condition(key)}

    def inner_comprehension():
        return {}

    # Now we collect every unique product that has been ordered.
    unique_products = {}
    for item in data:
        products = data[item]['Products']
        for product in products:
            unique_products[product] = products[product]

    # Remove the product with id 7.
    del unique_products[7]

    # Using json.dumps for simple formatting of dictionary/json-like data.
    print(json.dumps(unique_products, indent=4))

    # Prints the amount of unique products that have been ordered when also
    # ordering the product with id 7.
    print('Total different products: ', len(unique_products))

except sqlite.Error as e:
    print(e)
    sys.exit(1)

finally:
    if connection:
        connection.close()
        print("--> Connection closed.")
