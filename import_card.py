#! /usr/bin/python3
# -*- coding: utf-8 -*-

from psycopg2 import Error
import psycopg2
import sqlite3
from time import sleep

def query(c, q, p):
    c.execute(q, p)

card_conn = sqlite3.connect("AllPrintings.sqlite")

conn = psycopg2.connect(dbname="est_b7241743",
                        user="est_b7241743",
                        password="dB.b7241743",
                        host="ubiwan.epsevg.upc.edu")
c = conn.cursor()

q = "SELECT DISTINCT name, number, setCode, type, rarity FROM cards WHERE printf(\"%d\", number) = number AND language=\"English\" GROUP BY setCode, number;"
res = card_conn.execute(q)
cards = res.fetchall()
card_conn.close()

# try:
#     c.execute("SET search_path TO practica;")
# except Error as e:
#     print(e)
# conn.commit()

insertQuery = "INSERT INTO practica.carta (codigo, nombre, rareza, tipo) VALUES (%s, %s, %s, %s);"
cardRow = 1
cardTotal = len(cards)

for card in cards:
    cardName    = card[0]
    cardNumber  = card[1]
    cardSetCode = card[2]
    cardType    = card[3]
    cardRarity  = card[4]
    cartaRareza = 'C'
    print("INSERTING card into Database (%d of \t%d)" % (cardRow, cardTotal), end='\r')
    cartaCodigo = cardNumber+"/"+cardSetCode
    match cardRarity:
        case 'common':
            cartaRareza = 'C'
        case 'uncommon':
            cartaRareza = 'U'
        case 'rare':
            cartaRareza = 'R'
        case 'mythic':
            cartaRareza = 'MR'
        case 'special':
            cartaRareza = 'S'
        case 'bonus':
            cartaRareza = 'B'
        case default:
            cartaRareza = 'C'
    success = False
    with open('queries.sql', 'w') as f:
        try:
            # print(c.mogrify(insertQuery, (cartaCodigo, cardName, cartaRareza, cardType, )))
            query(c, insertQuery, (cartaCodigo, cardName, cartaRareza, cardType, ))
            f.write(str(c.mogrify(insertQuery, (cartaCodigo, cardName, cartaRareza, cardType, )))+"\n")
            success = True
            cardRow = cardRow + 1
        except Error as e:
            # sleep(1)
            print(e)
            conn.rollback()
conn.commit()
c.close()
