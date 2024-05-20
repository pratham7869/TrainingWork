from models import User, Item, Bill, Assets, ValidId
from database import get_session

# CRUD operations
# Create


def create_user(user_data):
    session = get_session()
    new_user = User(**user_data)
    session.add(new_user)
    session.commit()
    session.close()
    return new_user


def create_item(item_data):
    session = get_session()
    new_item = Item(**item_data)
    session.add(new_item)
    session.commit()
    session.close()
    return new_item


def create_bill(bill_data):
    session = get_session()
    new_bill = Bill(**bill_data)
    session.add(new_bill)
    session.commit()
    session.close()
    return new_bill


def create_assets(assets_data):
    session = get_session()
    new_assets = Assets(**assets_data)
    session.add(new_assets)
    session.commit()
    session.close()
    return new_assets

# Read


def get_user_by_id(user_id):
    session = get_session()
    user = session.query(User).get(user_id)
    session.close()
    return user


def get_user_by_name(name):
    session = get_session()
    user = session.query(User).get(name)
    session.close()
    return user


def get_item_by_id(item_id):
    session = get_session()
    item = session.query(Item).get(item_id)
    session.close()
    return item


# Update
def update_user(user_id, update_data):
    session = get_session()
    user = get_user_by_id(user_id)
    if user:
        for key, value in update_data.items():
            setattr(user, key, value)
        session.commit()
    session.close()
    return user


def update_item(item_id, update_data):
    session = get_session()
    item = get_item_by_id(item_id)
    if item:
        for key, value in update_data.items():
            setattr(item, key, value)
        session.commit()
    session.close()
    return item

# utility


def get_all_users():
    session = get_session()
    users = session.query(User).all()
    session.close()
    return users


def check_valid_email(email, password):
    session = get_session()
    valid_entry = session.query(ValidId).filter_by(company_email=email, password=password).first()
    session.close()
    return valid_entry


def get_valid_id(email):
    session = get_session()
    valid_id = session.query(ValidId).filter_by(company_email=email).first()
    session.close()
    return valid_id


def get_valid_id_by_email(email):
    session = get_session()
    valid_id = session.query(ValidId).filter_by(company_email=email).first()
    session.close()
    return valid_id


def update_valid_id_status(email, status):
    session = get_session()
    valid_id = session.query(ValidId).filter_by(company_email=email).first()
    if valid_id:
        valid_id.register_status = status
        session.commit()
    session.close()
    return valid_id


def get_user_by_email(email):
    session = get_session()
    user = session.query(User).filter(User.email == email).first()
    session.close()
    return user


