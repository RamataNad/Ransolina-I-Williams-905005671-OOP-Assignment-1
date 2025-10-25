from operations import LibraryManagementSystem


class TestLibraryManagementSystem:

    def setup_method(self):
        """Set up a fresh library system for each test"""
        self.library = LibraryManagementSystem()

        # Add some test data
        self.library.add_book("LIB-001", "Test Book 1", "Author One", "Science Fiction", 3)
        self.library.add_book("LIB-002", "Test Book 2", "Author Two", "Fantasy", 1)
        self.library.add_member("Test Member", "test@email.com")

        # Get the auto-generated member ID
        self.member_id = self.library.get_all_members()[0]['member_id']

    def test_add_book_success(self):
        """Test adding a book successfully to Library"""
        success = self.library.add_book("LIB-003", "New Book", "New Author", "Thriller", 5)
        assert success == True
        assert "LIB-003" in self.library.get_all_books()

    def test_add_book_duplicate_isbn(self):
        """Test adding a book with duplicate ISBN to Library"""
        success = self.library.add_book("LIB-001", "Duplicate Book", "Some Author", "Science Fiction", 2)
        assert success == False

    def test_add_book_invalid_genre(self):
        """Test adding a book with invalid genre to Library"""
        success = self.library.add_book("LIB-004", "Invalid Genre Book", "Author", "InvalidGenre", 2)
        assert success == False

    def test_add_book_negative_copies(self):
        """Test adding a book with negative copies to Library"""
        success = self.library.add_book("LIB-005", "Negative Copies", "Author", "Science Fiction", -1)
        assert success == False

    def test_add_member_success(self):
        """Test adding a member successfully to Library"""
        success = self.library.add_member("John Doe", "john@email.com")
        assert success == True
        assert len(self.library.get_all_members()) == 2

    def test_add_member_duplicate_email(self):
        """Test adding a member with duplicate email to Library"""
        success = self.library.add_member("Different Name", "test@email.com")
        assert success == False

    def test_search_books_by_title(self):
        """Test searching books by title in Library"""
        success, results = self.library.search_books("title", "Test Book")
        assert success == True
        assert len(results) == 2

    def test_search_books_by_author(self):
        """Test searching books by author in Library"""
        success, results = self.library.search_books("author", "Author One")
        assert success == True
        assert len(results) == 1
        assert results[0][1]['title'] == "Test Book 1"

    def test_borrow_book_success(self):
        """Test borrowing a book successfully from Library"""
        success = self.library.borrow_book(self.member_id, "LIB-001")
        assert success == True

        # Check that available copies decreased
        book = self.library.get_book_details("LIB-001")
        assert book['available_copies'] == 2

        # Check that member has the book
        member = self.library.get_member_details(self.member_id)
        assert "LIB-001" in member['borrowed_books']

    def test_borrow_book_no_copies_left(self):
        """Test borrowing when no copies are available in Library"""
        # First, borrow the only copy
        self.library.borrow_book(self.member_id, "LIB-002")

        # Add another member to try borrowing the same book
        self.library.add_member("Second Member", "second@email.com")
        second_member_id = self.library.get_all_members()[1]['member_id']

        success = self.library.borrow_book(second_member_id, "LIB-002")
        assert success == False

    def test_borrow_book_max_limit(self):
        """Test borrowing beyond maximum limit (3 books) in Library"""
        # Add more books
        self.library.add_book("LIB-003", "Book 3", "Author", "Science Fiction", 1)
        self.library.add_book("LIB-004", "Book 4", "Author", "Fantasy", 1)
        self.library.add_book("LIB-005", "Book 5", "Author", "Thriller", 1)

        # Borrow 3 books successfully
        self.library.borrow_book(self.member_id, "LIB-001")
        self.library.borrow_book(self.member_id, "LIB-003")
        self.library.borrow_book(self.member_id, "LIB-004")

        # Try to borrow fourth book
        success = self.library.borrow_book(self.member_id, "LIB-005")
        assert success == False

    def test_return_book_success(self):
        """Test returning a book successfully to Library"""
        # First borrow a book
        self.library.borrow_book(self.member_id, "LIB-001")

        # Then return it
        success = self.library.return_book(self.member_id, "LIB-001")
        assert success == True

        # Check that available copies increased
        book = self.library.get_book_details("LIB-001")
        assert book['available_copies'] == 3

        # Check that member no longer has the book
        member = self.library.get_member_details(self.member_id)
        assert "LIB-001" not in member['borrowed_books']

    def test_return_book_not_borrowed(self):
        """Test returning a book that wasn't borrowed from Library"""
        success = self.library.return_book(self.member_id, "LIB-001")
        assert success == False

    def test_update_book_success(self):
        """Test updating book details successfully in Library"""
        success = self.library.update_book("LIB-001", "title", "Updated Title")
        assert success == True

        book = self.library.get_book_details("LIB-001")
        assert book['title'] == "Updated Title"

    def test_update_book_copies(self):
        """Test updating book copies in Library"""
        # First borrow a copy to test available copies adjustment
        self.library.borrow_book(self.member_id, "LIB-001")

        success = self.library.update_book("LIB-001", "total_copies", "5")
        assert success == True

        book = self.library.get_book_details("LIB-001")
        assert book['total_copies'] == 5
        assert book['available_copies'] == 4  # 5 total - 1 borrowed

    def test_delete_book_success(self):
        """Test deleting a book successfully from Library"""
        success = self.library.delete_book("LIB-002")
        assert success == True
        assert "LIB-002" not in self.library.get_all_books()

    def test_delete_book_with_borrowed_copies(self):
        """Test deleting a book with borrowed copies from Library"""
        # First borrow the book
        self.library.borrow_book(self.member_id, "LIB-001")

        # Try to delete it
        success = self.library.delete_book("LIB-001")
        assert success == False

    def test_delete_member_success(self):
        """Test deleting a member successfully from Library"""
        success = self.library.delete_member(self.member_id)
        assert success == True
        assert len(self.library.get_all_members()) == 0

    def test_delete_member_with_borrowed_books(self):
        """Test deleting a member with borrowed books from Library"""
        # First borrow a book
        self.library.borrow_book(self.member_id, "LIB-001")

        # Try to delete the member
        success = self.library.delete_member(self.member_id)
        assert success == False


