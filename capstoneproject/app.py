from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import date
from db_crud import *
from forms import *
from logging_config import setup_logging
import datetime

app = Flask(__name__)
app.secret_key = 'supersecretkey'
logger = setup_logging()


@app.route('/')
def index():
    logger.debug('Home page accessed')
    return render_template('index.html')  # Render the index page template


# @app.route('/verify', methods=['GET', 'POST'])
# def verify():
#     form = VerificationForm()
#     error = None
#     if form.validate_on_submit():
#         email = form.email.data
#         password = form.password.data
#         valid_id = get_valid_id_by_email(email)
#
#         if valid_id and valid_id.password == password:
#             if valid_id.register_status == 'unregistered':
#                 session['user_email'] = email  # Store email in session for use in registration
#                 return redirect(url_for('register'))
#             else:
#                 error = 'User is already registered.'
#         else:
#             error = 'Invalid email or password.'
#     return render_template('verify.html', form=form, error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    logger.debug('add employee page accessed')
    form = RegistrationForm()
    error = None

    if form.validate_on_submit():
        user_data = {
            'name': form.name.data,
            'mobile_no': form.mobile_no.data,
            'email': form.email.data,
            'role': form.Role.data,
            'password': form.new_password.data,
        }
        create_user(user_data)
        error = form.name.data + ' is registered successfully...'
        return render_template('register.html', form=form, error=error)

    return render_template('register.html', form=form, error=error)


@app.route('/login', methods=['GET', 'POST'])
def login():
    logger.debug('login page accessed')
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


@app.route('/logout')
def logout():
    logger.debug('logut page accessed')
    session.clear()
    return redirect(url_for('login'))


@app.route('/employee_dashboard')
def employee_dashboard():
    logger.debug('employee_dashboard page accessed')
    if 'user_id' not in session or session.get('role') != 'employee':
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = get_user_by_id(user_id)
    assigned_items = get_assigned_item_for_emp(user_id)

    return render_template('employee_dashboard.html', user=user, assigned_items=assigned_items)


@app.route('/admin_dashboard')
def admin_dashboard():
    logger.debug('admin_dashboard page accessed')
    total_items = get_total_items()
    total_bills = get_total_bills()
    assigned_items = get_assigned_items()
    total_employees = get_total_employees()
    unassigned_items = get_unassigned_items()
    user_id = session['user_id']
    user = get_user_by_id(user_id)

    return render_template('admin_dashboard.html',
                           total_items=total_items,
                           total_bills=total_bills,
                           assigned_items=assigned_items,
                           total_employees=total_employees,
                           unassigned_items=unassigned_items, user=user)


@app.route('/add_bill', methods=['GET', 'POST'])
def add_bill():
    logger.debug('add_items page accessed')
    if session.get('role') != 'admin':
        return redirect(url_for('login'))

    if request.method == 'POST':
        bill_number = request.form['bill_number']
        bill_date = request.form['bill_date']
        bill_amount = request.form['bill_amount']
        num_items = int(request.form['num_items'])

        total_quantity = 0

        for i in range(num_items):
            quantity = int(request.form[f'quantity_{i}'])

            for _ in range(quantity):
                total_quantity += 1

        bill_data = {
            'bill_number': bill_number,
            'bill_amount': bill_amount,
            'no_of_items': total_quantity,
            'bill_date': bill_date,
            'admin_id': session['user_id']
        }

        bill_id = create_bill(bill_data)

         # = get_bill_id_by_number(bill_number)

        for i in range(num_items):
            item_name = request.form[f'item_name_{i}']
            item_type = request.form[f'item_type_{i}']
            quantity = int(request.form[f'quantity_{i}'])
            warranty_period = request.form[f'warranty_period_{i}']

            for _ in range(quantity):
                item_data = {
                    'item_name': item_name,
                    'item_type': item_type,
                    'bill_id': bill_id,
                    'item_status': 'unassigned',
                    'warranty_period': warranty_period
                }
                create_item(item_data)
                session['bill_id'] = bill_id

        # Update the number of items in the bill
        # update_bill_item_count(bill_id, total_quantity)

        return redirect(url_for('show_added_items'))

    return render_template('add_bill.html')


@app.route('/total_items', methods=['GET'])
def total_items():
    logger.debug('total_items page accessed')
    items = get_all_items()  # Function to fetch all items from the database
    return render_template('total_items.html', items=items)


@app.route('/total_bills')
def total_bills():
    logger.debug('Total_bills page accessed')
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    bills = get_all_bills()

    # Render the total_bills.html template with the list of bills
    return render_template('total_bills.html', bills=bills)


@app.route('/assigned_items')
def all_assigned_items():
    logger.debug('assigned_items page accessed')
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    assigned_items = get_all_assigned_items()

    return render_template('assigned_items.html', assigned_items=assigned_items)


@app.route('/total_employees')
def total_employees():
    logger.debug('total_employees page accessed')
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    total_employees = get_all_total_employees()

    return render_template('total_employees.html', total_employees=total_employees)


@app.route('/unassigned_items')
def all_unassigned_items():
    logger.debug('unassigned_items page accessed')
    if 'user_id' not in session:  # Check if user is logged in
        return redirect(url_for('login'))

    unassigned_items = get_all_unassigned_items()

    return render_template('unassigned_items.html', unassigned_items=unassigned_items)


