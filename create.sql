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


CREATE TABLE Carta (codigo TEXT NOT NULL,
		            nombre TEXT NOT NULL,
		            rareza VARCHAR(2) NOT NULL,
		            tipo TEXT NOT NULL,
		            PRIMARY KEY (codigo));

CREATE TABLE Provincia (nombre TEXT NOT NULL,
                        PRIMARY KEY (nombre));

CREATE TABLE Ciudad (nombre TEXT NOT NULL,
                     provincia TEXT NOT NULL,
                     FOREIGN KEY (provincia) REFERENCES Provincia(nombre)
                                             ON UPDATE CASCADE
                                             ON DELETE CASCADE,
                     PRIMARY KEY (nombre, provincia));

CREATE TABLE Tienda (nombre TEXT NOT NULL,
                     telefono BIGINT NOT NULL CHECK (telefono < 1000000000 AND telefono > 99999999),
                     ciudad TEXT NOT NULL,
                     provincia TEXT NOT NULL,
                     PRIMARY KEY (nombre),
                     UNIQUE (telefono),
                     FOREIGN KEY (ciudad, provincia) REFERENCES Ciudad(nombre, provincia)
                                                     ON UPDATE CASCADE
                                                     ON DELETE RESTRICT);
  
CREATE TABLE Inventario (cantidad INT NOT NULL DEFAULT 1,
                         tienda TEXT NOT NULL,
                         carta TEXT NOT NULL,
                         PRIMARY KEY (tienda, carta),
                         FOREIGN KEY (tienda) REFERENCES Tienda(nombre)
                                              ON UPDATE CASCADE
                                              ON DELETE CASCADE,
                         FOREIGN KEY (carta) REFERENCES Carta(codigo)
                                             ON UPDATE CASCADE
                                             ON DELETE CASCADE);

CREATE TABLE Jugador (nif TEXT NOT NULL,
                      nombre TEXT NOT NULL,
                      apellido TEXT NOT NULL,
                      ciudad TEXT NOT NULL,
                      provincia TEXT NOT NULL,
                      PRIMARY KEY (nif),
                      FOREIGN KEY (ciudad, provincia) REFERENCES Ciudad(nombre, provincia)
                                                      ON UPDATE CASCADE
                                                      ON DELETE RESTRICT);

CREATE TABLE Copia (cantidad INT NOT NULL DEFAULT 1,
                    carta TEXT NOT NULL,
                    propietario TEXT NOT NULL,
                    PRIMARY KEY (carta, propietario),
                    FOREIGN KEY (carta) REFERENCES Carta(codigo)
                                        ON UPDATE CASCADE
                                        ON DELETE CASCADE,
                    FOREIGN KEY (propietario) REFERENCES Jugador(nif)
                                              ON UPDATE CASCADE
                                              ON DELETE CASCADE);

CREATE TABLE Deck (id SERIAL,
                   creacion DATE NOT NULL DEFAULT CURRENT_DATE,
                   propietario TEXT NOT NULL,
                   PRIMARY KEY (id, propietario),
                   FOREIGN KEY (propietario) REFERENCES Jugador(nif)
                                             ON UPDATE CASCADE
                                             ON DELETE CASCADE);

CREATE TABLE Repetido (cantidad INT NOT NULL DEFAULT 1,
                       carta TEXT NOT NULL,
                       deck SERIAL,
                       propietario TEXT NOT NULL,
                       PRIMARY KEY (carta, deck, propietario),
                       FOREIGN KEY (carta) REFERENCES Carta(codigo)
                                                      ON UPDATE CASCADE
                                                      ON DELETE CASCADE,
                       FOREIGN KEY (deck, propietario) REFERENCES Deck(id, propietario)
                                                       ON UPDATE CASCADE
                                                       ON DELETE CASCADE);

CREATE TABLE Transaccion (id SERIAL,
                          carta TEXT NOT NULL,
                          cede TEXT,
                          recibe TEXT,
                          PRIMARY KEY (id),
                          FOREIGN KEY (carta) REFERENCES Carta(codigo)
                                              ON UPDATE CASCADE
                                              ON DELETE CASCADE,
                          FOREIGN KEY (cede) REFERENCES Jugador(nif)
                                             ON UPDATE CASCADE
                                             ON DELETE SET NULL (cede),
                          FOREIGN KEY (recibe) REFERENCES Jugador(nif)
                                               ON UPDATE CASCADE
                                               ON DELETE SET NULL (recibe));