def run_tests():
    """Run all tests and display results for Library Management System"""
    terminal_width = 60
    print("=" * terminal_width)
    print("🧪 RUNNING LIBRARY MANAGEMENT SYSTEM TESTS 🧪".center(terminal_width))
    print("=" * terminal_width)

    test_class = TestLibraryManagementSystem()

    # List of test methods to run
    test_methods = [
        test_class.test_add_book_success,
        test_class.test_add_book_duplicate_isbn,
        test_class.test_add_book_invalid_genre,
        test_class.test_add_book_negative_copies,
        test_class.test_add_member_success,
        test_class.test_add_member_duplicate_email,
        test_class.test_search_books_by_title,
        test_class.test_search_books_by_author,
        test_class.test_borrow_book_success,
        test_class.test_borrow_book_no_copies_left,
        test_class.test_borrow_book_max_limit,
        test_class.test_return_book_success,
        test_class.test_return_book_not_borrowed,
        test_class.test_update_book_success,
        test_class.test_update_book_copies,
        test_class.test_delete_book_success,
        test_class.test_delete_book_with_borrowed_copies,
        test_class.test_delete_member_success,
        test_class.test_delete_member_with_borrowed_books,
    ]

    passed = 0
    failed = 0

    for test_method in test_methods:
        try:
            # Reset for each test
            test_class.setup_method()
            test_method()
            print(f"🎯 {test_method.__name__}: PASSED")
            passed += 1
        except AssertionError as e:
            print(f"🚫 {test_method.__name__}: FAILED - {e}")
            failed += 1
        except Exception as e:
            print(f"💥 {test_method.__name__}: ERROR - {e}")
            failed += 1

    print("=" * terminal_width)
    print(f"📊 RESULTS: {passed} passed, {failed} failed, {len(test_methods)} total".center(terminal_width))

    if failed == 0:
        print("🎉 ALL LIBRARY MANAGEMENT SYSTEM TESTS PASSED!".center(terminal_width))
    else:
        print(f"⚠️  {failed} LIBRARY MANAGEMENT SYSTEM TESTS FAILED!".center(terminal_width))

    print("=" * terminal_width)


if __name__ == "__main__":
    run_tests()