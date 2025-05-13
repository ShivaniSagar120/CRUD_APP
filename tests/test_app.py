import unittest
from app import app, get_db_connection
from flask import session

class FlaskCRUDTestCase(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

        # Add a test admin user if not present
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM admins WHERE email = 'testadmin@example.com'")
        cursor.execute("""
            INSERT INTO admins (name, email, password)
            VALUES (%s, %s, %s)
        """, ('Test Admin', 'testadmin@example.com', 
              '$pbkdf2-sha256$29000$0uPHJj8U1om8hC1Dxh9QzQ$3NQ5nDCH..HASHEDPASSWORD...'))  # Replace with hashed pw
        conn.commit()
        conn.close()

    def login(self):
        return self.app.post('/login', data=dict(
            email='testadmin@example.com',
            password='testpassword'  # Use correct password for the hashed version
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def test_login_logout(self):
        # Test login
        response = self.login()
        self.assertIn(b'Login successful', response.data)

        # Test logout
        response = self.logout()
        self.assertIn(b'Logged out successfully', response.data)

    def test_invalid_login(self):
        response = self.app.post('/login', data=dict(
            email='wrong@example.com',
            password='wrongpass'
        ), follow_redirects=True)
        self.assertIn(b'Invalid email or password', response.data)

    def test_employee_add_edit_delete(self):
        self.login()

        # Add employee
        response = self.app.post('/add', data=dict(
            name='John Doe',
            email='john@example.com',
            phone='1234567890',
            department='Engineering',
            joining_date='2024-01-01'
        ), follow_redirects=True)
        self.assertIn(b'Employee added successfully', response.data)

        # Get last inserted employee
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM employees WHERE email = 'john@example.com'")
        emp = cursor.fetchone()
        conn.close()
        emp_id = emp['id']

        # Edit employee
        response = self.app.post(f'/edit/{emp_id}', data=dict(
            name='John Smith',
            email='johnsmith@example.com',
            phone='9876543210',
            department='Marketing',
            joining_date='2025-01-01'
        ), follow_redirects=True)
        self.assertIn(b'Employee updated successfully', response.data)

        # Delete employee
        response = self.app.get(f'/delete/{emp_id}', follow_redirects=True)
        self.assertIn(b'Employee deleted successfully', response.data)

    def test_unauthorized_access_redirects(self):
        # Should redirect to login
        response = self.app.get('/')
        self.assertEqual(response.status_code, 302)
        self.assertIn('/login', response.location)

        response = self.app.get('/add')
        self.assertEqual(response.status_code, 302)

        response = self.app.get('/edit/1')
        self.assertEqual(response.status_code, 302)

        response = self.app.get('/delete/1')
        self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
    unittest.main()
