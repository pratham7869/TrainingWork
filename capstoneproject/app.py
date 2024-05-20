from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from db_crud import create_user, get_valid_id_by_email, update_valid_id_status, get_user_by_email
from forms import RegistrationForm, VerificationForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    form = VerificationForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        valid_id = get_valid_id_by_email(email)

        if valid_id and valid_id.password == password:
            if valid_id.register_status == 'unregistered':
                session['user_email'] = email  # Store email in session for use in registration
                return redirect(url_for('register'))
            else:
                error = 'User is already registered.'
        else:
            error = 'Invalid email or password.'
    return render_template('verify.html', form=form, error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    user_email = session.get('user_email')
    valid_id = get_valid_id_by_email(user_email)

    if not valid_id:
        return redirect(url_for('verify'))

    if form.validate_on_submit():
        user_data = {
            'name': form.name.data,
            'mobile_no': form.mobile_no.data,
            'dob': form.dob.data,
            'department': form.department.data,
            'email': user_email,
            'role': valid_id.role,
            'password': form.new_password.data,
            'security_question': form.security_question.data,
            'security_answer': form.security_answer.data,
            'user_status': 'active'
        }
        create_user(user_data)
        update_valid_id_status(user_email, 'registered')
        return redirect(url_for('login'))

    return render_template('register.html', form=form, email=user_email, role=valid_id.role)


@app.route('/')
def index():
    return render_template('index.html')  # Render the index page template


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = get_user_by_email(email)

        if user and (user.password == password) and (user.user_status == 'active'):
            session['user_id'] = user.user_id
            session['role'] = user.role
            if user.role == 'admin':
                return redirect(url_for('admin_dashboard'))
            else:
                return redirect(url_for('employee_dashboard'))
        else:
            error = 'Invalid email or password.'

    return render_template('login.html', form=form, error=error)


@app.route('/admin_dashboard')
def admin_dashboard():
    return render_template('admin_dashboard.html')


@app.route('/employee_dashboard')
def employee_dashboard():
    return render_template('employee_dashboard.html')


if __name__ == '__main__':
    app.run(debug=True)