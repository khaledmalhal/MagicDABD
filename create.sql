-- CONSTRAIN para Cartas:
-- * Si se elimina una carta de la base de datos. Se debe eliminar todas las referencias a él.
--   Cuando se elimina, se convierten en cartas que dejan de ser válidas o no oficiales.
-- * En teoría, el código de las cartas no se actualizan. Pero en caso de que lo haga, se actualiza en toda la base de datos.
--
-- CONSTRAIN para Jugador:
-- * Si se elimina un Jugador, se debe eliminar también sus decks y las cartas que posea.
-- * En el caso de torneos, se debe eliminar también.
-- * En una partida, se coloca a NULL, para que quede constancia de como ha ido el torneo.
--   Al igual que en una Transacción y Venta.
--
-- CONSTRAIN para Ciudad:
-- * Si se actualiza, se debe actualizar en toda la base de datos.
-- * No se puede eliminar la Ciudad en case de que hayan Jugadores, Torneos o Tiendas ahí. 
--   Se deben actualizar antes de poder eliminarse. Es un caso excepcional.

DROP TABLE practica.partida;
DROP TABLE practica.participante;
DROP TABLE practica.torneo;
DROP TABLE practica.vendida;
DROP TABLE practica.venta;
DROP TABLE practica.transaccion;
DROP TABLE practica.repetido;
DROP TABLE practica.deck;
DROP TABLE practica.copia;
DROP TABLE practica.jugador;
DROP TABLE practica.inventario;
DROP TABLE practica.tienda;
DROP TABLE practica.ciudad;
DROP TABLE practica.provincia;
-- DROP TABLE practica.carta;

SET search_path TO practica;

-- CREATE TABLE Carta (codigo VARCHAR(10) NOT NULL,
-- 		            nombre VARCHAR(150) NOT NULL,
-- 		            rareza VARCHAR(2) NOT NULL,
-- 		            tipo VARCHAR(50) NOT NULL,
-- 		            PRIMARY KEY (codigo));

CREATE TABLE Provincia (nombre VARCHAR(40) NOT NULL,
                        PRIMARY KEY (nombre));

CREATE TABLE Ciudad (nombre VARCHAR(100) NOT NULL,
                     provincia VARCHAR(40) NOT NULL,
                     FOREIGN KEY (provincia) REFERENCES Provincia(nombre)
                                             ON UPDATE CASCADE
                                             ON DELETE CASCADE,
                     PRIMARY KEY (nombre, provincia));

CREATE TABLE Tienda (nombre VARCHAR(100) NOT NULL,
                     telefono BIGINT NOT NULL CHECK (telefono < 1000000000 AND telefono > 99999999),
                     ciudad VARCHAR(100) NOT NULL,
                     provincia VARCHAR(40) NOT NULL,
                     PRIMARY KEY (nombre),
                     UNIQUE (telefono),
                     FOREIGN KEY (ciudad, provincia) REFERENCES Ciudad(nombre, provincia)
                                                     ON UPDATE CASCADE
                                                     ON DELETE RESTRICT);
  
CREATE TABLE Inventario (cantidad INT NOT NULL DEFAULT 1,
                         tienda VARCHAR(100) NOT NULL,
                         carta VARCHAR(10) NOT NULL,
                         PRIMARY KEY (tienda, carta),
                         FOREIGN KEY (tienda) REFERENCES Tienda(nombre)
                                              ON UPDATE CASCADE
                                              ON DELETE CASCADE,
                         FOREIGN KEY (carta) REFERENCES Carta(codigo)
                                             ON UPDATE CASCADE
                                             ON DELETE CASCADE);

CREATE TABLE Jugador (nif VARCHAR(9) NOT NULL,
                      nombre VARCHAR(25) NOT NULL,
                      apellido VARCHAR(40) NOT NULL,
                      ciudad VARCHAR(100) NOT NULL,
                      provincia VARCHAR(40) NOT NULL,
                      PRIMARY KEY (nif),
                      FOREIGN KEY (ciudad, provincia) REFERENCES Ciudad(nombre, provincia)
                                                      ON UPDATE CASCADE
                                                      ON DELETE RESTRICT);

CREATE TABLE Copia (cantidad INT NOT NULL DEFAULT 1,
                    carta VARCHAR(10) NOT NULL,
                    propietario VARCHAR(9) NOT NULL,
                    PRIMARY KEY (carta, propietario),
                    FOREIGN KEY (carta) REFERENCES Carta(codigo)
                                        ON UPDATE CASCADE
                                        ON DELETE CASCADE,
                    FOREIGN KEY (propietario) REFERENCES Jugador(nif)
                                              ON UPDATE CASCADE
                                              ON DELETE CASCADE);

CREATE TABLE Deck (id SERIAL,
                   creacion DATE NOT NULL DEFAULT CURRENT_DATE,
                   propietario VARCHAR(9) NOT NULL,
                   PRIMARY KEY (id, propietario),
                   FOREIGN KEY (propietario) REFERENCES Jugador(nif)
                                             ON UPDATE CASCADE
                                             ON DELETE CASCADE);

