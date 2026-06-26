from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        user_id: str = payload.get("sub")
        role: str = payload.get("role")
        
        if user_id is None:
            raise credentials_exception
            
        return {"user_id": user_id, "role": role}
        
    except JWTError:
        raise credentials_exception

class RoleChecker:
    def __init__(self,allowed_roles:list):
        self.allowed_roles=allowed_roles
        
    async def __call__(self, current_user:dict=Depends(get_current_user)):
        if current_user["role"] not in self.allowed_roles:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="You do not have enough permissions to access this resource"
            )
        return current_user
    
allow_admin = RoleChecker(["admin"])
allow_any_user = RoleChecker(["admin", "user", "support"])   