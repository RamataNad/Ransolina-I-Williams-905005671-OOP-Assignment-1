# Library Management System 🏛️

A beautiful and empowering Python-based Library Management System designed with women in mind, featuring Sierra Leonean community members and women-focused literature.

## ✨ Features

- **🎨 Beautiful Interface**: Centered text with meaningful emojis
- **🔍 Smart Search**: Search books by title or author
- **📖 Borrowing System**: Borrow and return books with intelligent constraints
- **✅ Comprehensive Validation**: Input validation and error handling with style

## 🏛️ Data Structures Used

- **📚 Books**: Dictionary (ISBN → book details)
- **👥 Members**: List of dictionaries with Sierra Leonean names  
- **📖 Genres**: Tuple of women-focused valid genres

## 🚀 Installation

1. Ensure you have Python 3.6+ installed
2. Clone or download the project files
3. No additional dependencies required

## 📁 Files Structure
library-system/
│
├── operations.py # 🌸 Core Ramata library system class and functions
├── demo.py # 🎭 Demonstration script showing system usage
├── tests.py # 🧪 Unit tests for all functionality
├── README.md # 📖 This file
├── DesignRationale.pdf # 📊 Design documentation
└── UML_Diagram.md # 🏗️ UML diagram description for hand-drawing


## 💫 Usage

### Interactive Mode
Run the system in beautiful interactive mode:

python operations.py

Demo Script
Run the comprehensive Ramata-themed demo:
python demo.py

Unit Tests
Run all unit tests with beautiful output:
python tests.py

📚 Core Functions
Book Operations
add_book() - Add new book

search_books() - Search by title/author

update_book() - Update book details

delete_book() - Delete book (if no borrowed copies)

borrow_book() - Borrow a book

return_book() - Return a borrowed book

Member Operations
dd_member() - Add new member

update_member() - Update member details

delete_member() - Delete member (if no borrowed books)

🛡️ Constraints
Maximum 3 books per member 📚📚📚

Cannot delete books with borrowed copies 🚫

Cannot delete members with borrowed books 🚫

Unique ISBN for books 🔑

Unique email for members 📧

Valid women-focused genres only (Romance, Contemporary Fiction, Self-Help, Biography, Mystery, Historical Fiction, Health & Wellness)

🌟 Example Usage
from operations import RamataMiniLibraryManagementSystem

# Initialize Ramata system
library = LibraryManagementSystem()

# Add a women-focused book
library.add_book("978-0735211292", "Big Magic", "Elizabeth Gilbert", "Self-Help", 5)

# Add a member
library.add_member("Fatmata Bangura", "fatmata@email.com")

# Borrow a book
library.borrow_book("RAM001", "978-0735211292")

# Return a book
library.return_book("RAM001", "978-0735211292")

## 🧪 Testing
The Ramata system includes comprehensive unit tests covering:

* Book and member CRUD operations 
* Borrowing and returning books 
* Edge cases and error conditions 
* Validation rules for women-focused genres

Run python tests.py to execute all beautiful tests.