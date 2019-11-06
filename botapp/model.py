from flask_login import UserMixin
from sqlalchemy import create_engine
from sqlalchemy import Column, Integer, String, Text, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from werkzeug.security import generate_password_hash, check_password_hash

from botapp.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI)
metadata = MetaData(bind=engine)

Base = declarative_base()


class User(Base, UserMixin):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)

    def __init__(self, username, password, role, age, name, surname):
        self.username = username
        self.password = password
        self.role = role
        self.age = age
        self.name = name
        self.surname = surname

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User('{self.username}', '{self.name}', '{self.surname}', "\
               f"'{self.password}', '{self.user_age}')>"


class Values(Base):
    __tablename__ = 'values'
    id = Column(Integer, primary_key=True)
    value = Column(Text)

    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"<Value '{self.id}' '{self.value}'>"


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)


def user_registration():
    user_name = str(input("Enter user's name: ").strip())
    user_surname = str(input("Enter user's surname: ").strip())
    user_password = str(input("Enter user's password: ").strip())
    user_age = abs(int(input("Enter user's age: ").strip()))
    table = Table('users', metadata, autoload=True)
    ins = table.insert().values(name=user_name,
                                surname=user_surname,
                                password=user_password,
                                age=user_age
                                )
    conn = engine.connect()
    conn.execute(ins)


if __name__ == '__main__':
    # user_registration()
    print(Table('users', metadata, autoload=True).columns)
    print(Table('values', metadata, autoload=True).columns)
    for _t in metadata.tables:
        print(f"Table: '{_t}'")
