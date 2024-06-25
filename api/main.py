from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from models import Jugador, Torneo, Participante, Partida, Ciudad
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
        q = "SELECT nif, nombre, apellido, ciudad, provincia FROM practica.jugador;"
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

@app.get('/torneos', response_model=list[Torneo], tags=['torneo'])
async def getAllTorneos():
    try:
        q = "SELECT fecha, ciudad, provincia, ganador FROM practica.torneo;"
        cursor.execute(q)
        ret = cursor.fetchall()
        columns = ['fecha', 'ciudad', 'provincia', 'ganador']
        torneos = []
        for row in ret:
            torneo = dict(zip(columns, row))
            torneos.append(torneo)
        return torneos
    except psycopg2.Error as e:
        print(e)
        conn.rollback()

@app.get('/participantes', response_model=list[Participante], tags=['participante'])
async def getParticipantes(fecha: str, ciudad: str, provincia: str):
    try:
        q = """SELECT jugador from practica.participante WHERE
               fecha = %s AND ciudad = %s AND provincia = %s"""
        p = (fecha, ciudad, provincia, )
        cursor.execute(q, p)
        ret = cursor.fetchall()
        participantes = []
        for row in ret:
            participante = dict(zip(['jugador'], row))
            participantes.append(participante)
        return participantes
    except psycopg2.Error as e:
        print(e)
        conn.rollback()

@app.get('/partidas', response_model=list[Partida], tags=['partida'])
async def getPartidas(fecha: str, ciudad: str, provincia: str):
    try:
        q = """SELECT duelista1, duelista2, ganador, deck1, deck2
               FROM practica.partida WHERE fecha = %s AND ciudad = %s AND provincia = %s"""
        p = (fecha, ciudad, provincia, )
        print(cursor.mogrify(q, p))
        cursor.execute(q, p)
        ret = cursor.fetchall()
        columns = ['duelista1', 'duelista2', 'ganador', 'deck1', 'deck2', 'ciudad', 'provincia', 'fecha']
        partidas = []
        for row in ret:
            partida = dict(zip(columns, row + (ciudad, provincia, fecha)))
            partidas.append(partida)
        print(partidas)
        return partidas
    except psycopg2.Error as e:
        print(e)
        conn.rollback()

@app.get('/ciudades', response_model=list[Ciudad], tags=['ciudad'])
async def getCiudades():
    try:
        q = "SELECT provincia FROM practica.provincia;"
        cursor.execute(q)
        provincias = [r[0] for r in cursor.fetchall()]
        # provincias = cursor.fetchall()
        ciudades = []
        for provincia in provincias:
            provincia = provincia.replace('(','').replace(')','').replace('"','')
            # print(type(provincia))
            q = "SELECT nombre FROM practica.ciudad WHERE provincia = %s;"
            cursor.execute(q, (provincia, ))
            list_ciudades = [r[0] for r in cursor.fetchall()]
            ciudades.append(dict(provincia=provincia, ciudades=list_ciudades))
        return ciudades
    except psycopg2.Error as e:
        print(e)
        conn.rollback()    
