#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from time import sleep
from datetime import datetime
from random import randint
from faker import Faker
import psycopg2

vowels = ('a', 'e', 'i', 'o', 'u')
somecons = ('b', 'd', 'f', 'k', 'l', 'm', 'p', 'r', 's')
nifLetters = ('T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B',
              'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K', 'E')

fake = Faker('es_ES')

num_jugadores = 5000

def query(c, q, p):
  c.execute(q, p)

def r(lim):
  "0 <= random int < lim"
  return randint(0, lim-1)

def randname(syll):
  "random name with syll 2-letter syllables"
  v = len(vowels)
  c = len(somecons)
  res = str()
  for i in range(syll):
    res += somecons[r(c)] + vowels[r(v)]
  return res.capitalize()

conn = psycopg2.connect(database="est_b7241743",
                        user="est_b7241743",
                        password="dB.b7241743",
                        host="ubiwan.epsevg.upc.edu")
cursor = conn.cursor()

if os.path.isfile('queries.sql'):
  os.remove('queries.sql')
f = open('queries.sql', 'a')

# Obteniendo ciudades
q = "SELECT nombre, provincia FROM practica.ciudad;"
cursor.execute(q)
ciudades = cursor.fetchall()
lenCiudades = len(ciudades)

q = "SELECT codigo FROM practica.carta;"
cursor.execute(q)
cartas = cursor.fetchall()

q = "SELECT nif FROM practica.jugador ORDER BY RANDOM();"
cursor.execute(q)
jugadores = cursor.fetchall()

q = "SELECT COUNT(*) FROM practica.carta;"
cursor.execute(q)
num_cartas = cursor.fetchone()

q = "SELECT nombre FROM practica.tienda;"
cursor.execute(q)
tiendas = cursor.fetchall()

def get_nif():
  nif = randint(10000000, 99999999)
  nif = str(nif) + nifLetters[(nif % 23)-1]
  return nif


def create_jugadores(cursor):
  q = "INSERT INTO practica.jugador (nif, nombre, apellido, ciudad, provincia) VALUES (%s, %s, %s, %s, %s)"
  for i in range(num_jugadores):
    print("INSERTING Jugadores (%d of %d)" % (i, num_jugadores), end="\r")
    nombre    = randname(randint(2, 3))
    apellido  = randname(randint(3, 4))
    nif       = get_nif()
    randIndex = r(lenCiudades)
    ciudad    = ciudades[randIndex][0]
    provincia = ciudades[randIndex][1]
    try:
      # print(cursor.mogrify(q, (nif, nombre, apellido, ciudad, provincia,)))
      query(cursor, q, (nif, nombre, apellido, ciudad, provincia,))
    except psycopg2.Error as e:
      print(e)
      conn.rollback()
  conn.commit()

def create_copias(cursor):
  for i in range(len(jugadores) - 1):
    max_copias = randint(40, 70)
    inserted = []
    print("Creando copias para jugadores (%d de %d)" % (i, len(jugadores) - 1), end='\r')
    for j in range(max_copias):
      rand_copias = randint(1, 10)
      carta_index = randint(0, len(cartas) - 1)
      carta = cartas[carta_index][0]
      q = "INSERT INTO practica.copia (cantidad, carta, propietario) VALUES (%s, %s, %s)"
      p = (rand_copias, carta, jugadores[i][0], )
      try:
        if carta not in inserted:
          inserted.append(carta)
          f.write(str(cursor.mogrify(q, p)) + '\n')
          query(cursor, q, p)
      except psycopg2.Error as e:
        print(e)
        conn.rollback()
  conn.commit()

