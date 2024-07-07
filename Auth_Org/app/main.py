from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, schemas, crud, database, auth

app = FastAPI()

models.Base.metadata.create_all(bind=database.engine)

@app.post("/auth/register", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/api/users/{user_id}", response_model=schemas.User)
def read_user(user_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    user = db.query(models.User).filter(models.User.userId == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/api/organisations", response_model=List[schemas.Organisation])
def read_organisations(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    return current_user.organisations

@app.get("/api/organisations/{org_id}", response_model=schemas.Organisation)
def read_organisation(org_id: str, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    organisation = db.query(models.Organisation).filter(models.Organisation.orgId == org_id).first()
    if organisation is None:
        raise HTTPException(status_code=404, detail="Organisation not found")
    if organisation not in current_user.organisations:
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return organisation

@app.post("/api/organisations", response_model=schemas.Organisation)
def create_organisation(org: schemas.OrganisationCreate, db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    organisation = models.Organisation(
        orgId=str(uuid.uuid4()),
        name=org.name,
        description=org.description
    )
    db.add(organisation)
    db.commit()
    db.refresh(organisation)

    current_user.organisations.append(organisation)
    db.commit()

    return organisation
