# bakery.py
from items import BakeryItem
from db import get_db_connection


class Bakery:
    def __init__(self):
        self.inventory = {}

    def add_item(self, item):
        """Add a new item to the bakery inventory."""
        self.inventory[item.item_id] = item

    def remove_item(self, item_id):
        """Remove an item from the inventory."""
        if item_id in self.inventory:
            del self.inventory[item_id]
            print(f"Item with ID {item_id} removed from inventory.")
        else:
            print("Item not found!")

    def update_stock(self, item_id, quantity):
        """Update stock for an item."""
        if item_id in self.inventory:
            self.inventory[item_id].update_stock(quantity)
        else:
            print("Item not found!")

    def display_inventory(self):
        """Display all items in the inventory."""
        for item in self.inventory.values():
            print(item)

    @staticmethod
    def get_item_by_id(item_id):
        """Fetch an item by ID from the database."""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, name, price, stock FROM items WHERE id = %s", (item_id,))
        item = cursor.fetchone()
        cursor.close()
        connection.close()
        return item
