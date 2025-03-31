import sys
import os
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from app.middlewares import add_cors

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi import FastAPI
from app.api.novels import router as novels_router
from app.database.settings import get_db

app = FastAPI()

add_cors(app)

@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Database connected!"}
app.include_router(novels_router)