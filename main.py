from items import BakeryItem
from reports import Reports
from auth import Authentication
from bakery import Bakery

def main():
    # Initialize modules
    reports = Reports()  # Create an instance of the Reports class
    auth = Authentication()
    cart = {}  # Initialize an empty cart
    logged_in = False  # Track if the user is logged in
    user_role = None  # User role will be stored once logged in

    while True:
        print("\n--- Bakery Management ---")
        print("1. Register\n2. Login\n3. Add Item\n4. Update Stock\n5. Sales Report\n6. Custom Report")
        print("7. Display Inventory\n8. Remove Item\n9. Add to Cart\n10. Remove from Cart")
        print("11. Generate Bill\n12. Logout\n13. Exit")

        choice = input("Select an option: ")

        # Option to Register
        if choice == '1':
            username = input("Username: ")
            password = input("Password: ")
            role = input("Role (cashier/manager): ")
            auth.register(username, password, role)

        # Option to Login
        elif choice == '2':  # Login
            username = input("Username: ")
            password = input("Password: ")
            if auth.login(username, password):  # First check if login is successful
                logged_in = True
                user_role = auth.get_role()  # Save the user role after login
                print(f"Login successful! Welcome, {username} ({user_role}).")
            else:
                print("Login failed. Please try again.")
        
        # Check if user is not logged in for all options except 1 (Register) and 2 (Login)
        elif not logged_in:
            print("Please login to continue.")
            continue

        # Option to Add Item (Manager Only)
        elif choice == '3' and user_role == 'manager':  # Check role once
            name = input("Item Name: ")
            price = float(input("Item Price: "))
            stock = int(input("Item Stock: "))
            item = BakeryItem(name, price, stock)
            item.add_to_db()
            print("Item added to inventory.")
        
        elif choice == '3':
            print("Access Denied: Only managers can add items.")

        # Option to Update Stock (Cashier or Manager)
        elif choice == '4':
            if logged_in:
                name = input("Item Name: ")
                quantity = int(input("Quantity Sold: "))
                item = BakeryItem.get_item(name)
                if item:
                    item_name, price, stock = item[1], item[2], item[3]
                    bakery_item = BakeryItem(name=item_name, price=price, stock=stock)
                    bakery_item.update_stock(quantity, price)
                else:
                    print("Item not found!")
            else:
                print("Please login first!")

        # Generate Sales Report
        elif choice == '5':
            if logged_in:
                period = input("Enter report period (daily/weekly/monthly): ").lower()
                if period in ['daily', 'weekly', 'monthly']:
                    reports.generate_report(period)
                else:
                    print("Invalid period. Please enter 'daily', 'weekly', or 'monthly'.")
            else:
                print("Please login first!")

        # Custom Report
        elif choice == '6':
            if logged_in:
                start_date = input("Enter start date (YYYY-MM-DD): ")
                end_date = input("Enter end date (YYYY-MM-DD): ")
                reports.generate_custom_report(start_date, end_date)
            else:
                print("Please login first!")

        # Display Inventory
        elif choice == '7':
            BakeryItem.display_inventory()

        # Remove Item from Inventory (Manager Only)
        elif choice == '8' and user_role == 'manager':
            item_id = int(input("Enter Item ID to remove: "))
            item = BakeryItem.get_item_by_id(item_id)
            if item:
                bakery = Bakery()
                bakery.remove_item(item_id)  # Use the Bakery instance to remove the item
                print(f"Item {item[1]} removed from inventory.")
            else:
                print("Item not found in inventory.")
            
        elif choice == '8':
            print("Access Denied: Only managers can remove items.")

        # Add to Cart
        elif choice == '9':
            item_id = int(input("Enter Item ID: "))
            quantity = int(input("Enter quantity: "))
            item = BakeryItem.get_item_by_id(item_id)
            if item:
                cart[item_id] = {'item': item, 'quantity': quantity}
                print(f"{quantity} of {item[1]} added to cart.")
            else:
                print("Item not found.")

        # Remove from Cart
        elif choice == '10':
            item_id = int(input("Enter Item ID to remove from cart: "))
            if item_id in cart:
                del cart[item_id]
                print(f"Item {item_id} removed from cart.")
            else:
                print("Item not found in cart.")

        # Generate Bill
        elif choice == '11':
            total = 0
            print("\n--- Bill ---")
            for item_id, details in cart.items():
                item = details['item']
                quantity = details['quantity']
                cost = item[2] * quantity
                print(f"{item[1]}: {quantity} x {item[2]} = {cost}")
                total += cost
                BakeryItem.update_stock(item_id, quantity)
            print(f"Total Amount: {total}")
            print("Thank you for your purchase!\n")
            cart.clear()

        # Option to Logout
        elif choice == '12':
            auth.logout()
            logged_in = False
            user_role = None
            print("You have successfully logged out.")

        # Option to Exit
        elif choice == '13':
            break

        else:
            print("Invalid option. Try again.")


if __name__ == "__main__":
    main()
