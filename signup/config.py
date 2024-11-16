import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:root@localhost/clinica'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
