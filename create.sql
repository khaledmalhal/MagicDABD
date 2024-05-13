CREATE TABLE Carta (codigo TEXT NOT NULL,
		            nombre TEXT NOT NULL,
		            rareza VARCHAR(2) NOT NULL,
		            tipo TEXT NOT NULL,
		            PRIMARY KEY (codigo));

CREATE TABLE Provincia (nombre TEXT NOT NULL,
                        PRIMARY KEY (nombre));

CREATE TABLE Ciudad (nombre TEXT NOT NULL,
                     provincia TEXT NOT NULL,
                     FOREIGN KEY (provincia) REFERENCES Provincia(nombre),
                     PRIMARY KEY (nombre, provincia));

CREATE TABLE Tienda (nombre TEXT NOT NULL,
                     telefono BIGINT NOT NULL,
                     ciudad TEXT NOT NULL,
                     provincia TEXT NOT NULL,
                     PRIMARY KEY (nombre),
                     UNIQUE (telefono),
                     FOREIGN KEY (ciudad, provincia) REFERENCES Ciudad(nombre, provincia));
  
CREATE TABLE Inventario (cantidad INT NOT NULL DEFAULT 1,
                         tienda TEXT NOT NULL,
                         carta TEXT NOT NULL,
                         PRIMARY KEY (tienda, carta),
                         FOREIGN KEY (tienda) REFERENCES Tienda(nombre),
                         FOREIGN KEY (carta) REFERENCES Carta(codigo));

CREATE TABLE Jugador (nif TEXT NOT NULL,
                      nombre TEXT NOT NULL,
                      apellido TEXT NOT NULL,
                      ciudad TEXT NOT NULL,
                      provincia TEXT NOT NULL,
                      PRIMARY KEY (nif),
                      FOREIGN KEY (ciudad, provincia) REFERENCES Ciudad(nombre, provincia));

CREATE TABLE Copia (cantidad INT NOT NULL DEFAULT 1,
                    carta TEXT NOT NULL,
                    propietario TEXT NOT NULL,
                    PRIMARY KEY (carta, propietario),
                    FOREIGN KEY (carta) REFERENCES Carta(codigo),
                    FOREIGN KEY (propietario) REFERENCES Jugador(nif));

CREATE TABLE Deck (id SERIAL,
                   creacion DATE NOT NULL DEFAULT CURRENT_DATE,
                   propietario TEXT NOT NULL,
                   PRIMARY KEY (id, propietario),
                   FOREIGN KEY (propietario) REFERENCES Jugador(nif));

CREATE TABLE Repetido (cantidad INT NOT NULL DEFAULT 1,
                       carta TEXT NOT NULL,
                       deck SERIAL,
                       propietario TEXT NOT NULL,
                       PRIMARY KEY (carta, deck, propietario),
                       FOREIGN KEY (carta) REFERENCES Carta(codigo),
                       FOREIGN KEY (deck, propietario) REFERENCES Deck(id, propietario));

CREATE TABLE Transaccion (id SERIAL,
                          carta TEXT NOT NULL,
                          cede TEXT NOT NULL,
                          recibe TEXT NOT NULL,
                          PRIMARY KEY (id),
                          FOREIGN KEY (carta) REFERENCES Carta(codigo),
                          FOREIGN KEY (cede) REFERENCES Jugador(nif),
                          FOREIGN KEY (recibe) REFERENCES Jugador(nif));

CREATE TABLE Venta (idfactura SERIAL,
                    fecha DATE NOT NULL DEFAULT CURRENT_DATE,
                    vendedor TEXT NOT NULL,
                    cliente TEXT NOT NULL,
                    PRIMARY KEY (idfactura, vendedor),
                    FOREIGN KEY (vendedor) REFERENCES Tienda(nombre),
                    FOREIGN KEY (cliente) REFERENCES Jugador(nif));

CREATE TABLE Vendida (cantidad INT NOT NULL DEFAULT 1,
                      carta TEXT NOT NULL,
                      factura SERIAL,
                      vendedor TEXT NOT NULL,
                      PRIMARY KEY (carta, factura),
                      FOREIGN KEY (carta) REFERENCES Carta(codigo),
                      FOREIGN KEY (factura, vendedor) REFERENCES Venta(idfactura, vendedor));

CREATE TABLE Torneo (fecha DATE NOT NULL,
                     ciudad TEXT NOT NULL,
                     provincia TEXT NOT NULL,
                     ganador TEXT NOT NULL,
                     PRIMARY KEY (fecha, ciudad, provincia),
                     FOREIGN KEY (ciudad, provincia) REFERENCES Ciudad(nombre, provincia),
                     FOREIGN KEY (ganador) REFERENCES Jugador(nif));

CREATE TABLE Participante (jugador TEXT NOT NULL,
                           fecha DATE NOT NULL,
                           ciudad TEXT NOT NULL,
                           provincia TEXT NOT NULL,
                           PRIMARY KEY (jugador, fecha, ciudad, provincia),
                           FOREIGN KEY (jugador) REFERENCES Jugador(nif),
                           FOREIGN KEY (fecha, ciudad, provincia) REFERENCES Torneo(fecha, ciudad, provincia));

CREATE TABLE Partida (duelista1 TEXT NOT NULL,
                      duelista2 TEXT NOT NULL,
                      ganador TEXT NOT NULL CHECK (ganador = duelista1 OR ganador = duelista2),
                      deck1 SERIAL,
                      deck2 SERIAL,
                      fecha DATE NOT NULL,
                      ciudad TEXT NOT NULL,
                      provincia TEXT NOT NULL,
                      PRIMARY KEY (duelista1, duelista2, fecha, ciudad, provincia),
                      FOREIGN KEY (duelista1, deck1) REFERENCES Deck(propietario, id),
                      FOREIGN KEY (duelista2, deck2) REFERENCES Deck(propietario, id),
                      FOREIGN KEY (fecha, ciudad, provincia) REFERENCES Torneo(fecha, ciudad, provincia),
                      FOREIGN KEY (ganador) REFERENCES Jugador(nif));
