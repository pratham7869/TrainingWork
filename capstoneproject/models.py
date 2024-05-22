from sqlalchemy import Column, Integer, String, ForeignKey, Date, Float
from database import Base
from sqlalchemy.sql import func


class User(Base):
    __tablename__ = 'user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    mobile_no = Column(String(20))
    dob = Column(Date)
    department = Column(String(100))
    email = Column(String(255))
    role = Column(String(50))
    password = Column(String(255))
    security_question = Column(String(255))
    security_answer = Column(String(255))
    prev_password = Column(String(255))
    user_status = Column(String(50), default='active')


class Assets(Base):
    __tablename__ = 'assets'

    admin_id = Column(Integer, ForeignKey('user.user_id'))
    emp_id = Column(Integer, ForeignKey('user.user_id'), primary_key=True)
    item_id = Column(Integer, ForeignKey('item.item_id'), primary_key=True)
    assigned_date = Column(Date, default=func.now())
    unassigned_date = Column(Date)
    asset_status = Column(String(50), default='assigned')


class Item(Base):
    __tablename__ = 'item'

    item_name = Column(String(255))
    item_id = Column(Integer, primary_key=True, autoincrement=True)
    bill_id = Column(Integer, ForeignKey('bill.bill_id'))
    item_type = Column(String(100))
    item_status = Column(String(50), default='unassigned')
    warranty_period = Column(String(50))


class Bill(Base):
    __tablename__ = 'bill'

    bill_number = Column(String(255))
    bill_amount = Column(Integer)
    bill_id = Column(Integer, primary_key=True, autoincrement=True)
    no_of_items = Column(Integer)
    bill_date = Column(Date)
    admin_id = Column(Integer, ForeignKey('user.user_id'))


class ValidId(Base):
    __tablename__ = 'validid'

    company_email = Column(String(255), primary_key=True)
    role = Column(String(50))
    register_status = Column(String(50), default='unregistered')
    password = Column(String(255))
    admin_id = Column(Integer, ForeignKey('user.user_id'))


# in this file the table structure is written in the form of classes.
# ALTER TABLE assets MODIFY assigned_date DATETIME DEFAULT CURRENT_TIMESTAMP;
# ALTER TABLE assets MODIFY asset_status VARCHAR(50) DEFAULT 'assigned';
# ALTER TABLE valid_id MODIFY register_status VARCHAR(50) DEFAULT 'unregistered';
# ALTER TABLE item MODIFY item_status VARCHAR(50) DEFAULT 'unassigned';
# ALTER TABLE user MODIFY user_status VARCHAR(50) DEFAULT 'active';

