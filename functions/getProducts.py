import azure.functions as func
import logging
import pyodbc

from flask import json

app = func.FunctionApp(http_auth_level=func.AuthLevel.FUNCTION)

@app.route(route="getProduct")
def getProducts(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    try:
        # Retrieve the Azure SQL Database connection string from an application setting
        connection_string = 'Driver={ODBC Driver 18 for SQL Server};Server=tcp:pyptk-server.database.windows.net,1433;Database=pyptk;Uid=sqladmin;Pwd=Testit123;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;'

        # Connect to the database using the retrieved connection string
        conn = pyodbc.connect(connection_string)
        cursor = conn.cursor()

        # Example SQL query to fetch product information (ID, name, and price)
        query = 'SELECT Id, Name, Price FROM Products'  # Modify this query to match your database schema
        cursor.execute(query)

        # Fetch all rows of data and create a list of Product objects
        products = []
        for row in cursor.fetchall():
            product = {
                "product_id": row.Id,
                "name": row.Name,
                "price": row.Price
            }
            products.append(product)

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Return the list of products as JSON response
        return func.HttpResponse(body=json.dumps(products), mimetype="application/json", status_code=200)

    except Exception as e:
        return func.HttpResponse(body=str(e), status_code=500)
