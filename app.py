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

    if q:
        cur = mysql.connection.cursor()
        # Construct the query to search for employees based on last name or department name
        query = """
            SELECT e.last_name, e.username, d.department_name, e.date_hired
            FROM employees e
            JOIN departments d ON e.department_id = d.department_id
            WHERE e.last_name LIKE %s OR d.department_name LIKE %s
        """
        # Execute the query with the search parameter
        cur.execute(query, ('%' + q + '%', '%' + q + '%'))
        results = cur.fetchall()
        cur.close()
        return render_template('home.html', results=results, query=q)
    else:
        return render_template('home.html', results=[], query=q)


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
            SELECT a.allowance_name, pa.amount, p.basic_salary 
            FROM payroll_allowances pa
            JOIN allowances a ON a.allowance_id = pa.allowance_id
            JOIN payroll p ON pa.payroll_id = p.payroll_id
            JOIN employees e ON p.employee_id = e.employee_id
            WHERE e.username = %s 
            """,(username,)
        )
        allowances = cur.fetchall()
        cur.close()
        return render_template('dashboard.html', title='Dashboard', username=username, allowances=allowances)
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