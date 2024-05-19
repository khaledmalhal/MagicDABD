#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from time import sleep
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

q = "SELECT nif FROM practica.jugador LIMIT 10;"
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
    max_copias = randint(80, 100)
    # max_copias = randint(0, num_cartas[0] - 1)
    print("max_copias: %d" % (max_copias))
    inserted = []
    for j in range(max_copias):
      # print("copias: %d" % (copias), end="\r")
      rand_copias = randint(1, 10)
      carta_index = randint(0, num_cartas[0] - 1)
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
    q = "SELECT * FROM practica.copia WHERE propietario=%s"
    p = (jugadores[i][0], )
    cursor.execute(q, p)
    copias = cursor.fetchall()
    max_decks = randint(0, 3)
    print("%d copias for jugador %s" % (len(copias), jugadores[i][0]))
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

# create_jugadores(cursor)
# create_copias(cursor)
# create_deck(cursor)
# create_tienda(cursor)
create_inventario(cursor)
# print(end="\33[2K\r")
f.close()
conn.close()
