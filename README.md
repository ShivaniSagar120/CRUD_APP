#Employee Management Web App

A simple employee management system built using **Flask** and **MySQL**. This app allows an admin to register, log in, and manage employee records with full CRUD (Create, Read, Update, Delete) functionality.

#Features

- Admin Registration & Login
- Add, Edit, Delete Employee Details
- Secure Password Hashing
- View List of Employees
- Session-Based Authentication
- Flash Messaging for User Feedback

#Tech Stack

- Backend: Python, Flask
- Frontend: HTML, Jinja2 Templates
- Database: MySQL
- Libraries: Flask, mysql-connector-python, werkzeug

#Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ShivaniSagar120/CRUD_APP.git
cd CRUD_APP

### 2. Install Dependencies

pip install flask mysql-connector-python


### 3. Configure MySQL Database

Create a MySQL database named `crud_app_db`:

```sql
CREATE DATABASE crud_app_db;

CREATE TABLE admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100) UNIQUE,
    password VARCHAR(255)
);

CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    email VARCHAR(100),
    phone VARCHAR(20),
    department VARCHAR(100),
    joining_date DATE
);


Update the credentials in `app.py` under `get_db_connection()`:

```python
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="your_mysql_username",
        password="your_mysql_password",
        database="crud_app_db"
    )


### 4. Run the Application

```bash
python app.py
```

Visit `http://127.0.0.1:5000` in your browser.

#Project Structure

├── app.py                # Main Flask application
├── templates/            # HTML templates (not provided here)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation


#Routes Overview

| Route          | Description                       |
|----------------|-----------------------------------|
| `/`            | Dashboard with employee list      |
| `/login`       | Admin login                       |
| `/register`    | Admin registration                |
| `/logout`      | Log out current session           |
| `/add`         | Add a new employee                |
| `/edit/<id>`   | Edit employee details             |
| `/delete/<id>` | Delete an employee                |


#Requirements

Flask==2.3.3
mysql-connector-python==8.3.0
```

#Security Note

- Passwords are hashed using Werkzeug's secure hashing method.
- Replace the secret key and DB credentials with secure values in production.

#License

This project is open-source. Feel free to use and modify as needed.
