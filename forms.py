from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField
from wtforms.validators import DataRequired, Length, email, EqualTo, ValidationError
from flask_mysqldb import MySQL
from flask import current_app

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    department_id = IntegerField('department_id', validators=[DataRequired()])
    status_id = IntegerField('Status_id', validators=[DataRequired()])
    lastname = StringField('lastname', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired(),
                                                   Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    status = StringField('status', validators=[DataRequired()])
    # confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField('Register')

    # def validate_username(self, field):
    #         mysql = current_app.extensions['mysql']
    #         cur = mysql.connection.cursor()
    #         cur.execute("SELECT * FROM employees WHERE username = %s", (field.data,))
    #         user = cur.fetchone()
    #         cur.close()
    #         if user:
    #             raise ValidationError('Username already exists.')