from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.users import UserCreate, UserOut, UserLogin, Token
from app.services import auth_service
from app.core.security import create_access_token
from app.api.deps import get_current_user

router = APIRouter()

@router.get("/me")
def read_users_me(current_user: dict = Depends(get_current_user)):
    return {
        "message": "Welcome to your profile!",
        "user_info": current_user
    }
@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(user_in: UserCreate, db: Session = Depends(get_db)):
    return auth_service.create_user(db, user_in)

@router.post("/login", response_model=Token)
def login(user_in: UserLogin, db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, user_in.email, user_in.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}