def create_deck(cursor):
  for i in range(len(jugadores) - 1):
    print("Creando deck para jugadores (%d de %d)" % (i, len(jugadores) - 1), end='\r')
    q = "SELECT * FROM practica.copia WHERE propietario=%s"
    p = (jugadores[i][0], )
    cursor.execute(q, p)
    copias = cursor.fetchall()
    max_decks = randint(1, 3)
    for j in range(max_decks):
      q = "INSERT INTO practica.deck (propietario) VALUES (%s)"
      p = (jugadores[i][0], )
      query(cursor, q, p)
      q = "SELECT id FROM practica.deck WHERE propietario=%s ORDER BY id DESC LIMIT 1"
      cursor.execute(q, p)
      deckID = cursor.fetchone()[0]
      maxRepetido = randint(30, 60)
      repetidos = 0
      inserted = []
      while repetidos < maxRepetido and len(inserted) < len(copias):
        randIndex    = randint(0, len(copias) - 1)
        carta        = copias[randIndex][1]
        cantidad     = copias[randIndex][0]
        randCantidad = randint(1, cantidad)
        if randCantidad + repetidos > maxRepetido:
          randCantidad = maxRepetido - repetidos
        if carta not in inserted:
          try:
            q = "INSERT INTO practica.repetido (cantidad, carta, deck, propietario) VALUES (%s, %s, %s, %s);"
            p = (randCantidad, carta, deckID, jugadores[i][0], )
            inserted.append(carta)
            f.write(str(cursor.mogrify(q, p)) + "\n")
            query(cursor, q, p)
            repetidos += randCantidad
          except psycopg2.Error as e:
            print(e)
            conn.rollback()
  conn.commit()

def create_tienda(cursor):
  for i in range(1487):
    nombre = randname(randint(2,3)) + ' ' + fake.company()
    randCiudad = randint(0, len(ciudades) - 1)
    telefono = fake.phone_number()
    q = "INSERT INTO practica.tienda (nombre, telefono, ciudad, provincia) VALUES (%s, %s, %s, %s);"
    p = (nombre, telefono, ciudades[randCiudad][0], ciudades[randCiudad][1])
    insertedNombre = []
    insertedTelefono = []
    try:
      if nombre not in insertedNombre and telefono not in insertedTelefono:
        f.write(str(cursor.mogrify(q, p)) + "\n")
        query(cursor, q, p)
        insertedNombre.append(nombre)
        insertedTelefono.append(telefono)
    except psycopg2.Error as e:
      print(e)
      conn.rollback()
  conn.commit()

def create_inventario(cursor):
  for i in range(len(tiendas) - 1):
    randCartas = randint(50, 200)
    inserted = []
    print("Inventario tienda %d de %d" % (i, len(tiendas)), end='\r')
    for j in range(randCartas):
      randIndex = randint(0, len(cartas) - 1)
      randCantidad = randint(20, 100)
      carta = cartas[randIndex][0]
      q = "INSERT INTO practica.inventario (cantidad, tienda, carta) VALUES (%s, %s, %s);"
      p = (randCantidad, tiendas[i][0], carta,)
      try: 
        if carta not in inserted:
          f.write(str(cursor.mogrify(q, p)) + "\n")
          query(cursor, q, p)
          inserted.append(carta)
      except psycopg2.Error as e:
        print(e)
        conn.rollback()
  conn.commit()

def simulate_tournament(cursor, participantes, fecha, ciudad, provincia):
  if len(participantes) == 1:
    return participantes[0]
  duelo = participantes.copy()
  for x in range(0, len(duelo) - 1, 2):
    q = "SELECT id FROM practica.deck WHERE propietario=%s ORDER BY RANDOM() LIMIT 1;"
    p = (duelo[x],)
    cursor.execute(q, p)
    deck1 = cursor.fetchone()[0]
    p = (duelo[x+1],)
    cursor.execute(q, p)
    deck2 = cursor.fetchone()[0]
    randGanador = randint(x, x+1)
    ganador = duelo[randGanador]
    if randGanador % 2 == 0:
      perdedor = duelo[x+1]
    else:
      perdedor = duelo[x]
    try:
      q = "INSERT INTO practica.partida (duelista1, duelista2, ganador, deck1, deck2, fecha, ciudad, provincia) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
      p = (duelo[x], duelo[x+1], ganador, deck1, deck2, fecha, ciudad, provincia, )
      f.write(str(cursor.mogrify(q, p)) + "\n")
      cursor.execute(q, p)
      participantes.remove(perdedor)
    except psycopg2.Error as e:
      print(e)
      conn.rollback()
  return simulate_tournament(cursor, participantes, fecha, ciudad, provincia)


