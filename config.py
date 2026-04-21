import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "devkey")
    SQLALCHEMY_DATABASE_URI = "sqlite:///expenseiq.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
