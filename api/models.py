from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime, date
from pydantic import BaseModel, Field
from typing import List, Optional

Base = declarative_base()

class Jugador(BaseModel):
    nombre:    Optional[str] = Field(...)
    apellido:  Optional[str] = Field(...)
    nif:                str  = Field(...)
    ciudad:    Optional[str] = Field(...)
    provincia: Optional[str] = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "nif": "123456789A",
                "nombre": "John",
                "apellido": "Doe",
                "ciudad": "Barcelona",
                "provincia": "Barcelona"
            }
        }

class Torneo(BaseModel):
    fecha:     date = Field(...)
    ciudad:    str  = Field(...)
    provincia: str  = Field(...)
    ganador:   str  = Field(...)

    class Config:
        json_schema_extra = {
            'example': {
                'fecha': '2024/05/01',
                'ciudad': 'Barcelona',
                'provincia': 'Barcelona',
                'ganador': '123456789A'
            }
        }
