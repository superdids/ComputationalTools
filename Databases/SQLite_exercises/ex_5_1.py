import sqlite3 as sqlite
import sys

try:
    # Initialize connection to the DB (connection() method returns a connection object)
    connection = sqlite.connect('sqlite-northwind.db')
    # Set the connection's text_factory to str. This will cause the connection executor to return stings instead of
    # automatically trying to decode the str with the UTF-8 codec.
    connection.text_factory = lambda x: str(x, 'latin1') #str

    # Declare and initialize a cursor object to the connection, which will be used to traverse the records returned
    cursor = connection.cursor()
    # Run a simple query to return the first 10 records from the "Customers" table, just to test the connection
    cursor.execute('SELECT * FROM Customers LIMIT 10')
    # Get all returned records.
    data = cursor.fetchall()

    # Print the data records one by one, for better readability
    for record in data:
        print (record)

# If the connection fails or any other error occurs - return it
except sqlite.Error as e:
    print (e)
    sys.exit (1)

# When everything is done - close the connection
finally:
    if connection:
        connection.close()
        print ("--> Connection closed.")
