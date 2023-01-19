from sqlalchemy.orm import Session


class DBSessionMixin:
    def __init__(self, session):
        self.session: Session = session


class AppService(DBSessionMixin):
    pass


class AppCRUD(DBSessionMixin):
    pass