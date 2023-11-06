from flask import current_app as app
from ..database import get_db
from .base import BaseModel, BaseModelException


log = app.logger


db = get_db()


class AdminException(BaseModelException):
    pass


class Admin(BaseModel):
    __tablename__ = "admin"

    first_name = db.Column(db.String(100), nullable=True)
    last_name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)

    def get_json_dict(self):
        super_dict = super().get_json_dict()
        super_dict.update({
            'email': self.email,
        })
        return dict(super_dict)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __repr__(self):
        return f'Admin: ({self.id}), ' \
               f'====> ' \
               f'creation_date: {self.creation_date} | ' \
               f'update_date: {self.update_date} | ' \
               f'full_name: {self.full_name} | ' \
               f'email: {self.email} |'

    @classmethod
    def default_admin_info(cls):
        return {
            'first_name': 'Jordan',
            'last_name': 'Zucker',
            'email': 'jordan.zucker@gmail.com',
        }

    @classmethod
    def ensure_admin(cls, database=db):
        log.warning('Not implemented!')
