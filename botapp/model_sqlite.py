from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, index=True, unique=True, nullable=False)
    password = Column(String, nullable=False)
    role = Column(String, nullable=False)
    age = Column(Integer, nullable=True)
    name = Column(String, nullable=True)
    surname = Column(String, nullable=True)

    def __repr__(self):
        return '<News'