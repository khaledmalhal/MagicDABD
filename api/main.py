from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Jugador
from docs import tags_metadata
from decouple import config
import json
import psycopg2

app = FastAPI(title="MAGICDABD",
              description="Rest API con FastAPI",
              openapi_tags=tags_metadata)

origins = [
    "http://localhost:8000",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

conn = psycopg2.connect(
    host=config('host'),
    user=config('user'),
    password=config('password'),
    database=config('database'))
cursor = conn.cursor()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get('/jugadores', response_model=list[Jugador], tags=["jugadores"])
async def getAllJugadores():
    try:
        q = "SELECT nif, nombre, apellido, ciudad, provincia FROM practica.jugador";
        cursor.execute(q)
        ret = cursor.fetchall()
        columns = ['nif', 'nombre', 'apellido', 'ciudad', 'provincia']
        jugadores = []
        for row in ret:
            jugador = dict(zip(columns, row))
            jugadores.append(jugador)
        return jugadores
    except psycopg2.Error as e:
        print(e)
        conn.rollback()
