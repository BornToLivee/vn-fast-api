import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend')))

# import pytest
# from fastapi.testclient import TestClient
# from sqlalchemy import create_engine, StaticPool
# from sqlalchemy.orm import sessionmaker
# from unittest.mock import MagicMock

# from app.main import app
# from app.database.settings import get_db
# from app.models.base import Base

# SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False},
#     poolclass=StaticPool
# )
# TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# client = TestClient(app)

# def override_get_db():
#     try:
#         db = TestingSessionLocal()
#         yield db
#     finally:
#         db.close()

# def set_up():
#     Base.metadata.create_all(bind=engine)

# def tear_down():
#     Base.metadata.drop_all(bind=engine)


# app.dependency_overrides[get_db] = override_get_db