def create_torneos(cursor):
  for i in range(150):
    print("Simulando torneo (%d de %d)" % (i, 100), end='\r')
    numParticipantes = randint(2, 6)
    numParticipantes = pow(2, numParticipantes)
    participantes = []
    randCity = randint(0, len(ciudades) - 1)
    ciudad = ciudades[randCity][0]
    provincia = ciudades[randCity][1]
    fecha = fake.date_between_dates(date_start=datetime(2015,1,1), date_end=datetime(2024,5,20))

    try:
      q = "INSERT INTO practica.torneo (ciudad, provincia, fecha) VALUES (%s, %s, %s)"
      p = (ciudad, provincia, fecha, )
      f.write(str(cursor.mogrify(q, p)) + "\n")
      cursor.execute(q, p)
    except psycopg2.Error as e:
      print(e)
      conn.rollback()

    while len(participantes) < numParticipantes:
      jugador = jugadores[randint(0, len(jugadores) - 1)][0]
      if jugador not in participantes:
        participantes.append(jugador)
        try:
          q = "INSERT INTO practica.participante (jugador, ciudad, provincia, fecha) VALUES (%s, %s, %s, %s)"
          p = (jugador, ciudad, provincia, fecha, )
          f.write(str(cursor.mogrify(q, p)) + "\n")
          cursor.execute(q, p)
        except psycopg2.Error as e:
          print(e)
          conn.rollback()
    ganador = str(simulate_tournament(cursor, participantes.copy(), fecha, ciudad, provincia))
    try:
      q = "UPDATE practica.torneo SET ganador=%s WHERE ciudad=%s AND provincia=%s AND fecha=%s;"
      p = (ganador, ciudad, provincia, fecha, )
      f.write(str(cursor.mogrify(q, p)) + "\n")
      cursor.execute(q, p)
    except psycopg2.Error as e:
      print(e)
      conn.rollback()
    
  conn.commit()

def create_venta(cursor):
  random_cliente = True
  for i in range(10000):
    print("Venta de tienda %d de %d" % (i, 10000), end='\r')
    if random_cliente is True:
      q = """SELECT nif FROM practica.jugador j
           WHERE NOT EXISTS 
           (SELECT * FROM practica.Venta WHERE cliente = j.nif)
           ORDER BY RANDOM() LIMIT 1;"""
      cursor.execute(q)
      cliente = cursor.fetchall()
      if len(cliente) == 0:
        random_cliente = False
      else:
        cliente = cliente[0]
    if random_cliente is False:
      cliente = jugadores[randint(0, len(jugadores) - 1)]

    tienda = tiendas[randint(0, len(tiendas) - 1)]
    fecha = fake.date_between_dates(date_start=datetime(2015,1,1), date_end=datetime(2024,5,20))

    q = "INSERT INTO practica.venta (fecha, vendedor, cliente) VALUES (%s, %s, %s);"
    p = (fecha, tienda, cliente, )
    cursor.execute(q, p)
  conn.commit()

def insert_carta(cursor, jugador, carta, cantidad):
  q = "SELECT carta FROM practica.copia WHERE carta = %s AND propietario = %s;"
  p = (carta, jugador, )
  cursor.execute(q, p)
  exist = cursor.fetchone()
  if exist is None:
    q = "INSERT INTO practica.copia (cantidad, carta, propietario) VALUES (%s, %s, %s);"  
  else:
    q = "UPDATE practica.copia SET cantidad = cantidad + %s WHERE carta = %s AND propietario = %s;"
  p = (cantidad, carta, jugador,)
  # f.write(str(cursor.mogrify(q, p)) + "\n")
  cursor.execute(q, p)

