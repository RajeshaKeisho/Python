# reports.py
from db import get_db_connection
import mysql.connector


class Reports:
    def __init__(self):
        pass

    def add_sale(self, name, quantity, price):
        """Record a sale in the sales table."""
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO sales (item_name, quantity, price) VALUES (%s, %s, %s)",
                (name, quantity, price)
            )
            connection.commit()
            print("Sale recorded successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    def generate_report(self, period):
        """Generates a sales report based on the selected period (daily/weekly/monthly)."""
        connection = get_db_connection()
        if not connection:
            print("Error connecting to database.")
            return
        cursor = connection.cursor()

        query = self._build_report_query(period)

        if query:
            cursor.execute(query)
            results = cursor.fetchall()
            self._display_sales_report(results, period)
        else:
            print(f"Invalid period: {period}")
        
        cursor.close()
        connection.close()

    def _build_report_query(self, period):
        """Helper function to build SQL query based on the report period"""
        if period == 'daily':
            return """
            SELECT item_name, quantity, price, (quantity * price) AS total, sale_date
            FROM sales
            WHERE DATE(sale_date) = CURDATE()
            """
        elif period == 'weekly':
            return """
            SELECT item_name, quantity, price, (quantity * price) AS total, sale_date
            FROM sales
            WHERE YEARWEEK(sale_date, 1) = YEARWEEK(CURDATE(), 1)
            """
        elif period == 'monthly':
            return """
            SELECT item_name, quantity, price, (quantity * price) AS total, sale_date
            FROM sales
            WHERE MONTH(sale_date) = MONTH(CURDATE()) AND YEAR(sale_date) = YEAR(CURDATE())
            """
        return None

    def generate_custom_report(self, start_date, end_date):
        """Generate a custom report between two dates."""
        connection = get_db_connection()
        if not connection:
            print("Error connecting to database.")
            return
        cursor = connection.cursor()

        query = (
            "SELECT item_name, quantity, price, (quantity * price) AS total, sale_date "
            "FROM sales "
            "WHERE DATE(sale_date) BETWEEN %s AND %s"
        )

        cursor.execute(query, (start_date, end_date))
        results = cursor.fetchall()
        self._display_sales_report(results, f"{start_date} to {end_date}")

        cursor.close()
        connection.close()

    def _display_sales_report(self, results, period):
        """Helper function to display formatted sales report."""
        if results:
            total_sales = 0
            print(f"\n--- Sales Report ({period.capitalize()}) ---")
            for row in results:
                total = row[3] if row[3] is not None else 0  # Handle None value for total
                print(f"Item: {row[0]}, Quantity: {row[1]}, Total: ${total:.2f}, Date: {row[4]}")
                total_sales += total
            print(f"Total Sales: ${total_sales:.2f}\n")
        else:
            print(f"No sales data available for {period}.")

