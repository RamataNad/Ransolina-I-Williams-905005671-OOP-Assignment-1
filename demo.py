from operations import LibraryManagementSystem

def run_demo():
    terminal_width = 70
    print("=" * terminal_width)
    print("🏢 LIBRARY MANAGEMENT SYSTEM - DEMO 🏢")
    print("=" * terminal_width)

    library = LibraryManagementSystem()

    # Demo 1: Add Books
    print("\n1. ADDING BOOKS TO COLLECTION")
    print("-" * terminal_width)

    books_to_add = [
        ("978-0553382563", "Dune", "Frank Herbert", "Science Fiction", 5),
        ("978-0451524935", "1984", "George Orwell", "Classic Literature", 4),
        ("978-0439064873", "The Hobbit", "J.R.R. Tolkien", "Fantasy", 3),
        ("978-0307474278", "The Da Vinci Code", "Dan Brown", "Thriller", 6),
        ("978-0061120084", "The Alchemist", "Paulo Coelho", "Young Adult", 4),  # Changed from "Fiction" to "Young Adult"
        ("978-0140280197", "The Lean Startup", "Eric Ries", "Business", 5),
        ("978-0134685991", "Effective Java", "Joshua Bloch", "Technology", 3),
        ("978-1591847786", "Hook Point", "Brendan Kane", "Business", 4),
        ("978-0307887894", "Ready Player One", "Ernest Cline", "Science Fiction", 3),
        ("978-0544003415", "The Lord of the Rings", "J.R.R. Tolkien", "Fantasy", 4)
    ]

    for isbn, title, author, genre, copies in books_to_add:
        print(f"\n📖 Adding '{title}'...")
        success = library.add_book(isbn, title, author, genre, copies)
        if not success:
            print(f"   🚫 Failed to add '{title}' - invalid genre: {genre}")

    # Demo 2: Add Members
    print("\n2. REGISTERING MEMBERS")
    print("-" * terminal_width)

    members_to_add = [
        ("John Smith", "john.smith@email.com"),
        ("Sarah Johnson", "sarah.johnson@email.com"),
        ("Michael Chen", "michael.chen@email.com"),
        ("Emily Davis", "emily.davis@email.com"),
        ("David Wilson", "david.wilson@email.com"),
        ("Lisa Brown", "lisa.brown@email.com"),
        ("Robert Taylor", "robert.taylor@email.com"),
        ("Maria Garcia", "maria.garcia@email.com"),
        ("James Miller", "james.miller@email.com"),
        ("Jennifer Lee", "jennifer.lee@email.com")
    ]

    for name, email in members_to_add:
        print(f"\n👨‍💼 Adding {name}...")
        library.add_member(name, email)

    # Demo 3: Display All Books and Members
    print("\n3. CURRENT LIBRARY STATUS")
    print("-" * terminal_width)

    print("\n📚 All Books in Library:")
    books = library.get_all_books()
    for isbn, book in books.items():
        print(f"   {book['title']} - Available: {book['available_copies']}/{book['total_copies']}")

    print("\n👥 All Library Members:")
    members = library.get_all_members()
    for member in members:
        print(f"   {member['name']} (ID: {member['member_id']}) - Borrowed: {len(member['borrowed_books'])}")

    # Demo 4: Search Books
    print("\n4. SEARCHING LIBRARY CATALOG")
    print("-" * terminal_width)

    # Search by title
    print("\n🔎 Searching for 'Lord' in titles...")
    success, results = library.search_books("title", "Lord")
    if success and results:
        for isbn, book in results:
            print(f"   Found: {book['title']} by {book['author']}")

    # Search by author
    print("\n🔎 Searching for 'Tolkien' in authors...")
    success, results = library.search_books("author", "Tolkien")
    if success and results:
        for isbn, book in results:
            print(f"   Found: {book['title']} by {book['author']}")

    # Demo 5: Borrow Books
    print("\n5. BORROWING BOOKS")
    print("-" * terminal_width)

    # Get member IDs
    members = library.get_all_members()
    john_id = members[0]['member_id']
    sarah_id = members[1]['member_id']

    # John borrows books
    print(f"\n📚 John (ID: {john_id}) borrowing books:")
    borrow_operations = [
        (john_id, "978-0553382563"),  # Dune
        (john_id, "978-0451524935"),  # 1984
        (john_id, "978-0439064873"),  # The Hobbit
    ]

    for member_id, isbn in borrow_operations:
        book_details = library.get_book_details(isbn)
        if book_details:
            book_title = book_details['title']
            print(f"   Borrowing '{book_title}'...")
            library.borrow_book(member_id, isbn)
        else:
            print(f"   🚫 Book with ISBN {isbn} not found!")

    # Try to borrow fourth book (should fail)
    print(f"\n⚠️ Trying to borrow fourth book...")
    library.borrow_book(john_id, "978-0307474278")

    # Sarah borrows a book - check if book exists first
    print(f"\n📚 Sarah (ID: {sarah_id}) borrowing a book:")
    book_details = library.get_book_details("978-0061120084")
    if book_details:
        book_title = book_details['title']
        print(f"   Borrowing '{book_title}'...")
        library.borrow_book(sarah_id, "978-0061120084")
    else:
        print(f"   🚫 Book with ISBN 978-0061120084 not found!")

    # Demo 6: Try to borrow unavailable book
    print("\n6. TESTING UNAVAILABLE BOOK SCENARIO")
    print("-" * terminal_width)

    # Try to borrow a book with no available copies
    print("\n🚫 Trying to borrow 'Dune' when no copies available...")
    library.borrow_book(sarah_id, "978-0553382563")

    # Demo 7: Return Books
    print("\n7. RETURNING BOOKS")
    print("-" * terminal_width)

    # John returns a book
    print(f"\n📥 John returning a book:")
    library.return_book(john_id, "978-0553382563")

    # Now Sarah can borrow it
    print(f"\n📚 Sarah borrowing the returned book:")
    library.borrow_book(sarah_id, "978-0553382563")

    # Demo 8: Update Operations
    print("\n8. UPDATING LIBRARY RECORDS")
    print("-" * terminal_width)

    # Update book
    print("\n🔄 Updating 'The Da Vinci Code' copies to 8...")
    library.update_book("978-0307474278", "total_copies", "8")

    # Update member
    michael_id = members[2]['member_id']
    print(f"\n👤 Updating Michael's email...")
    library.update_member(michael_id, "email", "michael.new@email.com")

    # Demo 9: Final Status
    print("\n9. FINAL LIBRARY STATUS")
    print("-" * terminal_width)

    print("\n📚 All Books (Final):")
    books = library.get_all_books()
    for isbn, book in books.items():
        print(f"   {book['title']} - Available: {book['available_copies']}/{book['total_copies']}")

    print("\n👥 All Members (Final):")
    members = library.get_all_members()
    for member in members:
        borrowed_books = member['borrowed_books']
        book_titles = []
        for isbn in borrowed_books:
            book = library.get_book_details(isbn)
            if book:
                book_titles.append(book['title'])
        print(f"   {member['name']}: {len(borrowed_books)} books - {book_titles}")

    # Demo 10: Delete Operations (with constraints)
    print("\n10. DELETE OPERATIONS WITH CONSTRAINTS")
    print("-" * terminal_width)

    # Try to delete member with borrowed books (should fail)
    print(f"\n👋 Trying to delete John (has borrowed books)...")
    library.delete_member(john_id)

    # Try to delete book with borrowed copies (should fail)
    print(f"\n❌ Trying to delete '1984' (borrowed copies)...")
    library.delete_book("978-0451524935")

    print("\n" + "=" * terminal_width)
    print("🎉 LIBRARY MANAGEMENT SYSTEM DEMO COMPLETED SUCCESSFULLY!")
    print("=" * terminal_width)

if __name__ == "__main__":
    run_demo()