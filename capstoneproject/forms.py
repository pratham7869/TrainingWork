from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, SubmitField, DateField, IntegerField, FieldList, FormField
from wtforms.validators import DataRequired, EqualTo, Email, Length, NumberRange, ValidationError
from db_crud import *


def company_email_check(form, field):
    if not field.data.endswith('@nucleusteq.com'):
        raise ValidationError('Email must be a company email')


def phone_number_check(form, field):
    if not field.data.isdigit():
        raise ValidationError('Mobile Number must contain only digits.')


def name_check(form, field):
    if not field.data.replace(" ", "").isalpha():
        raise ValidationError('Name must contain only letters and spaces.')


def unique_email_check(form, field):
    if is_email_exists_in_user(field.data):
        raise ValidationError('This email is already exists.'+field.data)


class RegistrationForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), name_check])
    mobile_no = StringField('Mobile Number', validators=[DataRequired(), Length(min=10, max=10), phone_number_check])
    email = StringField('Email', validators=[DataRequired(), Email(), company_email_check, unique_email_check])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    Role = SelectField('Role', choices=[('employee', 'Employee'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Register')


# class VerificationForm(FlaskForm):
#     email = StringField('Company Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     submit = SubmitField('Verify')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class ItemForm(FlaskForm):
    item_name = StringField('Item Name', validators=[DataRequired(), Length(min=1, max=25)])
    item_type = StringField('Item Type', validators=[DataRequired(), Length(min=1, max=25)])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1, max=25)])
    warranty_period = StringField('Warranty Period', validators=[DataRequired(), NumberRange(min=1, max=10)])


# class AddItemsForm(FlaskForm):
#     items = FieldList(FormField(ItemForm), min_entries=1)
#     submit = SubmitField('Add Items')


class AddBillForm(FlaskForm):
    bill_number = StringField('Bill Number', validators=[DataRequired(), Length(min=1, max=10)])
    bill_date = DateField('Bill Date', format='%Y-%m-%d', validators=[DataRequired()])
    bill_amount = IntegerField('Bill Amount', validators=[DataRequired(), Length(min=1, max=1000000)])
    number_of_rows = IntegerField('Number of Items', validators=[DataRequired(), NumberRange(min=1, max=15)])
    submit = SubmitField('Next')


class AssignItemsForm(FlaskForm):
    emp_id = IntegerField('Employee ID', validators=[DataRequired(), NumberRange(min=1)])
    item_id = IntegerField('Item ID', validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField('Assign Item')


# class AddEmployeeForm(FlaskForm):
#     company_email = StringField('Company Email', validators=[DataRequired(), Email()])
#     password = PasswordField('Password', validators=[DataRequired()])
#     role = SelectField('Role', choices=[('admin', 'Admin'), ('employee', 'Employee')], validators=[DataRequired()])
#     submit = SubmitField('Add Employee')


class RemoveEmployeeForm(FlaskForm):
    emp_id = IntegerField('Employee ID', validators=[DataRequired()])
    find_employee = SubmitField('Find Employee')
    confirm_remove = SubmitField('Confirm Remove')


class UnassignItemForm(FlaskForm):
    item_id = StringField('Item ID', validators=[DataRequired()])
    find_item = SubmitField('Find Item')
    confirm_unassign = SubmitField('Unassign Item')
