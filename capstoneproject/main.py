from db_crud import *
from models import *

user_data = {
    'name': 'aditya kasera',
    'mobile_no': '7869443087',
    'dob': '2001-12-10',
    'department': 'software engineer',
    'email': 'aditya@nucleus',
    'role': 'Admin',
    'password': 'password123',
    'security_question': 'What is your pet’s name?',
    'security_answer': 'tushar',
    'prev_password': 'oldpassword123',
    'user_status': 'Active'
}

# valid_entry = "one"
#
# if valid_entry:
#     print("ok")
# else:
#     print("notok")

# new_user = get_user_by_id(10001)
# print(new_user.name)
# new_user = create_user(user_data)
# print(new_user.email)
#
# bill_data = {
#             'bill_number': "2024-023",
#             'bill_amount': 60000,
#             'no_of_items': 2,
#             'bill_date': '2024-05-19',
#             'admin_id': 10001
#         }
# billn = get_bill_id_by_number("2324-011")
# print(billn)

item_data = {
    'item_name': 'New Item',
    'bill_id': 125,
    'item_type': 'Electronics',
    'item_status': 'unassigned',
    'warranty_period': '1 year',
    'bill_id': '1'
}

item_id = add_item_and_return_id(item_data)
print(f"New item ID: {item_id}")
