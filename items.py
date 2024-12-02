# items.py
from db import get_db_connection
import mysql.connector
from reports import Reports



class BakeryItem:
    def __init__(self, name, price, stock):
        self.name = name
        self.price = price
        self.stock = stock

    def add_to_db(self):
        """Add item to the MySQL database."""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute(
            "INSERT INTO items (name, price, stock) VALUES (%s, %s, %s)",
            (self.name, self.price, self.stock)
        )
        connection.commit()
        cursor.close()
        connection.close()

    def update_stock(self, quantity, price):
        """Update stock of an item and record the sale."""
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            # Update stock
            cursor.execute(
                "UPDATE items SET stock = stock - %s WHERE name = %s AND stock >= %s",
                (quantity, self.name, quantity)
            )
            if cursor.rowcount == 0:
                print("Error: Insufficient stock or item not found.")
                return

            connection.commit()

            # Record sale
            reports = Reports()  # Ensure Reports object is accessible
            reports.add_sale(self.name, quantity, price)
            print("Stock updated and sale recorded successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    @staticmethod
    def get_item(name):
        """Fetch an item by name from the database."""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, price, stock FROM items WHERE name = %s", (name,))
        item = cursor.fetchone()
        cursor.close()
        connection.close()
        return item

    @staticmethod
    def get_item_by_id(item_id):
        """Fetch an item by its ID from the database."""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, price, stock FROM items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()
        connection.close()
        return item

    @staticmethod
    def display_inventory():
        """Display all items in the inventory."""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, price, stock FROM items")
        for (id, name, price, stock) in cursor:
            print(f"ID: {id}, Name: {name}, Price: {price}, Stock: {stock}")
        cursor.close()
        connection.close()
