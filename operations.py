import shutil

class LibraryManagementSystem:
    def __init__(self):
        self.books = {}
        self.members = []
        self.valid_genres = ("Science Fiction", "Fantasy", "Thriller", "Non-Fiction", "Young Adult",
                           "Classic Literature", "Technology", "Business", "Art & Design")
        self.next_member_id = 1

    # ---------------------------
    # Helper print methods with new emojis
    # ---------------------------

    def _print_success(self, message):
        print(f"🎯 {message}")

    def _print_error(self, message):
        print(f"🚫 {message}")

    def _print_info(self, message):
        print(f"💡 {message}")

    def _print_warning(self, message):
        print(f"⚠️  {message}")

    def _print_book(self, message):
        print(f"📖 {message}")

    def _print_member(self, message):
        print(f"👨‍💼 {message}")

    def _print_search(self, message):
        print(f"🔎 {message}")

    def _print_update(self, message):
        print(f"🔄 {message}")

    def _print_delete(self, message):
        print(f"❌ {message}")

    def _print_borrow(self, message):
        print(f"📚 {message}")

    def _print_return(self, message):
        print(f"📥 {message}")

    def add_book(self, isbn, title, author, genre, total_copies):
        print()
        self._print_book("ADDING NEW BOOK TO LIBRARY COLLECTION")
        print()

        if not isbn or not title or not author or not genre:
            self._print_error("All fields are required!")
            return False

        if isbn in self.books:
            self._print_error(f"Book with ISBN '{isbn}' already exists!")
            return False

        if genre not in self.valid_genres:
            self._print_error(f"Invalid genre! Must be one of: {self.valid_genres}")
            return False

        if total_copies <= 0:
            self._print_error("Total copies cannot be less than or equal to 0!")
            return False

        self.books[isbn] = {
            'title': title,
            'author': author,
            'genre': genre,
            'total_copies': total_copies,
            'available_copies': total_copies
        }

        self._print_success(f"Book '{title}' added successfully to Library!")
        return True

    def add_member(self, name, email):
        print()
        self._print_member("REGISTERING NEW LIBRARY MEMBER")
        print()

        if not name or not email:
            self._print_error("Name and email are required!")
            return False

        for member in self.members:
            if member['email'] == email:
                self._print_error("Member with this email already exists!")
                return False

        member_id = f"MEM{self.next_member_id:03d}"
        self.next_member_id += 1

        self.members.append({
            'member_id': member_id,
            'name': name,
            'email': email,
            'borrowed_books': []
        })

        self._print_success(f"Member '{name}' registered successfully with ID: {member_id}")
        return True

    def search_books(self, search_type, search_term):
        print()
        self._print_search("SEARCHING LIBRARY CATALOG")
        print()

        if not search_term:
            self._print_error("Search term cannot be empty!")
            return False, []

        results = []
        search_term = search_term.lower()

        if search_type == "title":
            for isbn, book in self.books.items():
                if search_term in book['title'].lower():
                    results.append((isbn, book))
        elif search_type == "author":
            for isbn, book in self.books.items():
                if search_term in book['author'].lower():
                    results.append((isbn, book))
        else:
            self._print_error("Invalid search type! Use 'title' or 'author'")
            return False, []

        if results:
            self._print_success(f"Found {len(results)} book(s) matching '{search_term}'")
        else:
            self._print_info("No books found matching your search")

        return True, results

    def update_book(self, isbn, field, new_value):
        print()
        self._print_update("UPDATING BOOK INFORMATION")
        print()

        if isbn not in self.books:
            self._print_error(f"Book with ISBN '{isbn}' not found!")
            return False

        book = self.books[isbn]

        try:
            if field == "title":
                if not new_value:
                    self._print_error("Title cannot be empty!")
                    return False
                book['title'] = new_value
                self._print_success("Book title updated successfully!")
                return True

            elif field == "author":
                if not new_value:
                    self._print_error("Author cannot be empty!")
                    return False
                book['author'] = new_value
                self._print_success("Book author updated successfully!")
                return True

            elif field == "genre":
                if new_value not in self.valid_genres:
                    self._print_error(f"Invalid genre! Must be one of: {self.valid_genres}")
                    return False
                book['genre'] = new_value
                self._print_success("Book genre updated successfully!")
                return True

            elif field == "total_copies":
                try:
                    new_copies = int(new_value)
                    if new_copies < 0:
                        self._print_error("Copies cannot be negative!")
                        return False

                    borrowed_count = book['total_copies'] - book['available_copies']
                    book['total_copies'] = new_copies
                    book['available_copies'] = max(0, new_copies - borrowed_count)
                    self._print_success("Total copies updated successfully!")
                    return True
                except ValueError:
                    self._print_error("Total copies must be a number!")
                    return False

            else:
                self._print_error("Invalid field! Use 'title', 'author', 'genre', or 'total_copies'")
                return False

        except Exception as e:
            self._print_error(f"Error updating book: {e}")
            return False

    def update_member(self, member_id, field, new_value):
        print()
        self._print_update("UPDATING MEMBER INFORMATION")
        print()

        member = self._find_member_by_id(member_id)
        if not member:
            self._print_error(f"Member with ID '{member_id}' not found!")
            return False

        if field == "name":
            if not new_value:
                self._print_error("Name cannot be empty!")
                return False
            member['name'] = new_value
            self._print_success("Member name updated successfully!")
            return True

        elif field == "email":
            if not new_value:
                self._print_error("Email cannot be empty!")
                return False

            for m in self.members:
                if m['email'] == new_value and m['member_id'] != member_id:
                    self._print_error("Email already exists!")
                    return False

            member['email'] = new_value
            self._print_success("Member email updated successfully!")
            return True

        else:
            self._print_error("Invalid field! Use 'name' or 'email'")
            return False

    def delete_book(self, isbn):
        print()
        self._print_delete("REMOVING BOOK FROM LIBRARY")
        print()

        if isbn not in self.books:
            self._print_error(f"Book with ISBN '{isbn}' not found!")
            return False

        book = self.books[isbn]

        if book['available_copies'] < book['total_copies']:
            self._print_error("Cannot delete book - some copies are currently borrowed!")
            return False

        del self.books[isbn]
        self._print_success("Book removed successfully from library!")
        return True

    def delete_member(self, member_id):
        print()
        self._print_delete("REMOVING MEMBER FROM LIBRARY")
        print()

        member = self._find_member_by_id(member_id)
        if not member:
            self._print_error(f"Member with ID '{member_id}' not found!")
            return False

        if member['borrowed_books']:
            self._print_error(f"Cannot delete member - they have {len(member['borrowed_books'])} borrowed book(s)!")
            return False

        self.members.remove(member)
        self._print_success("Member removed successfully from library!")
        return True

    def borrow_book(self, member_id, isbn):
        print()
        self._print_borrow("PROCESSING BOOK BORROWAL")
        print()

        member = self._find_member_by_id(member_id)
        if not member:
            self._print_error(f"Member with ID '{member_id}' not found!")
            return False

        if len(member['borrowed_books']) >= 3:
            self._print_error("You have reached the maximum borrowing limit of 3 books!")
            return False

        if isbn not in self.books:
            self._print_error(f"Book with ISBN '{isbn}' not found!")
            return False

        book = self.books[isbn]

        if book['available_copies'] <= 0:
            self._print_error("This book is currently not available!")
            return False

        if isbn in member['borrowed_books']:
            self._print_error("You have already borrowed this book!")
            return False

        book['available_copies'] -= 1
        member['borrowed_books'].append(isbn)

        self._print_success(f"Book '{book['title']}' borrowed successfully!")
        self._print_info(f"You now have {len(member['borrowed_books'])} book(s) borrowed")
        return True

    def return_book(self, member_id, isbn):
        print()
        self._print_return("PROCESSING BOOK RETURN")
        print()

        member = self._find_member_by_id(member_id)
        if not member:
            self._print_error(f"Member with ID '{member_id}' not found!")
            return False

        if isbn not in member['borrowed_books']:
            self._print_error("You haven't borrowed this book!")
            return False

        if isbn not in self.books:
            self._print_error("Book not found in library system!")
            return False

        member['borrowed_books'].remove(isbn)
        self.books[isbn]['available_copies'] += 1

        self._print_success(f"Book '{self.books[isbn]['title']}' returned successfully!")
        return True

    def get_book_details(self, isbn):
        return self.books.get(isbn)

    def get_member_details(self, member_id):
        return self._find_member_by_id(member_id)

    def get_all_books(self):
        return self.books

    def get_all_members(self):
        return self.members

    def _find_member_by_id(self, member_id):
        for member in self.members:
            if member['member_id'] == member_id:
                return member
        return None

    def display_menu(self):
        terminal_width = shutil.get_terminal_size().columns
        print()
        print("=" * (terminal_width // 2))
        print("🏢 LIBRARY MANAGEMENT SYSTEM 🏢".center(terminal_width))
        print("=" * (terminal_width // 2))
        print("📖 1. Add New Book")
        print("👨‍💼 2. Register New Member")
        print("🔎 3. Search Books")
        print("🔄 4. Update Book Details")
        print("👤 5. Update Member Information")
        print("❌ 6. Remove Book")
        print("👋 7. Remove Member")
        print("📚 8. Borrow Book")
        print("📥 9. Return Book")
        print("📋 10. Display All Books")
        print("👥 11. Display All Members")
        print("🚪 12. Exit System")
        print("=" * (terminal_width // 2))

    def run_interactive(self):
        print()
        print("🌟 WELCOME TO LIBRARY MANAGEMENT SYSTEM! 🌟")
        print("Your gateway to knowledge and discovery! 💫")

        while True:
            self.display_menu()
            print()
            choice = input("Enter your choice (1-12): ").strip()

            try:
                if choice == "1":
                    self._interactive_add_book()
                elif choice == "2":
                    self._interactive_add_member()
                elif choice == "3":
                    self._interactive_search_books()
                elif choice == "4":
                    self._interactive_update_book()
                elif choice == "5":
                    self._interactive_update_member()
                elif choice == "6":
                    self._interactive_delete_book()
                elif choice == "7":
                    self._interactive_delete_member()
                elif choice == "8":
                    self._interactive_borrow_book()
                elif choice == "9":
                    self._interactive_return_book()
                elif choice == "10":
                    self._display_all_books()
                elif choice == "11":
                    self._display_all_members()
                elif choice == "12":
                    print("🙏 Thank you for using Library Management System!")
                    print("📚 Keep reading and exploring! 🌟")
                    break
                else:
                    self._print_error("Please enter a valid choice (1-12)!")

            except Exception as e:
                self._print_error(f"An error occurred: {e}")

    def _interactive_add_book(self):
        print()
        self._print_book("ADDING NEW BOOK TO COLLECTION")
        print()
        isbn = input("Enter ISBN: ").strip()
        title = input("Enter title: ").strip()
        author = input("Enter author: ").strip()
        genre = input(f"Enter genre {self.valid_genres}: ").strip()
        try:
            total_copies = int(input("Enter total copies: "))
        except ValueError:
            self._print_error("Total copies must be a number!")
            return

        self.add_book(isbn, title, author, genre, total_copies)

    def _interactive_add_member(self):
        print()
        self._print_member("REGISTERING NEW MEMBER")
        print()
        name = input("Enter member name: ").strip()
        email = input("Enter email: ").strip()

        self.add_member(name, email)

    def _interactive_search_books(self):
        print()
        self._print_search("SEARCHING LIBRARY CATALOG")
        print()
        search_type = input("Search by (title/author): ").strip()
        search_term = input("Enter search term: ").strip()

        success, result = self.search_books(search_type, search_term)
        if success and result:
            print()
            self._print_book("SEARCH RESULTS")
            for isbn, book in result:
                available = book['available_copies']
                total = book['total_copies']
                status = "🎯 Available" if available > 0 else "🚫 Out of Stock"
                print(f"   ISBN: {isbn}")
                print(f"   Title: {book['title']}")
                print(f"   Author: {book['author']}")
                print(f"   Genre: {book['genre']}")
                print(f"   Status: {available}/{total} copies - {status}")
                print("   " + "-" * 40)

    def _interactive_update_book(self):
        print()
        self._print_update("UPDATING BOOK INFORMATION")
        print()
        isbn = input("Enter ISBN of book to update: ").strip()
        field = input("Enter field to update (title/author/genre/total_copies): ").strip()
        new_value = input("Enter new value: ").strip()

        self.update_book(isbn, field, new_value)

    def _interactive_update_member(self):
        print()
        self._print_update("UPDATING MEMBER INFORMATION")
        print()
        member_id = input("Enter member ID to update: ").strip()
        field = input("Enter field to update (name/email): ").strip()
        new_value = input("Enter new value: ").strip()

        self.update_member(member_id, field, new_value)

    def _interactive_delete_book(self):
        print()
        self._print_delete("REMOVING BOOK FROM LIBRARY")
        print()
        isbn = input("Enter ISBN of book to remove: ").strip()

        self.delete_book(isbn)

    def _interactive_delete_member(self):
        print()
        self._print_delete("REMOVING MEMBER FROM LIBRARY")
        print()
        member_id = input("Enter member ID to remove: ").strip()

        self.delete_member(member_id)

    def _interactive_borrow_book(self):
        print()
        self._print_borrow("BORROWING BOOK")
        print()
        member_id = input("Enter your member ID: ").strip()
        isbn = input("Enter ISBN of book to borrow: ").strip()

        self.borrow_book(member_id, isbn)

    def _interactive_return_book(self):
        print()
        self._print_return("RETURNING BOOK")
        print()
        member_id = input("Enter your member ID: ").strip()
        isbn = input("Enter ISBN of book to return: ").strip()

        self.return_book(member_id, isbn)

    def _display_all_books(self):
        print()
        self._print_book("COMPLETE LIBRARY COLLECTION")
        print()
        books = self.get_all_books()
        if not books:
            self._print_info("No books in the library collection yet.")
            return

        for isbn, book in books.items():
            available = book['available_copies']
            total = book['total_copies']
            status = "🎯 Available" if available > 0 else "🚫 Out of Stock"
            print(f"📖 {book['title']} by {book['author']}")
            print(f"   ISBN: {isbn}")
            print(f"   Genre: {book['genre']}")
            print(f"   Status: {available}/{total} copies - {status}")
            print("   " + "=" * 30)

    def _display_all_members(self):
        print()
        self._print_member("REGISTERED LIBRARY MEMBERS")
        print()
        members = self.get_all_members()
        if not members:
            self._print_info("No members registered in the library yet.")
            return

        for member in members:
            borrowed_count = len(member['borrowed_books'])
            print(f"👨‍💼 {member['name']}")
            print(f"   ID: {member['member_id']}")
            print(f"   Email: {member['email']}")
            print(f"   Borrowed Books: {borrowed_count}")
            print("   " + "•" * 30)

if __name__ == "__main__":
    library = LibraryManagementSystem()
    library.run_interactive()