from flask import Flask, request, session, redirect, url_for, render_template, sessions, redirect,g, flash
from config import Config
from flask_mysqldb import MySQL
from forms import LoginForm
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(Config)

secret_key = app.config['SECRET_KEY']
mysql_host = app.config['MYSQL_HOST']
mysql_user = app.config['MYSQL_USER']
mysql_password = app.config['MYSQL_PASSWORD']
mysql_db = app.config['MYSQL_DB']

mysql = MySQL(app)
@app.route("/")
def home():
    q = request.args.get("q")
    page = request.args.get("page", default=1, type=int)
    per_page = 50  # Number of results per page

    cur = mysql.connection.cursor()

    if q:
        query = """
            SELECT e.employee_id, e.last_name, e.username, d.department_name, e.date_hired
            FROM employees e
            JOIN departments d ON e.department_id = d.department_id
            WHERE e.last_name LIKE %s OR e.employee_id LIKE %s  
            LIMIT %s OFFSET %s
        """
        offset = (page - 1) * per_page
        cur.execute(query, ('%' + q + '%', '%' + q + '%', per_page, offset))
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

if __name__ == "__main__":
    app.run(debug=True)