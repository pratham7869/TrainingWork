from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField, FloatField, IntegerField, \
    FieldList, FormField
from wtforms.validators import DataRequired, EqualTo, Email, Length, NumberRange


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


class ItemForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired()])
    item_type = StringField('Item Type', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    warranty_period = StringField('Warranty Period', validators=[DataRequired()])


class AddItemsForm(FlaskForm):
    items = FieldList(FormField(ItemForm), min_entries=1)
    submit = SubmitField('Add Items')


class AddBillForm(FlaskForm):
    bill_number = StringField('Bill Number', validators=[DataRequired()])
    bill_date = DateField('Bill Date', format='%Y-%m-%d', validators=[DataRequired()])
    bill_amount = IntegerField('Bill Amount', validators=[DataRequired()])
    number_of_rows = IntegerField('Number of Items', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Next')


class AssignItemsForm(FlaskForm):
    emp_id = IntegerField('Employee ID', validators=[DataRequired(), NumberRange(min=1)])
    item_id = IntegerField('Item ID', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Assign Item')


class AddEmployeeForm(FlaskForm):
    company_email = StringField('Company Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    role = SelectField('Role', choices=[('admin', 'Admin'), ('employee', 'Employee')], validators=[DataRequired()])
    submit = SubmitField('Add Employee')


class RemoveEmployeeForm(FlaskForm):
    emp_id = IntegerField('Employee ID', validators=[DataRequired()])
    find_employee = SubmitField('Find Employee')
    confirm_remove = SubmitField('Confirm Remove')


class UnassignItemForm(FlaskForm):
    item_id = StringField('Item ID', validators=[DataRequired()])
    find_item = SubmitField('Find Item')
    confirm_unassign = SubmitField('Unassign Item')
