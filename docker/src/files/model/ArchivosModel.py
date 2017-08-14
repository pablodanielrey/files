import uuid
import datetime
import base64
import requests

from sqlalchemy import or_
from sqlalchemy.orm import joinedload

from . import Session
from .exceptions import *
from .entities import *


class ArchivosModel:

    @staticmethod
    def _aplicar_filtros_comunes(q, offset, limit):
        q = q.offset(offset) if offset else q
        q = q.limit(limit) if limit else q
        return q

    @classmethod
    def archivos(cls, session, limit=None, offset=None):
        q = session.query(Archivo)
        cls._aplicar_filtros_comunes(q, offset, limit)
        return q.all()

    @classmethod
    def archivo(cls, session, fid, solo_contenido=False):
        q = session.query(Archivo).filter(Archivo.id == fid)
        arch = q.one()
        if solo_contenido:
            return arch.contenido
        else:
            return arch


    @classmethod
    def agregar_archivo(cls, session, nombre, contenido):
        print(contenido)
        arch = Archivo(
            nombre=nombre,
            contenido=contenido)
        session.add(arch)
