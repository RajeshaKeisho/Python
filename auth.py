# auth.py
import mysql.connector 
import bcrypt
from db import get_db_connection

class Authentication:
    def __init__(self):
        self.current_user = None

    def hash_password(self, password):
        """Hash a password."""
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    def check_password(self, hashed_password, user_password):
        """Compare the hashed password with the provided password."""
        # Ensure both are byte strings
        if isinstance(hashed_password, str):
            hashed_password = hashed_password.encode('utf-8')
        if isinstance(user_password, str):
            user_password = user_password.encode('utf-8')
        
        return bcrypt.checkpw(user_password, hashed_password)


    def register(self, username, password, role):
        """Register a new user with a hashed password."""
        hashed_password = self.hash_password(password)
        connection = get_db_connection()
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)",
                (username, hashed_password, role)
            )
            connection.commit()
            print("User registered successfully!")
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()
            connection.close()

    def login(self, username, password):
        """Login an existing user."""
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT id, username, password, role FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
        connection.close()

        if user and self.check_password(user[2], password):  # Compare passwords
            self.current_user = user
            return True  # Login successful
        return False  # Login failed



    def get_role(self):
        """Get the role of the currently logged-in user."""
        if self.current_user:
            return self.current_user[3]
        return None

    def logout(self):
        """Logout the current user."""
        self.current_user = None
        print("Logged out.")
