from sqlalchemy import func

from logging_config import setup_logging
from models import *
from database import get_session

# CRUD operations
# Create..........
logger = setup_logging()


def create_user(user_data):
    session = get_session()
    new_user = User(**user_data)
    session.add(new_user)
    session.commit()
    user_id = new_user.user_id
    session.close()
    logger.debug(f'User created with ID:{user_id}')
    return new_user


def create_item(item_data):
    session = get_session()
    new_item = Item(**item_data)
    session.add(new_item)
    session.commit()
    session.close()
    logger.debug(f'Item created with ID: {new_item}')
    return new_item


def create_bill(bill_data):
    session = get_session()
    new_bill = Bill(**bill_data)
    session.add(new_bill)
    session.commit()
    bill_id = new_bill.bill_id
    session.close()
    logger.debug(f'Bill created with ID: {bill_id}')
    return bill_id


def create_asset(asset_data):
    session = get_session()
    new_asset = Assets(**asset_data)
    session.add(new_asset)
    session.commit()
    session.close()
    logger.debug(f'Asset created with data: {asset_data}')


# Read........


def get_user_by_id(user_id):
    session = get_session()
    user = session.query(User).get(user_id)
    session.close()
    logger.debug(f'user fetched with data: {user.name}')
    return user


def get_user_by_name(name):
    session = get_session()
    user = session.query(User).get(name)
    session.close()
    logger.debug(f'user fetched with data: {user.name}')
    return user


def get_item_by_id(item_id):
    session = get_session()
    item = session.query(Item).get(item_id)
    session.close()
    logger.debug(f'item fetched with data: {item.item_name}')
    return item


def get_bill_by_bill_number(bill_number):
    session = get_session()
    bill = session.query(Bill).get(bill_number)
    session.close()
    logger.debug(f'bill fetched with data: {bill.bill_id}')
    return bill


def get_bill_id_by_number(bill_number):
    session = get_session()
    bill = session.query(Bill).filter_by(bill_number=bill_number).first()
    session.close()
    if bill:
        return bill.bill_id
    return None


def get_items_by_bill_id(bill_id):
    session = get_session()
    items = session.query(Item).filter_by(bill_id=bill_id).all()
    session.close()
    logger.debug(f'items fetched with bill_id: {bill_id}')
    return items


def get_all_users():
    session = get_session()
    users = session.query(User).filter_by(user_status='active',role="employee").all()
    session.close()
    logger.debug('all user data is fetched..')
    return users


def get_user_by_email(email):
    session = get_session()
    user = session.query(User).filter(User.email == email).first()
    session.close()
    logger.debug(f'user fetched with data: {user.name}')
    return user


def get_total_items():
    session = get_session()
    total_items = session.query(func.count(Item.item_id)).scalar()
    session.close()
    logger.debug('all item data is fetched..')
    return total_items


def get_total_bills():
    session = get_session()
    total_bills = session.query(func.count(Bill.bill_id)).scalar()
    session.close()
    logger.debug('all bills data is fetched..')
    return total_bills


def get_assigned_items():
    session = get_session()
    assigned_items = session.query(func.count(Assets.item_id)).filter(Assets.asset_status == 'assigned').scalar()
    session.close()
    logger.debug('all assigned_item data is fetched..')
    return assigned_items


def get_assigned_item_for_emp(user_id):
    session = get_session()
    items = session.query(Item).join(Assets).filter(Assets.emp_id == user_id, Assets.asset_status == 'assigned').all()
    session.close()
    logger.debug(f'all assigned item data with user_id:{user_id}')
    return items


def get_assigned_item(item_id):
    session = get_session()
    item = session.query(Assets).filter(Assets.item_id == item_id, Assets.asset_status == 'assigned').first()
    logger.debug('all assigned_item data is fetched..')
    session.close()

    return item


def get_total_employees():
    session = get_session()
    total_employees = session.query(func.count(User.user_id)).scalar()
    session.close()
    logger.debug('all employees data is fetched..')
    return total_employees


def get_unassigned_items():
    session = get_session()
    unassigned_items = session.query(func.count(Item.item_id)).filter(Item.item_status == 'unassigned').scalar()
    session.close()
    logger.debug('all unassigned_item data is fetched..')
    return unassigned_items


def get_asset_by_emp_item_id(emp_id, item_id):
    session = get_session()
    asset = session.query(Assets).filter(Assets.emp_id == emp_id, Assets.item_id == item_id).first()
    session.close()
    return asset


def get_all_items():
    session = get_session()
    items = session.query(Item).all()
    session.close()
    logger.debug('all item data is fetched..')
    return items


def get_all_bills():
    session = get_session()
    bills = session.query(Bill).all()
    session.close()
    logger.debug('all bill data is fetched..')
    return bills


def add_item_and_return_id(item_data):
    session = get_session()
    new_item = Item(**item_data)
    session.add(new_item)
    session.commit()
    item_id = new_item.item_id
    session.close()
    return item_id


def get_all_assigned_items():
    session = get_session()
    assigned_items = session.query(Item).filter_by(item_status='assigned').all()
    session.close()
    logger.debug('all assigned_item data is fetched..')
    return assigned_items


def get_all_total_employees():
    session = get_session()
    total_employees = session.query(User).filter_by(user_status='active').all()
    session.close()
    logger.debug('all employees_data is fetched..')
    return total_employees


def get_all_unassigned_items():
    session = get_session()
    unassigned_items = session.query(Item).filter_by(item_status='unassigned').all()
    session.close()
    logger.debug('all unassigned_items data is fetched..')
    return unassigned_items


def get_assigned_items_by_category(emp_id, category):
    session = get_session()
    assigned_items = session.query(Assets).join(Item, Assets.item_id == Item.item_id).filter(
        Assets.emp_id == emp_id,
        Item.item_type == category,
        Assets.asset_status == 'assigned'
    ).all()
    session.close()
    return assigned_items

# Update.........


def update_user(user_id, update_data):
    session = get_session()
    user = session.query(User).get(user_id)
    if user:
        for key, value in update_data.items():
            setattr(user, key, value)
        session.commit()
    logger.debug(f'user_data is updated with:{user_id}')
    session.close()
    return user


def update_item(item_id, update_data):
    session = get_session()
    item = session.query(Item).get(item_id)
    if item:
        for key, value in update_data.items():
            setattr(item, key, value)
        session.commit()
    logger.debug(f'item_data is updated with:{item_id}')
    session.close()
    return item


def update_item_status(item_id, status):
    session = get_session()
    item = session.query(Item).filter_by(item_id=item_id).first()
    if item:
        item.item_status = status
        session.commit()
    logger.debug(f'item_status is updated with:{item_id}')
    session.close()


def update_bill_number_of_items(bill_id, total_quantity):
    session = get_session()
    bill = session.query(Bill).get(bill_id)
    if bill:
        bill.no_of_items = total_quantity
        session.commit()
    session.close()


def update_asset(item_id, update_data):
    session = get_session()
    asset = session.query(Assets).filter(Assets.item_id == item_id).first()
    if asset:
        for key, value in update_data.items():
            setattr(asset, key, value)
        session.commit()
    logger.debug(f'asset_data is updated for:{item_id}')
    session.close()

# utility .......













