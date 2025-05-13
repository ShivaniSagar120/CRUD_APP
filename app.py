from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

app = Flask(__name__)
app.secret_key = 'supersecretkey'

# MySQL connection
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2411",  # Replace with your DB password
        database="crud_app_db"
    )

# ---------------- LOGIN ----------------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
        admin = cursor.fetchone()
        connection.close()
        
        if admin and check_password_hash(admin['password'], password):
            session['user_id'] = admin['id']
            session['user_name'] = admin['name']
            flash("Login successful!", "success")
            return redirect('/')
        else:
            flash('Invalid email or password.', 'danger')
    return render_template('landing.html')


# ---------------- LOGOUT ----------------
@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('login'))


# ---------------- REGISTER ADMIN ----------------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        connection = get_db_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM admins WHERE email = %s", (email,))
        existing = cursor.fetchone()
        if existing:
            flash('Email already exists. Please login.', 'danger')
            connection.close()
            return redirect('/login')

        hashed_pw = generate_password_hash(password)
        cursor.execute("INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)", (name, email, hashed_pw))
        connection.commit()
        connection.close()
        
        flash('Admin account created! Please login.', 'success')
        return redirect('/login')
    return render_template('register.html')


# ---------------- HOME / EMPLOYEE LIST ----------------
@app.route('/')
def index():
    if 'user_id' not in session:
        return redirect('/login')
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    connection.close()
    return render_template('index.html', employees=employees)


# ---------------- ADD EMPLOYEE DETAILS ----------------
@app.route('/add', methods=['GET', 'POST'])
def add_employee():
    if 'user_id' not in session:
        return redirect('/login')
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        joining_date = request.form['joining_date']
        
        connection = get_db_connection()
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO employees (name, email, phone, department, joining_date)
            VALUES (%s, %s, %s, %s, %s)
        """, (name, email, phone, department, joining_date))
        connection.commit()
        connection.close()
        
        flash('Employee added successfully!', 'success')
        return redirect('/')
    return render_template('add_user.html')


# ---------------- EDIT EMPLOYEE ----------------
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_employee(id):
    if 'user_id' not in session:
        return redirect('/login')
    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        department = request.form['department']
        joining_date = request.form['joining_date']
        
        cursor.execute("""
            UPDATE employees SET name=%s, email=%s, phone=%s, department=%s, joining_date=%s WHERE id=%s
        """, (name, email, phone, department, joining_date, id))
        connection.commit()
        connection.close()
        
        flash('Employee updated successfully!', 'success')
        return redirect('/')
    
    cursor.execute("SELECT * FROM employees WHERE id = %s", (id,))
    employee = cursor.fetchone()
    connection.close()
    return render_template('edit_user.html', employee=employee)


# ---------------- DELETE EMPLOYEE ----------------
@app.route('/delete/<int:id>')
def delete_employee(id):
    if 'user_id' not in session:
        return redirect('/login')
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("DELETE FROM employees WHERE id = %s", (id,))
    connection.commit()
    connection.close()
    flash('Employee deleted successfully.', 'warning')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