def update_bill_item_count(bill_id, count):
    session = get_session()
    bill = session.query(Bill).get(bill_id)
    if bill:
        bill.no_of_items = count
        session.commit()
    session.close()


@app.route('/show_added_items')
def show_added_items():
    logger.debug('added_items page accessed')
    bill_id = session.get('bill_id')
    if not bill_id:
        return redirect(url_for('admin_dashboard'))
    items = get_items_by_bill_id(bill_id)
    return render_template('show_added_items.html', bill_id=bill_id, items=items)


@app.route('/assign_items', methods=['GET', 'POST'])
def assign_items():
    logger.debug('assign_items page accessed')
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    form = AssignItemsForm()
    message = None
    all_user = get_all_users()
    all_item = get_all_unassigned_items()

    if form.validate_on_submit():
        emp_id = form.emp_id.data
        item_id = form.item_id.data
        admin_id = session['user_id']

        # Check if employee and item exist
        user = get_user_by_id(emp_id)
        item = get_item_by_id(item_id)

        if user and item:
            # Check if the user already has an assigned item in the same category
            assigned_items_in_category = get_assigned_items_by_category(emp_id, item.item_type)
            if assigned_items_in_category:
                message = f'The user already has an assigned item in the {item.item_type} category.'
            else:
                existing_asset = get_asset_by_emp_item_id(emp_id, item_id)
                if existing_asset:
                    # Update asset entry
                    update_asset(item_id, {
                        'admin_id': admin_id,
                        'assigned_date': date.today(),
                        'asset_status': 'assigned'
                    })

                    # Update item status
                    update_item_status(item_id, 'assigned')

                    message = f'Item {item_id} {item.item_name} has been reassigned to employee {user.name}.'
                else:
                    if item.item_status == 'unassigned':
                        # Create asset entry
                        asset_data = {
                            'admin_id': admin_id,
                            'emp_id': emp_id,
                            'item_id': item_id,
                            'assigned_date': date.today(),
                            'asset_status': 'assigned'
                        }
                        create_asset(asset_data)

                        # Update item status
                        update_item_status(item_id, 'assigned')

                        message = f'Item {item_id} {item.item_name} is assigned to employee {user.name}.'
                    else:
                        message = f'Item {item_id} {item.item_name} is already assigned.'
        else:
            message = 'Invalid employee ID or item ID.'

    return render_template('assign_items.html', form=form, message=message, all_user=all_user, all_item=all_item)


@app.route('/unassign_item', methods=['GET', 'POST'])
def unassign_item():
    logger.debug('unassign_items page accessed')
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    form = UnassignItemForm()
    item_details = None
    error = None
    all_item = get_all_assigned_items()

    if form.validate_on_submit():
        item_id = form.item_id.data
        if 'confirm_unassign' in request.form:
            # Confirm unassign action
            update_item(item_id, {'item_status': 'unassigned'})
            update_asset(item_id, {'asset_status': 'unassigned', 'unassigned_date': date.today()})
            error = f'Item {item_id} has been unassigned.'
        else:
            # Find item action
            item_details = get_assigned_item(item_id)
            if not item_details or item_details.asset_status != 'assigned':
                error = 'Item is not currently assigned.'
                item_details = None

    return render_template('unassign_item.html', form=form, item=item_details, error=error, all_item=all_item)


# @app.route('/add_employee', methods=['GET', 'POST'])
# def add_employee():
#     if 'user_id' not in session or session.get('role') != 'admin':
#         return redirect(url_for('login'))
#
#     form = AddEmployeeForm()
#     message = None
#
#     if form.validate_on_submit():
#         company_email = form.company_email.data
#         password = form.password.data
#         role = form.role.data
#         admin_id = session['user_id']
#
#         # Create valid_id entry
#         valid_id_data = {
#             'company_email': company_email,
#             'password': password,
#             'role': role,
#             'register_status': 'unregistered',
#             'admin_id': admin_id
#         }
#         create_valid_id(valid_id_data)
#
#         message = f'Employee {company_email} added successfully.'
#
#     return render_template('add_employee.html', form=form, message=message)


@app.route('/remove_employee', methods=['GET', 'POST'])
def remove_employee():
    logger.debug('remove_employee page accessed')
    if 'user_id' not in session or session.get('role') != 'admin':
        return redirect(url_for('login'))

    form = RemoveEmployeeForm()
    user_details = None
    error = None
    message = None
    all_emp = get_all_total_employees()

    if form.validate_on_submit():
        emp_id = form.emp_id.data
        if 'confirm_remove' in request.form:
            # Confirm remove action
            update_user(emp_id, {'user_status': 'inactive'})
            message = f'Employee {emp_id} has been deactivated.'
        elif 'find_employee' in request.form:
            # Find employee action
            user_details = get_user_by_id(emp_id)
            if not user_details:
                error = 'Employee not found.'

    return render_template('remove_employee.html', form=form, user=user_details, error=error, message=message,
                           all_emp=all_emp)


if __name__ == '__main__':
    app.run(debug=True)
