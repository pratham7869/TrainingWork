from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField
from wtforms.validators import DataRequired, EqualTo, Email, Length


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    mobile_no = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=10)])
    dob = DateField('Date of Birth', format='%Y-%m-%d', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    security_question = SelectField('Security Question', choices=[
        ('What is your mother\'s maiden name?', 'What is your mother\'s maiden name?'),
        ('What was the name of your first pet?', 'What was the name of your first pet?'),
        ('What was your first car?', 'What was your first car?'),
        ('What elementary school did you attend?', 'What elementary school did you attend?')
    ], validators=[DataRequired()])
    security_answer = StringField('Security Answer', validators=[DataRequired()])
    submit = SubmitField('Register')


class VerificationForm(FlaskForm):
    email = StringField('Company Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Verify')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