def create_vendida(cursor):
  q = "SELECT idfactura, cliente, vendedor FROM practica.venta;"
  cursor.execute(q)
  ventas = cursor.fetchall()
  for i in range(len(ventas) - 1):
    print("Cartas vendidas %d de %d" % (i, len(ventas) - 1), end='\r')
    factura  = ventas[i][0]
    cliente  = ventas[i][1]
    vendedor = ventas[i][2]
    q = """SELECT carta, cantidad FROM practica.inventario 
           WHERE tienda = %s AND cantidad > 10 ORDER BY RANDOM();"""
    p = (vendedor, )
    cursor.execute(q, p)
    inventario = cursor.fetchall()
    if len(inventario) == 0:
      f.write("Skipping empty inventario " + ventas[i][2] + "\n")
      continue
    vendidas = randint(1, len(inventario) - 1)
    for j in range(vendidas):
      carta = inventario[j][0]
      cant_inv = inventario[j][1]
      cantidad = randint(1, int(cant_inv / 6))
      try:
        q = """INSERT INTO practica.vendida (cantidad, carta, factura, vendedor) VALUES (%s, %s, %s, %s);"""
        p = (cantidad, carta, factura, vendedor, )
        # f.write(str(cursor.mogrify(q, p)) + "\n")
        cursor.execute(q, p)
        q = """UPDATE practica.inventario 
               SET cantidad = cantidad - %s WHERE tienda = %s AND carta = %s;"""
        p = (cantidad, vendedor, carta, )
        # f.write(str(cursor.mogrify(q, p)) + "\n")
        cursor.execute(q, p)
        insert_carta(cursor, cliente, carta, cantidad)
      except psycopg2.Error as e:
        print(e)
        conn.rollback()
  conn.commit()

def create_transaccion(cursor):
  randjugadores = randint((len(jugadores)/2), len(jugadores)-1)
  q = "SELECT cantidad, carta, propietario FROM practica.copia;"
  cursor.execute(q)
  copia_array = cursor.fetchall()
  copia = []
  for c in copia_array:
    obj = {}
    obj['cantidad']    = c[0]
    obj['carta']       = c[1]
    obj['propietario'] = c[2]
    copia.append(obj)
  print(len(copia))
  for i in range(randjugadores):
    print("Transaccion %d de %d" % (i, randjugadores), end='\r')
    cede = jugadores[i]
    copias = [x for x in copia if x['propietario'] == cede[0]]
    if len(copias) == 0:
      continue
    for j in range(len(copias) - 1):
      cantidad = copias[j]['cantidad']
      carta = copias[j]['carta']
      rand_cantidad = randint(1, max(1, cantidad - 1))
      for z in range(rand_cantidad):
        recibe = jugadores[randint(0, len(jugadores) - 1)]
        insert_carta(cursor, recibe, carta, 1)
        try:
          q = "INSERT INTO practica.transaccion (carta, cede, recibe) VALUES (%s, %s, %s);"
          p = (carta, cede, recibe, )
          # f.write(str(cursor.mogrify(q, p)) + "\n")
          cursor.execute(q, p)
        except psycopg2.Error as e:
          print(e)
          conn.rollback()
      try:
        q = """UPDATE practica.copia SET cantidad = cantidad - %s WHERE carta = %s AND propietario = %s"""
        p = (rand_cantidad, carta, cede, )
        # f.write(str(cursor.mogrify(q, p)) + "\n")
        cursor.execute(q, p)
      except psycopg2.Error as e:
        print(e)
        conn.rollback()
  conn.commit()



  

# create_jugadores(cursor)
# create_copias(cursor)
# create_deck(cursor)
# create_tienda(cursor)
# create_inventario(cursor)
# create_torneos(cursor)
# create_venta(cursor)
# create_vendida(cursor)
create_transaccion(cursor)
# print(end="\33[2K\r")
f.close()
conn.close()
