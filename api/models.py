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

class Participante(BaseModel):
    jugador:   str = Field(...)
    ciudad:    str = Field(...)
    provincia: str = Field(...)
    fecha:     date = Field(...)

    class Config:
        json_schema_extra = {
            'example': {
                'fecha': '2024/05/01',
                'ciudad': 'Barcelona',
                'provincia': 'Barcelona',
                'jugador': '123456789A'
            }
        }

class Partida(BaseModel):
    duelista1: str = Field(...)
    duelista2: str = Field(...)
    ganador: str = Field(...)
    deck1: int = Field(...)
    deck2: int = Field(...)
    ciudad:    str = Field(...)
    provincia: str = Field(...)
    fecha:     date = Field(...)

    class Config:
        json_schema_extra = {
            'example': {
                'duelista1': '123456789A',
                'duelista2': '987654321B',
                'deck1': '1',
                'deck2': '2',
                'fecha': '2024/05/01',
                'ciudad': 'Barcelona',
                'provincia': 'Barcelona',
                'ganador': '123456789A'
            }
        }

class Ciudad(BaseModel):
    ciudades: list = Field(...)
    provincia: str = Field(...)

    class Config:
        json_schema_extra = {
            'ciudad': "Barcelona",
            'provincia': 'Barcelona'
        }