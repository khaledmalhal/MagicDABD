#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import psycopg2

def query(c, q, p):
    c.execute(q, p)

provincia_file = open("sql/lista_provincias.sql", "r")

conn = psycopg2.connect(database="est_b7241743",
                        user="est_b7241743",
                        password="dB.b7241743",
                        host="ubiwan.epsevg.upc.edu")
cursor = conn.cursor()
cursor.execute(provincia_file.read())
cursor.execute("SELECT idProvincia, Provincia FROM PROVINCIAS;")
provincias = cursor.fetchall()
conn.rollback()

# print(provincias)
insertQuery = "INSERT INTO practica.provincia (nombre) VALUES (%s);"
i = 1
for provincia in provincias:
    try:
        print("INSERTING provincia into Database (%d of \t%d)" % (i, len(provincias)), end='\r')
        nombre = provincia[1]
        print(cursor.mogrify(insertQuery, (nombre, )))
        query(cursor, insertQuery, (nombre, ))
    except psycopg2.Error as e:
        print(e)
        conn.rollback()
    i=i+1
conn.commit()

print("")
ciudades_file = open("sql/lista_municipios.sql", "r")
cursor.execute(ciudades_file.read())
cursor.execute("SELECT idProvincia, Municipio FROM MUNICIPIOS;")
ciudades = cursor.fetchall()
conn.rollback()

insertQuery = "INSERT INTO practica.ciudad (nombre, provincia) VALUES(%s, %s);"
provincias=dict(provincias)

i = 1
for ciudad in ciudades:
    try:
        nombre = ciudad[1]
        provincia = provincias[ciudad[0]]
        # print("Provincia: %s\tCiudad: %s" % (provincia, nombre))
        print("INSERTING ciudad into Database (%d of \t%d)" % (i, len(ciudades)), end='\r')
        query(cursor, insertQuery, (nombre, provincia, ))
    except psycopg2.Error as e:
        print(e)
        conn.rollback()
    i = i+1
conn.commit()
conn.close()