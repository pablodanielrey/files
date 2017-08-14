from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, DateTime, LargeBinary
from sqlalchemy.orm import relationship

from model_utils import Base


class Archivo(Base):

    __tablename__ = 'archivos'
    __table_args__ = ({'schema': 'archivos'})

    nombre = Column(String)
    contenido = Column(String)
    tipo = Column(String)
