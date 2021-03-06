import os
import base64
import requests

from sqlalchemy import create_engine
from sqlalchemy.schema import CreateSchema
from sqlalchemy.orm import sessionmaker

from model_utils import Base
from .entities import *

engine = create_engine('postgresql://{}:{}@{}:5432/{}'.format(
    os.environ['FILES_DB_USER'],
    os.environ['FILES_DB_PASSWORD'],
    os.environ['FILES_DB_HOST'],
    os.environ['FILES_DB_NAME']
), echo=True)

Session = sessionmaker(bind=engine, autoflush=False, autocommit=False)

def crear_tablas():
    #engine.execute(CreateSchema('users'))
    Base.metadata.create_all(engine)


from .ArchivosModel import ArchivosModel

__all__ = [
    'ArchivosModel'
]
