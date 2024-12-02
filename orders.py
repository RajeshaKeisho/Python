# orders.py
class Order:
    def __init__(self, bakery):
        self.bakery = bakery
        self.cart = {}

    def add_to_cart(self, item_id, quantity):
        """Add items to the cart."""
        if item_id in self.bakery.inventory:
            item = self.bakery.inventory[item_id]
            if quantity <= item.stock:
                self.cart[item_id] = {'item': item, 'quantity': quantity}
                print(f"{quantity} {item.name}(s) added to the cart.")
            else:
                print(f"Only {item.stock} available in stock.")
        else:
            print("Item not found!")

    def remove_from_cart(self, item_id):
        """Remove an item from the cart."""
        if item_id in self.cart:
            del self.cart[item_id]
            print("Item removed from cart.")
        else:
            print("Item not found in the cart.")

    def generate_bill(self):
        """Generate bill for the customer."""
        total = 0
        print("\n--- Bill ---")
        for item_id, details in self.cart.items():
            item = details['item']
            quantity = details['quantity']
            cost = item.price * quantity
            print(f"{item.name}: {quantity} x {item.price} = {cost}")
            total += cost
            self.bakery.update_stock(item_id, quantity)
        
        print(f"Total Amount: {total}")
        print("Thank you for your purchase!\n")
        self.cart.clear()