CREATE TABLE Venta (idfactura SERIAL,
                    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
                    vendedor TEXT NOT NULL,
                    cliente TEXT,
                    PRIMARY KEY (idfactura, vendedor),
                    FOREIGN KEY (vendedor) REFERENCES Tienda(nombre)
                                           ON UPDATE CASCADE
                                           ON DELETE CASCADE,
                    FOREIGN KEY (cliente) REFERENCES Jugador(nif)
                                          ON UPDATE CASCADE
                                          ON DELETE SET NULL (cliente));

CREATE TABLE Vendida (cantidad INT NOT NULL DEFAULT 1,
                      carta TEXT NOT NULL,
                      factura SERIAL,
                      vendedor TEXT NOT NULL,
                      PRIMARY KEY (carta, factura),
                      FOREIGN KEY (carta) REFERENCES Carta(codigo)
                                          ON UPDATE CASCADE
                                          ON DELETE CASCADE,
                      FOREIGN KEY (factura, vendedor) REFERENCES Venta(idfactura, vendedor)
                                                      ON UPDATE CASCADE
                                                      ON DELETE CASCADE);

CREATE TABLE Torneo (fecha DATE NOT NULL,
                     ciudad TEXT NOT NULL,
                     provincia TEXT NOT NULL,
                     ganador TEXT,
                     PRIMARY KEY (fecha, ciudad, provincia),
                     FOREIGN KEY (ciudad, provincia) REFERENCES Ciudad(nombre, provincia)
                                                     ON UPDATE CASCADE
                                                     ON DELETE RESTRICT,
                     FOREIGN KEY (ganador) REFERENCES Jugador(nif)
                                                     ON UPDATE CASCADE
                                                     ON DELETE SET NULL (ganador));

CREATE TABLE Participante (jugador TEXT,
                           fecha DATE NOT NULL,
                           ciudad TEXT NOT NULL,
                           provincia TEXT NOT NULL,
                           PRIMARY KEY (jugador, fecha, ciudad, provincia),
                           FOREIGN KEY (jugador) REFERENCES Jugador(nif)
                                                 ON UPDATE CASCADE
                                                 ON DELETE SET NULL (jugador),
                           FOREIGN KEY (fecha, ciudad, provincia) REFERENCES Torneo(fecha, ciudad, provincia)
                                                                  ON UPDATE CASCADE
                                                                  ON DELETE CASCADE);

CREATE TABLE Partida (duelista1 TEXT,
                      duelista2 TEXT,
                      ganador TEXT CHECK (ganador = duelista1 OR ganador = duelista2),
                      deck1 SERIAL,
                      deck2 SERIAL,
                      fecha DATE NOT NULL,
                      ciudad TEXT NOT NULL,
                      provincia TEXT NOT NULL,
                      PRIMARY KEY (duelista1, duelista2, fecha, ciudad, provincia),
                      FOREIGN KEY (duelista1) REFERENCES Jugador(nif)
                                              ON UPDATE CASCADE
                                              ON DELETE SET NULL (duelista1),
                      FOREIGN KEY (duelista2) REFERENCES Jugador(nif)
                                              ON UPDATE CASCADE
                                              ON DELETE SET NULL (duelista2),
                      FOREIGN KEY (deck1) REFERENCES Deck(id)
                                          ON UPDATE CASCADE
                                          ON DELETE CASCADE,
                      FOREIGN KEY (deck2) REFERENCES Deck(id)
                                          ON UPDATE CASCADE
                                          ON DELETE CASCADE,
                      FOREIGN KEY (fecha, ciudad, provincia) REFERENCES Torneo(fecha, ciudad, provincia)
                                                             ON UPDATE CASCADE
                                                             ON DELETE CASCADE,
                      FOREIGN KEY (ganador) REFERENCES Jugador(nif)
                                            ON UPDATE CASCADE
                                            ON DELETE SET NULL (ganador));
