Library Management System

A Django-based Library Management System with custom authentication and role-based access control. This project was built as a capstone project and deployed on PythonAnywhere.

🚀 Features

Custom User Model with Roles

Admin – Full control over system.

Librarian – Manage books and transactions.

Member (default) – Borrow and view books.

Authentication & Profiles

User registration, login, and logout using Django’s authentication system.

Automatic profile creation via Django signals.

Users can update their profiles.

Role-Based Permissions

Access levels based on role:

Admin → System-wide management.

Librarian → Books & transactions.

Member → Borrow books, view history.

Books Management

Add, update, and delete books (Admin/Librarian).

Members can view available books.

Transactions & Borrowing History

Track book borrow and return.

Members can view their own borrowing history.

Librarians/Admins can manage all transactions.

Error Handling & Bug Fixes

Improved validation and error messages.

Fixed permission-related issues.

Deployment

Successfully deployed on PythonAnywhere.

API Support (Work in Progress)

Token-based API authentication for future integration.

🛠️ Tech Stack

Backend: Django (Python)

Database: SQLite (development)

Authentication: Django’s built-in system + custom roles

Deployment: PythonAnywhere
