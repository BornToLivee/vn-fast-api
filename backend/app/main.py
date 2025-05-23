import os
import sys

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

from app.api.novels import router as novels_router
from app.api.tags import router as tags_router
from app.database.settings import get_db
from app.middlewares import add_cors

app = FastAPI()

add_cors(app)


@app.get("/test-db")
def test_db(db: Session = Depends(get_db)):
    return {"message": "Database connected!"}


app.include_router(novels_router)
app.include_router(tags_router)
