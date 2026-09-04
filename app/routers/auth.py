from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas import UserCreate, UserResponse, UserLogin, Token
from app.auth import create_access_token, verify_password
from app import crud

router = APIRouter()

@router.post('/register', response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db, user)


@router.post('/login', response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, credentials.email)
    if user is None:
        raise HTTPException(status_code=401, detail='Invalid Email or Password')
    if not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail='Invalid Email or Password')
    access_token = create_access_token({'sub': str(user.id)})
    return {'access_token': access_token, 'token_type': 'bearer'}
