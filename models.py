from sqlalchemy.dialects.postgresql import UUID
from flask_sqlalchemy import SQLAlchemy
import uuid
import datetime
from datetime import datetime
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

db = SQLAlchemy()

POSTGRES = {
    'user': 'postgres',
    'pw': 'postgres',
    'db': 'plex_downloads_local',
    'host': 'localhost',
    'port': '5432',
}
engine = create_engine('postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES)

session_factory = sessionmaker(bind=engine, autocommit=False)
Session = scoped_session(session_factory)

class BaseModel(db.Model):
    """Base data model for all objects"""
    __abstract__ = True

    def __init__(self, *args):
        super().__init__(*args)

    def __repr__(self):
        """Define a base way to print models"""
        return '%s(%s)' % (self.__class__.__name__, {
            column: value
            for column, value in self._to_dict().items()
        })

    def json(self):
        """
                Define a base way to jsonify models, dealing with datetime objects
        """
        return {
            column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
            for column, value in self._to_dict().items()
        }

class Download(BaseModel, db.Model):
    """Model for the downloads table"""
    __tablename__ = 'downloads'

    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, unique=True)
    download_link = db.Column(db.String(1000))
    path = db.Column(db.String(1000))
    status = db.Column(db.String(100))
    downloaded_bytes = db.Column(db.String(100))
    total_bytes = db.Column(db.String(100))
    start_time = db.Column(db.DateTime)
    last_update = db.Column(db.DateTime)

    def __init__(self, id, download_link, path, status, downloaded_bytes, total_bytes, start_time, last_update=datetime.now()):
        """ Create a new Download """
        self.id = id
        self.download_link = download_link
        self.path = path
        self.status = status
        self.downloaded_bytes = downloaded_bytes
        self.total_bytes = total_bytes
        self.start_time = start_time
        self.last_update = last_update
