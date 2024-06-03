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


@pytest.fixture(scope='module')
def init_database():
    # Use an in-memory SQLite database for testing
    engine = get_engine('sqlite:///:memory:')
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)

    yield Session()

    Base.metadata.drop_all(engine)


def test_home_page(test_client):
    response = test_client.get('/index')
    assert response.status_code == 200
    assert b"Welcome to the Home Page" in response.data


def test_create_user_route(test_client, init_database):
    user_data = {
        'name': 'Test User',
        'mobile_no': '1234567890',
        'email': 'testuser@example.com',
        'role': 'admin',
        'password': 'password123'
    }
    response = test_client.post('/register', json=user_data)
    assert response.status_code == 201
    assert response.json['name'] == 'Test User'


def test_get_user_by_id_route(test_client, init_database):
    user_data = {
        'name': 'Test User',
        'mobile_no': '1234567890',
        'email': 'testuser@example.com',
        'role': 'admin',
        'password': 'password123'
    }
    # First, create a user
    response = test_client.post('/register', json=user_data)
    user_id = response.json['user_id']

    # Then, get the user by ID
    response = test_client.get(f'/users/{user_id}')
    assert response.status_code == 200
    assert response.json['name'] == 'Test User'


def test_create_item_route(test_client, init_database):
    item_data = {
        'item_name': 'Test Item',
        'item_type': 'Type1',
        'bill_id': 1,
        'item_status': 'unassigned',
        'warranty_period': '1 year'
    }
    response = test_client.post('/add_items', json=item_data)
    assert response.status_code == 201
    assert response.json['item_name'] == 'Test Item'


def test_get_item_by_id_route(test_client, init_database):
    item_data = {
        'item_name': 'Test Item',
        'item_type': 'Type1',
        'bill_id': 1,
        'item_status': 'unassigned',
        'warranty_period': '1 year'
    }
    # First, create an item
    response = test_client.post('/items', json=item_data)
    item_id = response.json['item_id']

    # Then, get the item by ID
    response = test_client.get(f'/items/{item_id}')
    assert response.status_code == 200
    assert response.json['item_name'] == 'Test Item'


def test_update_item_route(test_client, init_database):
    item_data = {
        'item_name': 'Test Item',
        'item_type': 'Type1',
        'bill_id': 1,
        'item_status': 'unassigned',
        'warranty_period': '1 year'
    }
    # First, create an item
    response = test_client.post('/items', json=item_data)
    item_id = response.json['item_id']

    # Then, update the item
    update_data = {'item_name': 'Updated Item'}
    response = test_client.put(f'/items/{item_id}', json=update_data)
    assert response.status_code == 200
    assert response.json['item_name'] == 'Updated Item'


def test_delete_item_route(test_client, init_database):
    item_data = {
        'item_name': 'Test Item',
        'item_type': 'Type1',
        'bill_id': 1,
        'item_status': 'unassigned',
        'warranty_period': '1 year'
    }
    # First, create an item
    response = test_client.post('/items', json=item_data)
    item_id = response.json['item_id']

    # Then, delete the item
    response = test_client.delete(f'/items/{item_id}')
    assert response.status_code == 204


def test_create_bill_route(test_client, init_database):
    bill_data = {
        'bill_number': 'BILL123',
        'bill_amount': 1000,
        'no_of_items': 10,
        'bill_date': '2023-01-01',
        'admin_id': 1
    }
    response = test_client.post('/bills', json=bill_data)
    assert response.status_code == 201
    assert response.json['bill_number'] == 'BILL123'


def test_get_bill_by_bill_number_route(test_client, init_database):
    bill_data = {
        'bill_number': 'BILL123',
        'bill_amount': 1000,
        'no_of_items': 10,
        'bill_date': '2023-01-01',
        'admin_id': 1
    }
    # First, create a bill
    response = test_client.post('/bills', json=bill_data)

    # Then, get the bill by bill number
    response = test_client.get('/bills/BILL123')
    assert response.status_code == 200
    assert response.json['bill_number'] == 'BILL123'


def test_create_asset_route(test_client, init_database):
    user_data = {
        'name': 'Test User',
        'mobile_no': '1234567890',
        'email': 'testuser@example.com',
        'role': 'employee',
        'password': 'password123'
    }
    item_data = {
        'item_name': 'Test Item',
        'item_type': 'Type1',
        'bill_id': 1,
        'item_status': 'unassigned',
        'warranty_period': '1 year'
    }
    response = test_client.post('/users', json=user_data)
    response = test_client.post('/items', json=item_data)

    asset_data = {
        'admin_id': 1,
        'emp_id': 1,
        'item_id': 1,
        'assigned_date': '2023-01-01',
        'asset_status': 'assigned'
    }
    response = test_client.post('/assets', json=asset_data)
    assert response.status_code == 201
    assert response.json['emp_id'] == 1
    assert response.json['item_id'] == 1


def test_get_all_users_route(test_client, init_database):
    response = test_client.get('/users')
    assert response.status_code == 200
    assert len(response.json) == 0

    user_data = {
        'name': 'Test User',
        'mobile_no': '1234567890',
        'email': 'testuser@example.com',
        'role': 'admin',
        'password': 'password123'
    }
    response = test_client.post('/users', json=user_data)
    response = test_client.get('/users')
    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_all_items_route(test_client, init_database):
    response = test_client.get('/items')
    assert response.status_code == 200
    assert len(response.json) == 0

    item_data = {
        'item_name': 'Test Item',
        'item_type': 'Type1',
        'bill_id': 1,
        'item_status': 'unassigned',
        'warranty_period': '1 year'
    }
    response = test_client.post('/items', json=item_data)
    response = test_client.get('/items')
    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_all_bills_route(test_client, init_database):
    response = test_client.get('/bills')
    assert response.status_code == 200
    assert len(response.json) == 0

    bill_data = {
        'bill_number': 'BILL123',
        'bill_amount': 1000,
        'no_of_items': 10,
        'bill_date': '2023-01-01',
        'admin_id': 1
    }
    response = test_client.post('/bills', json=bill_data)
    response = test_client.get('/bills')
    assert response.status_code == 200
    assert len(response.json) == 1


def test_get_all_assets_route(test_client, init_database):
    response = test_client.get('/assets')
    assert response.status_code == 200
    assert len(response.json) == 0

    user_data = {
        'name': 'Test User',
        'mobile_no': '1234567890',
        'email': 'testuser@example.com',
        'role': 'employee',
        'password': 'password123'
    }
    item_data = {
        'item_name': 'Test Item',
        'item_type': 'Type1',
        'bill_id': 1,
        'item_status': 'unassigned',
        'warranty_period': '1 year'
    }
    response = test_client.post('/users', json=user_data)
    response = test_client.post('/items', json=item_data)

    asset_data = {
        'admin_id': 1,
        'emp_id': 1,
        'item_id': 1,
        'assigned_date': '2023-01-01',
        'asset_status': 'assigned'
    }
    response = test_client.post('/assets', json=asset_data)
    response = test_client.get('/assets')
    assert response.status_code == 200
    assert len(response.json) == 1
