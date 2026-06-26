from fastapi import FastAPI
from app.api.v1.auth import router as auth_router
from app.db.session import engine, Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title='Auth Service')

@app.get('/health')
def health_check():
    return {"status": "ok", "service": "auth-service"}

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])