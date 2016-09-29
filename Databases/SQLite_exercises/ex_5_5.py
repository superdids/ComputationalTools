import sqlite3 as sqlite
import sys
try:
    connection = sqlite.connect('sqlite-northwind.db')
    # This does not work in windows.
    #connection.text_factory = str
    connection.text_factory = lambda x: str(x, 'latin1')
    cursor = connection.cursor()

    sql =   '''

            SELECT
            o.orderId, o.CustomerId, c.ContactName,od.ProductId --or od.ProductId
            FROM 'Order details' od
            INNER JOIN Orders o ON o.orderId = od.orderId
            INNER JOIN Customers c ON c.CustomerId = o.CustomerId
            '''


    cursor.execute(sql)
    raw_data = cursor.fetchall()
    # Dictionary with orders that has been placed for product with ID 7.
    data_with = {}
    # Dictionary with orders that have been placed for another product ID than 7.
    data_without = {}

    # Here we initialize a dictionary with key=orderId and value=ProductId,
    # CustomerId and ContactName (and product name).
    for record in raw_data:
        order_id = record[0]
        product_id = record[3]
        obj = {
            'CustomerId': record[1],
            'ContactName': record[2],
            'ProductId': record[3]
        }
        if product_id == 7:
            data_with[order_id] = obj
        else:
            data_without[order_id] = obj

    result = {}
    for key in data_without:
        if key in data_with:
            result[key] = data_without[key]


    # Prints each customer that has ordered another product besides product id 7.
    for index in result:
        print(result[index])


    # Prints the amount of distinct products that customers have ordered besides
    # product id 7.
    distinct_products_count = len({result[key]['ProductId'] for key in result})

    print(distinct_products_count)


except sqlite.Error as e:
    print(e)
    sys.exit(1)

finally:
    if connection:
        connection.close()
        print("--> Connection closed.")