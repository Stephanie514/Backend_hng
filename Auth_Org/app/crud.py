from sqlalchemy.orm import Session
from . import models, schemas
import uuid
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        userId=str(uuid.uuid4()),
        firstName=user.firstName,
        lastName=user.lastName,
        email=user.email,
        password=hashed_password,
        phone=user.phone,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    # Create default organisation
    org = models.Organisation(
        orgId=str(uuid.uuid4()),
        name=f"{user.firstName}'s Organisation",
        description="Default organisation"
    )
    db.add(org)
    db.commit()
    db.refresh(org)

    db_user.organisations.append(org)
    db.commit()

    return db_user

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def authenticate_user(db: Session, email: str, password: str):
    user = get_user_by_email(db, email)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user
