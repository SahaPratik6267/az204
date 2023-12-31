from flask import Flask, render_template
import pyodbc
import os

app = Flask(__name__)

# Define the Product class to represent product information
class Product:
    def __init__(self, product_id, name, price):
        self.product_id = product_id
        self.name = name
        self.price = price

@app.route('/')
def list_products():
    try:
        # Retrieve the Azure SQL Database connection string from the environment variable
        connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:pyptk-server.database.windows.net;Database=pyptk;Uid=sqladmin;Pwd=Testit123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

        print("Azure SQL Database Connection String:", connection_string)

        # Connect to the database using the retrieved connection string
        conn = pyodbc.connect(connection_string)

        # Create a cursor object to execute SQL queries
        cursor = conn.cursor()

        # Example SQL query to fetch product information (ID, name, and price)
        query = 'SELECT Id, Name, Price FROM Products'  # Modify this query to match your database schema
        cursor.execute(query)

        # Fetch all rows of data and create a list of Product objects
        products = []
        for row in cursor.fetchall():
            product = Product(row.Id, row.Name, row.Price)
            products.append(product)

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Render an HTML template and pass the list of Product objects
        return render_template('products.html', products=products)

    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
