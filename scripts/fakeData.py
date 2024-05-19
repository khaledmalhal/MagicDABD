#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

# Obteniendo ciudades
q = "SELECT nombre, provincia FROM practica.ciudad;"
cursor.execute(q)
ciudades = cursor.fetchall()
lenCiudades = len(ciudades)
conn.commit()

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


create_jugadores(cursor)
# print(end="\33[2K\r")
