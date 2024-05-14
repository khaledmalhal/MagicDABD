#! /usr/bin/python3

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

q = "SELECT DISTINCT row_number() over (order by '') as \"#\", name, number, setCode, type, rarity FROM cards WHERE printf(\"%d\", number) = number;"
res = card_conn.execute(q)
cards = res.fetchall()

c.execute("SET search_path TO practica;")
conn.commit()

insertQuery = "INSERT INTO Cartas (codigo, nombre, rareza, tipo) VALUES (?, ?, ?, ?);"
cardRow = 1
cardTotal = len(cards)
for card in cards:
    cardName    = card[1]
    cardNumber  = card[2]
    cardSetCode = card[3]
    cardType    = card[4]
    cardRarity  = card[5]
    cartaRareza = 'C'
    print("INSERTING card into Database (%d of \t%d)" % (cardRow, cardTotal), end='\r')
    sleep(0.5)
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
    while success is False:
        try:
            # query(c, insertQuery, (cartaCodigo, cardName, cartaRareza, cardType))
            success = True
            cardRow = cardRow + 1
        except:
            sleep(1)
            print("Error")