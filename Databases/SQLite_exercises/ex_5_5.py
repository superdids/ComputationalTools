import sqlite3 as sqlite
import sys

try:
    connection = sqlite.connect('sqlite-northwind.db')
    # This does not work in windows.
    connection.text_factory = str
    # connection.text_factory = lambda x: str(x, 'latin1')
    cursor = connection.cursor()

    # Okay, so... cuz we wanted to show off, we made the whole job in a single query with nested SELECT statements.
    # Look at the query inside-out (from the last nested query towards the beginning). It goes like this:
    # first we get the IDs of the all customers that have ordered product with id=7. Then, this list of customer IDs we
    # feed to a query that gets the product IDs of all products that have been ordered by all these selected customers.
    # And at the end, we feed the resulted list of product IDs to the query that will get the names of all these ordered
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


    # Here we just format the resulted list of product names, because the cursor returns a list of sets, and we want
    # just the product names as separate strings. We push them into a list and print it out.
    # Then we print out the length of this list, which is in fact the number of distinct products ordered by customers
    # who have ordered also product with id=7.
    distinct_products = [p[0] for p in raw_data]
    print 'The number of different products: %d' % len(distinct_products)
    print 'A list of the products names: '
    print distinct_products

except sqlite.Error as e:
    print(e)
    sys.exit(1)

finally:
    if connection:
        connection.close()
        print("--> Connection closed.")
