import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database import Base, get_engine, get_session
from models import User, Item, Bill, Assets
from db_crud import *


class TestCRUDOperations(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Use an in-memory SQLite database for testing
        cls.engine = get_engine('sqlite:///:memory:')
        Base.metadata.create_all(cls.engine)
        cls.Session = sessionmaker(bind=cls.engine)

    def setUp(self):
        # Start a new session for each test
        self.session = self.Session()

    def tearDown(self):
        # Rollback any changes made during the test
        self.session.rollback()
        self.session.close()

    def test_create_user(self):
        user_data = {
            'name': 'Test User',
            'mobile_no': '1234567890',
            'email': 'testuser@nucleusteq.com',
            'role': 'admin',
            'password': 'password123'
        }
        new_user = create_user(user_data)
        self.assertEqual(new_user.name, 'Test User')
        self.assertEqual(new_user.email, 'testuser@nucleusteq.com')

    def test_get_user_by_id(self):
        user = get_user_by_id(1)
        self.assertIsNone(user)
        user_data = {
            'name': 'Test User',
            'mobile_no': '1234567890',
            'email': 'testuser@example.com',
            'role': 'admin',
            'password': 'password123'
        }
        create_user(user_data)
        user = get_user_by_id(1)
        self.assertIsNotNone(user)
        self.assertEqual(user.name, 'Test User')

    def test_update_user(self):
        user_data = {
            'name': 'Test User',
            'mobile_no': '1234567890',
            'email': 'testuser@example.com',
            'role': 'admin',
            'password': 'password123'
        }
        new_user = create_user(user_data)
        update_data = {'name': 'Updated User'}
        updated_user = update_user(new_user.user_id, update_data)
        self.assertEqual(updated_user.name, 'Updated User')

    def test_create_item(self):
        item_data = {
            'item_name': 'Test Item',
            'item_type': 'Type1',
            'bill_id': 1,
            'item_status': 'unassigned',
            'warranty_period': '1 year'
        }
        new_item = create_item(item_data)
        self.assertEqual(new_item.item_name, 'Test Item')

    def test_get_item_by_id(self):
        item = get_item_by_id(1)
        self.assertIsNone(item)
        item_data = {
            'item_name': 'Test Item',
            'item_type': 'Type1',
            'bill_id': 1,
            'item_status': 'unassigned',
            'warranty_period': '1 year'
        }
        create_item(item_data)
        item = get_item_by_id(1)
        self.assertIsNotNone(item)
        self.assertEqual(item.item_name, 'Test Item')

    def test_update_item(self):
        item_data = {
            'item_name': 'Test Item',
            'item_type': 'Type1',
            'bill_id': 1,
            'item_status': 'unassigned',
            'warranty_period': '1 year'
        }
        new_item = create_item(item_data)
        update_data = {'item_name': 'Updated Item'}
        updated_item = update_item(new_item.item_id, update_data)
        self.assertEqual(updated_item.item_name, 'Updated Item')

    def test_create_bill(self):
        bill_data = {
            'bill_number': 'BILL123',
            'bill_amount': 1000,
            'no_of_items': 10,
            'bill_date': '2023-01-01',
            'admin_id': 1
        }
        new_bill = create_bill(bill_data)
        self.assertEqual(new_bill.bill_number, 'BILL123')

    def test_get_bill_by_bill_number(self):
        bill = get_bill_by_bill_number('BILL123')
        self.assertIsNone(bill)
        bill_data = {
            'bill_number': 'BILL123',
            'bill_amount': 1000,
            'no_of_items': 10,
            'bill_date': '2023-01-01',
            'admin_id': 1
        }
        create_bill(bill_data)
        bill = get_bill_by_bill_number('BILL123')
        self.assertIsNotNone(bill)
        self.assertEqual(bill.bill_number, 'BILL123')

    def test_create_asset(self):
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
        create_user(user_data)
        create_item(item_data)
        asset_data = {
            'admin_id': 1,
            'emp_id': 1,
            'item_id': 1,
            'assigned_date': '2023-01-01',
            'asset_status': 'assigned'
        }
        create_asset(asset_data)
        asset = get_asset_by_emp_item_id(1, 1)
        self.assertIsNotNone(asset)
        self.assertEqual(asset.emp_id, 1)
        self.assertEqual(asset.item_id, 1)

    def test_get_all_users(self):
        users = get_all_users()
        self.assertEqual(len(users), 0)
        user_data = {
            'name': 'Test User',
            'mobile_no': '1234567890',
            'email': 'testuser@example.com',
            'role': 'admin',
            'password': 'password123'
        }
        create_user(user_data)
        users = get_all_users()
        self.assertEqual(len(users), 1)

    def test_get_all_items(self):
        items = get_all_items()
        self.assertEqual(len(items), 0)
        item_data = {
            'item_name': 'Test Item',
            'item_type': 'Type1',
            'bill_id': 1,
            'item_status': 'unassigned',
            'warranty_period': '1 year'
        }
        create_item(item_data)
        items = get_all_items()
        self.assertEqual(len(items), 1)

    def test_get_all_bills(self):
        bills = get_all_bills()
        self.assertEqual(len(bills), 0)
        bill_data = {
            'bill_number': 'BILL123',
            'bill_amount': 1000,
            'no_of_items': 10,
            'bill_date': '2023-01-01',
            'admin_id': 1
        }
        create_bill(bill_data)
        bills = get_all_bills()
        self.assertEqual(len(bills), 1)

    def test_get_all_assigned_items(self):
        assigned_items = get_all_assigned_items()
        self.assertEqual(len(assigned_items), 0)
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
        create_user(user_data)
        create_item(item_data)
        asset_data = {
            'admin_id': 1,
            'emp_id': 1,
            'item_id': 1,
            'assigned_date': '2023-01-01',
            'asset_status': 'assigned'
        }
        create_asset(asset_data)
        assigned_items = get_all_assigned_items()
        self.assertEqual(len(assigned_items), 1)

    def test_get_all_unassigned_items(self):
        unassigned_items = get_all_unassigned_items()
        self.assertEqual(len(unassigned_items), 0)
        item_data = {
            'item_name': 'Test Item',
            'item_type': 'Type1',
            'bill_id': 1,
            'item_status': 'unassigned',
            'warranty_period': '1 year'
        }
        create_item(item_data)
        unassigned_items = get_all_unassigned_items()
        self.assertEqual(len(unassigned_items), 1)


if __name__ == '__main__':
    unittest.main()
