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
    def agregar_archivo(cls, session, fid, nombre, contenido):
        agregar = True
        arch = None
        if fid:
            arch = session.query(Archivo).filter(Archivo.id == fid).one_or_none()
            if arch:
                agregar = False

        if not arch:
            arch = Archivo()
            if fid:
                arch.id = fid

        arch.nombre = nombre
        arch.contenido = contenido

        arch = Archivo(
            id=fid,
            nombre=nombre,
            contenido=contenido)

        if agregar:
            session.add(arch)
