from flask import Flask, request, session, redirect, url_for, render_template, sessions, redirect,g, flash, send_file
from config import Config
from flask_mysqldb import MySQL
from forms import LoginForm, RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import pandas as pd

app = Flask(__name__)
app.config.from_object(Config)

secret_key = app.config['SECRET_KEY']
mysql_host = app.config['MYSQL_HOST']
mysql_user = app.config['MYSQL_USER']
mysql_password = app.config['MYSQL_PASSWORD']
mysql_db = app.config['MYSQL_DB']

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route("/")
def home():
    q = request.args.get("q")
    page = request.args.get("page", default=1, type=int)
    per_page = 50  # Number of results per page

    cur = mysql.connection.cursor()

    if q:
        query = """
            SELECT employee_id, last_name, username, date_hired
            FROM employees 
            WHERE last_name LIKE %s 
            LIMIT %s OFFSET %s
        """
        offset = (page - 1) * per_page
        search_term = f"%{q}%" 
        cur.execute(query, (search_term, per_page, offset))

    else:
        query = """
            SELECT e.employee_id,e.last_name, e.username, e.date_hired
            FROM employees e
            LIMIT %s OFFSET %s
        """
        offset = (page - 1) * per_page
        cur.execute(query, (per_page, offset))

    results = cur.fetchall()
    cur.close()

    return render_template('home.html', results=results, query=q, page=page)

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if form.validate_on_submit():
        lastname = form.lastname.data
        username = form.username.data
        status_id = form.status_id.data
        department_id = form.department_id.data
        password = form.password.data
        status = form.status.data
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO employees (status_id, department_id, last_name, username, password, date_hired, date_modified, status)
            VALUES (%s, %s, %s, %s, %s, NOW(), NOW(), %s)
            """, (status_id, department_id, lastname, username, hashed_password, status)
        )
        mysql.connection.commit()  # Don't forget to commit changes
        flash('Registration successful. Please Sign In', 'success')
        cur.close()  # Close cursor after use
        return redirect(url_for('login'))
    else:
        return render_template('registration.html', title='Registration', form=form)




@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()  
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM employees WHERE username = %s AND password = %s", (username, password))
        user = cur.fetchone()
        cur.close()
        if user:
            flash(f'Welcome {username}!', 'success')
            session['username'] = username
            # Handle successful login
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='login', form = form)
  

@app.route('/dashboard', methods = ['GET','POST'])
def dashboard():
    if 'username' in session:
        username = session['username']
        # You can perform database queries here to fetch data for the dashboard
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT p.date_created, p.basic_salary,  p.total_deductions, p.total_allowances, p.net_income
            FROM payroll p
            JOIN employees e ON p.employee_id = e.employee_id
            WHERE e.username = %s 

        """, (username,))
        allowances = cur.fetchall()
        cur.close()
 
        cur = mysql.connection.cursor()
        cur.execute("""
            SELECT *
            FROM payroll p
            JOIN employees e ON e.employee_id = p.employee_id
            WHERE username = %s """,(username,))
        payroll_details = cur.fetchone()
        cur.close
        print(payroll_details)
        return render_template('dashboard.html', title='Dashboard', username=username, allowances=allowances, payroll_details=payroll_details)
    else:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))

@app.route('/about') 
def about():
    return render_template('about.html')

@app.route('/logout')
def logout():
    # Clear session data
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for('home'))

@app.route('/download_excel')
def download_excel():
    query = "SELECT * FROM employees LIMIT 100"
    cur = mysql.connection.cursor()
    cur.execute(query)
    all_rows = cur.fetchall()
    columns = [column[0] for column in cur.description]

    # num_chunks = (len(all_rows) + 999999) // 1000000  # Ceiling division to get the number of chunks

    # excel_writer = pd.ExcelWriter('output_file.xlsx', engine='xlsxwriter')
    # for i in range(num_chunks):
    #     start_idx = i * 1000000
    #     end_idx = min((i + 1) * 1000000, len(all_rows))
    #     chunk = all_rows[start_idx:end_idx]
    #     df = pd.DataFrame(chunk, columns=columns)
    #     sheet_name = f'Sheet_{i+1}'
    #     df.to_excel(excel_writer, sheet_name=sheet_name, index=False)

    
    # excel_writer.close()

    df = pd.DataFrame(all_rows, columns=columns)
    # Close the cursor
    cur.close()
    return send_file('output_file.xlsx', as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)