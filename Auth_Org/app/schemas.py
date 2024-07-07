from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    firstName: str
    lastName: str
    email: EmailStr
    password: str
    phone: str

class User(BaseModel):
    userId: str
    firstName: str
    lastName: str
    email: EmailStr
    phone: str

    class Config:
        orm_mode = True

class OrganisationCreate(BaseModel):
    name: str
    description: str

class Organisation(BaseModel):
    orgId: str
    name: str
    description: str

    class Config:
        orm_mode = True