CREATE TABLE Repetido (cantidad INT NOT NULL DEFAULT 1,
                       carta VARCHAR(10) NOT NULL,
                       deck SERIAL,
                       propietario VARCHAR(40) NOT NULL,
                       PRIMARY KEY (carta, deck, propietario),
                       FOREIGN KEY (carta) REFERENCES Carta(codigo)
                                                      ON UPDATE CASCADE
                                                      ON DELETE CASCADE,
                       FOREIGN KEY (deck, propietario) REFERENCES Deck(id, propietario)
                                                       ON UPDATE CASCADE
                                                       ON DELETE CASCADE);

CREATE TABLE Transaccion (id SERIAL,
                          carta VARCHAR(10) NOT NULL,
                          cede VARCHAR(9),
                          recibe VARCHAR(9),
                          PRIMARY KEY (id),
                          FOREIGN KEY (carta) REFERENCES Carta(codigo)
                                              ON UPDATE CASCADE
                                              ON DELETE CASCADE,
                          FOREIGN KEY (cede) REFERENCES Jugador(nif)
                                             ON UPDATE CASCADE
                                             ON DELETE SET NULL,
                          FOREIGN KEY (recibe) REFERENCES Jugador(nif)
                                               ON UPDATE CASCADE
                                               ON DELETE SET NULL);

CREATE TABLE Venta (idfactura SERIAL,
                    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
                    vendedor VARCHAR(100) NOT NULL,
                    cliente VARCHAR(9),
                    PRIMARY KEY (idfactura, vendedor),
                    FOREIGN KEY (vendedor) REFERENCES Tienda(nombre)
                                           ON UPDATE CASCADE
                                           ON DELETE CASCADE,
                    FOREIGN KEY (cliente) REFERENCES Jugador(nif)
                                          ON UPDATE CASCADE
                                          ON DELETE SET NULL);

CREATE TABLE Vendida (cantidad INT NOT NULL DEFAULT 1,
                      carta VARCHAR(10) NOT NULL,
                      factura SERIAL,
                      vendedor VARCHAR(100) NOT NULL,
                      PRIMARY KEY (carta, factura),
                      FOREIGN KEY (carta) REFERENCES Carta(codigo)
                                          ON UPDATE CASCADE
                                          ON DELETE CASCADE,
                      FOREIGN KEY (factura, vendedor) REFERENCES Venta(idfactura, vendedor)
                                                      ON UPDATE CASCADE
                                                      ON DELETE CASCADE);

CREATE TABLE Torneo (fecha DATE NOT NULL,
                     ciudad VARCHAR(100) NOT NULL,
                     provincia VARCHAR(40) NOT NULL,
                     ganador VARCHAR(9),
                     PRIMARY KEY (fecha, ciudad, provincia),
                     FOREIGN KEY (ciudad, provincia) REFERENCES Ciudad(nombre, provincia)
                                                     ON UPDATE CASCADE
                                                     ON DELETE RESTRICT,
                     FOREIGN KEY (ganador) REFERENCES Jugador(nif)
                                                     ON UPDATE CASCADE
                                                     ON DELETE SET NULL);

CREATE TABLE Participante (jugador VARCHAR(9),
                           fecha DATE NOT NULL,
                           ciudad VARCHAR(100) NOT NULL,
                           provincia VARCHAR(40) NOT NULL,
                           PRIMARY KEY (jugador, fecha, ciudad, provincia),
                           FOREIGN KEY (jugador) REFERENCES Jugador(nif)
                                                 ON UPDATE CASCADE
                                                 ON DELETE SET NULL,
                           FOREIGN KEY (fecha, ciudad, provincia) REFERENCES Torneo(fecha, ciudad, provincia)
                                                                  ON UPDATE CASCADE
                                                                  ON DELETE CASCADE);

CREATE TABLE Partida (duelista1 VARCHAR(9),
                      duelista2 VARCHAR(9),
                      ganador VARCHAR(9) CHECK (ganador = duelista1 OR ganador = duelista2),
                      deck1 SERIAL,
                      deck2 SERIAL,
                      fecha DATE NOT NULL,
                      ciudad VARCHAR(100) NOT NULL,
                      provincia VARCHAR(40) NOT NULL,
                      PRIMARY KEY (duelista1, duelista2, fecha, ciudad, provincia),
                      FOREIGN KEY (duelista1) REFERENCES Jugador(nif)
                                              ON UPDATE CASCADE
                                              ON DELETE SET NULL,
                      FOREIGN KEY (duelista2) REFERENCES Jugador(nif)
                                              ON UPDATE CASCADE
                                              ON DELETE SET NULL,
                      FOREIGN KEY (deck1, duelista1) REFERENCES Deck(id, propietario)
                                          ON UPDATE CASCADE
                                          ON DELETE CASCADE,
                      FOREIGN KEY (deck2, duelista2) REFERENCES Deck(id, propietario)
                                          ON UPDATE CASCADE
                                          ON DELETE CASCADE,
                      FOREIGN KEY (fecha, ciudad, provincia) REFERENCES Torneo(fecha, ciudad, provincia)
                                                             ON UPDATE CASCADE
                                                             ON DELETE CASCADE,
                      FOREIGN KEY (ganador) REFERENCES Jugador(nif)
                                            ON UPDATE CASCADE
                                            ON DELETE SET NULL);
