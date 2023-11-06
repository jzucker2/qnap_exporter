from sqlalchemy.sql import func, expression
from flask import current_app as app
from ..database import get_db


log = app.logger


db = get_db()


DEFAULT_ALL_LIMIT = 100


class BaseModelException(Exception):
    pass


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    # https://stackoverflow.com/questions/13370317/sqlalchemy-default-datetime
    creation_date = db.Column(
        db.DateTime(timezone=True),
        server_default=func.now())
    update_date = db.Column(
        db.DateTime(timezone=True),
        onupdate=func.now())

    @classmethod
    def model_name(cls):
        return str(cls.__name__)

    def __repr__(self):
        return f'{self.__class__.__name__}: ({self.id}), ' \
               f'====> ' \
               f'creation_date: {self.creation_date} | ' \
               f'update_date: {self.update_date} | '

    def get_json_dict(self):
        return {
            'id': self.id,
            'creation_date': self.creation_date,
        }

    @classmethod
    def get_latest_item(cls, database=None):
        if not database:
            database = get_db()
        id_order = expression.desc(cls.id)
        latest_order = expression.desc(cls.creation_date)
        order_by_expr = [id_order, latest_order]
        return database.session.query(cls).order_by(
            *order_by_expr).first()

    @classmethod
    def get_latest_item_json_response(cls, database=None):
        item = cls.get_latest_item(database=database)
        log.debug(f'latest_item got item: {item}')
        if item:
            return item.get_json_dict()

    @classmethod
    def save(cls, database=None):
        if not database:
            database = get_db()
        database.session.commit()
        log.debug('done saving!!!!')

    @classmethod
    def create(cls, database=None, **info):
        if not database:
            database = get_db()
        log.debug(f'create info: {info}')
        try:
            instance = cls(**info)
            log.debug(f'created unsaved instance: {instance}')
            database.session.add(instance)
            cls.save(database=database)
        except Exception as e:
            e_m = f'Encountered error saving ' \
                  f'instance: {info} with e: {e}'
            log.error(e_m)
            database.session.rollback()
        else:
            return instance

    @classmethod
    def latest_instance(cls, database=None):
        if not database:
            database = get_db()
        latest_order = expression.desc(cls.creation_date)
        return database.session.query(cls).order_by(
            latest_order).one_or_none()

    @classmethod
    def has_latest_instance(cls, database=None):
        return bool(cls.latest_instance(database=database))

    @classmethod
    def get_all(cls, limit=None, database=None):
        if not database:
            database = get_db()
        if not limit:
            limit = DEFAULT_ALL_LIMIT
            log.debug(f'limiting all to default: {limit}')
        latest_order = expression.desc(cls.creation_date)
        return database.session.query(cls).order_by(
            latest_order).limit(limit).all()

    @classmethod
    def get_json_response(cls, limit=None, database=None):
        items = cls.get_all(limit=limit, database=database)
        item_json = []
        if items:
            item_json = [i.get_json_dict() for i in items]
        response = {
            'model_name': cls.model_name(),
            'count': len(item_json),
            'items': item_json,
        }
        return response
