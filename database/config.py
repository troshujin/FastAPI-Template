import os


class Config:
    DBUSER = os.getenv("db_user")
    DBPASSWORD = os.getenv("db_password")
    DB = os.getenv("db")
    SERVICE_HOST = os.getenv("service_host")