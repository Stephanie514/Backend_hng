from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    userId = Column(String, primary_key=True, index=True, unique=True)
    firstName = Column(String, nullable=False)
    lastName = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    phone = Column(String)

    organisations = relationship("Organisation", secondary="user_organisation")

class Organisation(Base):
    __tablename__ = "organisations"

    orgId = Column(String, primary_key=True, index=True, unique=True)
    name = Column(String, nullable=False)
    description = Column(String)

user_organisation = Table(
    'user_organisation', Base.metadata,
    Column('user_id', ForeignKey('users.userId')),
    Column('organisation_id', ForeignKey('organisations.orgId'))
)
