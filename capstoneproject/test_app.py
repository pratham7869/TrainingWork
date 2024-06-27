import pytest
from app import app
from database import Base, get_engine
from sqlalchemy.orm import sessionmaker


@pytest.fixture(scope='module')
def test_client():
    flask_app = app

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    with flask_app.test_client() as testing_client:
        with flask_app.app_context():
            yield testing_client  # this is where the testing happens!


def test_home_page(test_client):
    response = test_client.get('/')
    assert response.status_code == 200
    # assert b"Welcome to the Home Page" in response.data


def test_login_page(test_client):
    response = test_client.post('/login')
    assert response.status_code == 200


def test_admin_dashboard_page(test_client):
    response = test_client.get('/admin_dashboard')
    assert response.status_code == 302
    response = test_client.post('/admin_dashboard')
    assert response.status_code == 405


def test_employee_dashboard_page(test_client):
    response = test_client.get('/employee_dashboard')
    assert response.status_code == 302
    response = test_client.post('/employee_dashboard')
    assert response.status_code == 405


def test_total_employees(test_client):
    response = test_client.post('/total_employees')
    assert response.status_code == 405


def test_total_employees_access(test_client):
    with test_client.session_transaction() as sess:
        sess['user_id'] = 10001
        sess['role'] = 'admin'

    response = test_client.get('/total_employees')

    # Check if the response status code is 200
    assert response.status_code == 200

    assert b'Employees List' in response.data
    assert b'Employee Id' in response.data
    assert b'Name' in response.data
    assert b'Email' in response.data
    assert b'Role' in response.data
    assert b'Mobile number' in response.data

    # Clear the session
    with test_client.session_transaction() as sess:
        sess.clear()

    # Verify session is cleared
    with test_client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'role' not in sess


def test_total_bills_access(test_client):

    with test_client.session_transaction() as sess:
        sess['user_id'] = 1  # Assuming '1' is a valid admin user_id
        sess['role'] = 'admin'

    response = test_client.get('/total_bills')
    assert response.status_code == 200

    assert b'Total Bills' in response.data
    assert b'Bill Number' in response.data
    assert b'Bill Date' in response.data
    assert b'Bill Amount' in response.data
    assert b'Number of Items' in response.data
    assert b'Admin ID' in response.data

    # Clear the session
    with test_client.session_transaction() as sess:
        sess.clear()

    # Verify session is cleared
    with test_client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'role' not in sess


def test_total_bills_unauthorized_access(test_client):
    response = test_client.get('/total_bills')
    assert response.status_code == 302


def test_total_items_access(test_client):

    with test_client.session_transaction() as sess:
        sess['user_id'] = 10001
        sess['role'] = 'admin'

    response = test_client.get('/total_items')
    assert response.status_code == 200

    assert b'All Items' in response.data
    assert b'Item ID' in response.data
    assert b'Item Name' in response.data
    assert b'Item Type' in response.data
    assert b'Item Status' in response.data
    assert b'Warranty Period' in response.data

    # Clear the session
    with test_client.session_transaction() as sess:
        sess.clear()

    # Verify session is cleared
    with test_client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'role' not in sess


def test_total_items_unauthorized_access(test_client):

    response = test_client.get('/total_items')
    assert response.status_code == 302


def test_unassigned_items_access(test_client):

    with test_client.session_transaction() as sess:
        sess['user_id'] = 10001
        sess['role'] = 'admin'

    response = test_client.get('/unassigned_items')
    assert response.status_code == 200

    assert b'Unassigned Items' in response.data
    assert b'Item ID' in response.data
    assert b'Item Name' in response.data
    assert b'Item Type' in response.data
    assert b'Item Status' in response.data
    assert b'Warranty Period' in response.data

    # Clear the session
    with test_client.session_transaction() as sess:
        sess.clear()

    # Verify session is cleared
    with test_client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'role' not in sess


def test_unassigned_items_unauthorized_access(test_client):
    with test_client.session_transaction() as sess:
        sess.clear()
    response = test_client.get('/unassigned_items')
    assert response.status_code == 302


def test_assigned_items_access(test_client):

    with test_client.session_transaction() as sess:
        sess['user_id'] = 10001
        sess['role'] = 'admin'

    response = test_client.get('/assigned_items')

    assert response.status_code == 200

    assert b'Assigned Items' in response.data
    assert b'Item ID' in response.data
    assert b'Item Name' in response.data
    assert b'Item Type' in response.data
    assert b'Item Status' in response.data
    assert b'Warranty Period' in response.data

    # Clear the session
    with test_client.session_transaction() as sess:
        sess.clear()

    # Verify session is cleared
    with test_client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'role' not in sess


def test_add_bill_access(test_client):

    with test_client.session_transaction() as sess:
        sess['user_id'] = 10001
        sess['role'] = 'admin'

    response = test_client.get('/add_bill')
    assert response.status_code == 200

    # Clear the session
    with test_client.session_transaction() as sess:
        sess.clear()

    # Verify session is cleared
    with test_client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'role' not in sess


def test_add_bill_unauthorized_access(test_client):

    response = test_client.get('/add_bill')
    assert response.status_code == 302


def test_assign_items_access(test_client):

    with test_client.session_transaction() as sess:
        sess['user_id'] = 10001
        sess['role'] = 'admin'

    response = test_client.post('/assign_items')

    assert response.status_code == 200

    assert b'Assign Items' in response.data
    assert b'User ID' in response.data
    assert b'Item ID' in response.data
    assert b'Submit' in response.data

    # Clear the session
    with test_client.session_transaction() as sess:
        sess.clear()

    # Verify session is cleared
    with test_client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'role' not in sess


def test_assign_items_unauthorized_access(test_client):

    response = test_client.get('/assign_items')
    assert response.status_code == 302


def test_add_employee_access(test_client):
    with test_client.session_transaction() as sess:
        sess['user_id'] = 10001
        sess['role'] = 'admin'

    response = test_client.post('/register')

    assert response.status_code == 200

    assert b'Assign Items' in response.data
    assert b'User ID' in response.data
    assert b'Item ID' in response.data
    assert b'Submit' in response.data

    # Clear the session
    with test_client.session_transaction() as sess:
        sess.clear()

    # Verify session is cleared
    with test_client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'role' not in sess


def test_add_employee_unauthorized_access(test_client):
    response = test_client.get('/register')
    assert response.status_code == 302


def test_remove_employee_access(test_client):
    with test_client.session_transaction() as sess:
        sess['user_id'] = 10001
        sess['role'] = 'admin'

    response = test_client.post('/remove_employee')

    assert response.status_code == 200
    # Clear the session
    with test_client.session_transaction() as sess:
        sess.clear()

    # Verify session is cleared
    with test_client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'role' not in sess


def test_remove_employee_unauthorized_access(test_client):
    response = test_client.get('/remove_employee')
    assert response.status_code == 302


def test_unassign_item_access(test_client):

    with test_client.session_transaction() as sess:
        sess['user_id'] = 10001
        sess['role'] = 'admin'

    response = test_client.post('/unassign_item')

    assert response.status_code == 200

    assert b'Unassign Item' in response.data
    assert b'Item Details' in response.data
    assert b'Assigned to Employee ID: 1' in response.data
    # Clear the session
    with test_client.session_transaction() as sess:
        sess.clear()

    # Verify session is cleared
    with test_client.session_transaction() as sess:
        assert 'user_id' not in sess
        assert 'role' not in sess


def test__unassign_item_unauthorized_access(test_client):
    response = test_client.get('/unassign_item')
    assert response.status_code == 302
