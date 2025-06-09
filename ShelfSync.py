# Code crafted by Chirrenthen
# Check out my portfolio - https://chirrenthen.netlify.app
# For more information visit -> https://www.patreon.com/posts/shelfsync-130920442

import json
import staffs
import users


# 🔧 Utility functions
def load_json(file_path):
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        print("⚠️ Error decoding JSON.")
        return {}


def save_json(file_path, data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)


BOOKS_FILE = "books.json"
BORROWED_FILE = "borrowed_books.json"


class Users:
    def __init__(self):
        self.username = None

    def login(self):
        while True:
            self.username = input("Enter your username: ")
            if self.username in users.user:
                password = input("Enter your password: ")
                if password == users.user[self.username]["password"]:
                    print("\n✅ Login successful!")
                    print(f"Welcome, {users.user[self.username]['name']}!")
                    self.user_menu()
                    break
                else:
                    print("❌ Invalid password.\n")
            else:
                print("❌ Invalid username.\n")

    def user_menu(self):
        options = {
            "1": self.view_books,
            "2": self.borrow_book,
            "3": self.return_book,
            "4": lambda: print("👋 Logged out.\n")
        }
        while True:
            print("\n📚 User Menu:")
            print("1. View Books\n2. Borrow Book\n3. Return Book\n4. Logout")
            choice = input("Enter an option: ")
            action = options.get(choice)
            if action:
                if choice == "4":
                    break
                action()
            else:
                print("❌ Invalid choice.")

    def view_books(self):
        data = load_json(BOOKS_FILE)
        if not data:
            print("📭 No books available.")
        else:
            print("\n📖 Available Books:")
            for name, details in data.items():
                print(f"- {name} by {details['author']} ({details['year']}), Genre: {details['genre']}, Rating: {details['rating']}")

    def borrow_book(self):
        books = load_json(BOOKS_FILE)
        if not books:
            print("📭 No books available to borrow.")
            return

        book_name = input("Enter the name of the book to borrow: ")
        if book_name not in books:
            print("❌ Book not found.")
            return

        borrowed_data = load_json(BORROWED_FILE)
        user_books = borrowed_data.setdefault(self.username, [])

        if book_name in user_books:
            print("⚠️ You've already borrowed this book.")
            return

        user_books.append(book_name)
        save_json(BORROWED_FILE, borrowed_data)
        print(f"✅ You borrowed '{book_name}' successfully!")

    def return_book(self):
        borrowed_data = load_json(BORROWED_FILE)
        user_books = borrowed_data.get(self.username, [])

        if not user_books:
            print("📭 You have no borrowed books.")
            return

        print("\n📖 Your Borrowed Books:")
        for idx, book in enumerate(user_books, 1):
            print(f"{idx}. {book}")

        choice = input("Enter the name of the book to return: ")
        if choice in user_books:
            user_books.remove(choice)
            save_json(BORROWED_FILE, borrowed_data)
            print(f"✅ Book '{choice}' returned successfully!")
        else:
            print("❌ You haven't borrowed that book.")


class Staff:
    def staff_login(self):
        while True:
            username_input = input("Enter your username: ")
            if username_input in staffs.staff:
                password_input = input("Enter your password: ")
                if password_input == staffs.staff[username_input]["password"]:
                    print("\n✅ Login successful!")
                    print(f"Welcome, {staffs.staff[username_input]['name']}!")
                    self.staff_menu()
                    break
                else:
                    print("❌ Invalid password.\n")
            else:
                print("❌ Invalid username.\n")

    def staff_menu(self):
        options = {
            "1": self.add_book,
            "2": self.remove_book,
            "3": self.view_books,
            "4": self.lend_book,
            "5": self.receive_book,
            "6": lambda: print("👋 Logged out.\n")
        }
        while True:
            print("\n📚 Staff Menu:")
            print("1. Add Book\n2. Remove Book\n3. View Books\n4. Lend Book\n5. Receive Book\n6. Logout")
            choice = input("Enter an option: ")
            action = options.get(choice)
            if action:
                if choice == "6":
                    break
                action()
            else:
                print("❌ Invalid choice.")

    def add_book(self):
        book_name = input("Enter the name of the book: ")
        author = input("Enter the author: ")
        try:
            year = int(input("Enter the year: "))
            genre = input("Enter the genre: ")
            rating = float(input("Enter the rating: "))
        except ValueError:
            print("⚠️ Invalid input for year or rating.")
            return

        data = load_json(BOOKS_FILE)
        data[book_name] = {
            "author": author,
            "year": year,
            "genre": genre,
            "rating": rating
        }
        save_json(BOOKS_FILE, data)
        print(f"✅ Book '{book_name}' added successfully!")

    def remove_book(self):
        book_name = input("Enter the name of the book to remove: ")
        data = load_json(BOOKS_FILE)
        if book_name in data:
            del data[book_name]
            save_json(BOOKS_FILE, data)
            print(f"🗑️ Book '{book_name}' removed successfully!")
        else:
            print(f"❌ Book '{book_name}' not found.")

    def lend_book(self):
        book_name = input("Enter the name of the book to lend: ")
        user_name = input("Enter the username of the user: ")
        borrowed_data = load_json(BORROWED_FILE)
        user_books = borrowed_data.setdefault(user_name, [])

        if book_name in user_books:
            print("⚠️ This book is already borrowed by the user.")
        else:
            user_books.append(book_name)
            save_json(BORROWED_FILE, borrowed_data)
            print(f"✅ Book '{book_name}' lent to '{user_name}' successfully!")

    def receive_book(self):
        book_name = input("Enter the name of the book to receive: ")
        user_name = input("Enter the username: ")
        borrowed_data = load_json(BORROWED_FILE)
        user_books = borrowed_data.get(user_name, [])

        if not user_books:
            print(f"📭 '{user_name}' has no borrowed books.")
            return

        if book_name in user_books:
            user_books.remove(book_name)
            save_json(BORROWED_FILE, borrowed_data)
            print(f"✅ Book '{book_name}' received successfully from '{user_name}'!")
        else:
            print(f"❌ '{user_name}' hasn't borrowed '{book_name}'.")

    def view_books(self):
        data = load_json(BOOKS_FILE)
        if not data:
            print("📭 No books available.")
        else:
            print("\n📖 Book List:")
            for name, details in data.items():
                print(f"- {name} by {details['author']} ({details['year']}), Genre: {details['genre']}, Rating: {details['rating']}")


# ⚡ Boot up the system
def main():
    staff_obj = Staff()
    user_obj = Users()

    while True:
        print("\n🏛️ Welcome to the Library Management System!")
        print("1. Staff Login\n2. User Login\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == "1":
            staff_obj.staff_login()
        elif choice == "2":
            user_obj.login()
        elif choice == "3":
            print("👋 Exiting the system. Have a great day!")
            break
        else:
            print("❌ Invalid choice.")


if __name__ == "__main__":
    main()
