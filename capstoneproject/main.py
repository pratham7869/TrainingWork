from db_crud import create_user, get_user_by_id, get_user_by_name

user_data = {
    'name': 'pratham joya',
    'mobile_no': '7869443087',
    'dob': '2001-12-10',
    'department': 'software engineer',
    'email': 'prathamjoya7869@gmail.com',
    'role': 'Admin',
    'password': 'password123',
    'security_question': 'What is your pet’s name?',
    'security_answer': 'tushar',
    'prev_password': 'oldpassword123',
    'user_status': 'Active'
}

valid_entry = "one"

if valid_entry:
    print("ok")
else:
    print("notok")

# new_user = get_user_by_id(10001)
# print(new_user.name)