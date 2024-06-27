import unittest
from db_crud import *


class TestCRUDOperations(unittest.TestCase):

    # test_create........

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

    def test_create_item(self):       # testing for create item , delete item , and get item .....
        item_data = {
            'item_name': 'Test Item',
            'item_type': 'Type1',
            'bill_id': 1,
            'item_status': 'unassigned',
            'warranty_period': '1'
        }
        new_item = create_item(item_data)
        self.assertEqual(new_item.item_name, 'Test Item')

    def test_create_bill(self):
        bill_data = {
            'bill_number': 'BILL124',
            'bill_amount': 1000,
            'no_of_items': 10,
            'bill_date': '2023-01-01',
            'admin_id': 1
        }
        create_bill(bill_data)
        new_bill = get_bill_by_bill_number("BILL124")
        self.assertEqual(new_bill.bill_number, 'BILL124')

    #Test_read.......

    def test_get_total_items(self):
        items = get_total_items()
        if items > 0:
            items = True

        self.assertEqual(items, True)

    def test_get_total_bills(self):
        bills = get_total_bills()
        if bills > 0:
            bills = True

        self.assertEqual(bills, True)

    def test_get_total_employees(self):
        employees = get_total_employees()
        if employees > 0:
            employees = True

        self.assertEqual(employees, True)

    def test_get_user_by_id(self):
        update_data = {'name': 'Updated User'}
        update_user(1, update_data)
        user = get_user_by_id(1)
        self.assertEqual(user.name, 'Updated User')

    def test_get_item_by_id(self):
        item = get_item_by_id(2)
        self.assertEqual(item.item_name, 'laptop')

    def test_get_bill_by_bill_number(self):
        bill = get_bill_by_bill_number('2024-001')
        self.assertEqual(bill.bill_amount, '24000')

    def test_get_all_users(self):
        users = get_all_users()
        print(users)
        self.assertIsNotNone(users)

    def test_get_all_items(self):
        items = get_all_items()
        print(items)
        self.assertIsNotNone(items)

    def test_get_all_bills(self):
        bills = get_all_bills()
        print(bills)
        self.assertIsNotNone(bills)

    def test_get_all_assigned_items(self):
        assigned_items = get_all_assigned_items()
        print(assigned_items)
        self.assertIsNotNone(assigned_items)

    def test_get_all_unassigned_items(self):
        unassigned_items = get_all_unassigned_items()
        print(unassigned_items)
        self.assertIsNotNone(unassigned_items)

    #test_update........

    def test_update_user(self):
        update_data = {'name': 'Updated User'}
        update_user(2, update_data)
        user = get_user_by_id(2)
        self.assertEqual(user.name, 'Updated User')

    def test_update_item(self):
        update_data = {'item_name': 'Updated Item'}
        update_item(4, update_data)
        item = get_item_by_id(4)
        self.assertEqual(item.item_name, 'Updated Item')

    def test_is_email_exists_in_user(self):
        email = "pratham@nucleusteq.com"
        self.assertEqual(is_email_exists_in_user(email), True)
        self.assertEqual(is_email_exists_in_user("pratham@gmail"), False)


if __name__ == '__main__':
    unittest.main()
