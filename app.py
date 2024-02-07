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
    return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.username.data == 'judejudo' and form.password.data == 'password':
            flash(f' Welcome  {form.username.data}!', 'success')
    # if request.method == 'POST':
        # session.pop('username', None)
        # Check user credentials and authenticate
        # Set session variables
        # if request.form['password'] == 'password':
            
        #     session['logged_in'] = True
        #     session['username'] = request.form['username']
            return redirect(url_for('dashboard'))
        else:
            flash('Login Unsucessfull. Please check username and password', 'danger')
    return render_template('login.html', title='login', form = form)
    
@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    # if 'logged_in' not in session:
    #     return redirect(url_for('login'))
    # username = session['username']
    # Query database for user information and payroll details
    # Pass data to dashboard template
    return render_template('dashboard.html',  title="Dashboard" )

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/dropsession')
def dropsession():
    session.pop
    return render_template('login.html')

if __name__ == "__main__":
    app.run(debug=True)