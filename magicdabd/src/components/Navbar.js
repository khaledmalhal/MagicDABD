import { useEffect, useState } from "react";
import { Container, Header, Slider, Nav, Navbar } from 'rsuite';
import { Drawer, ButtonToolbar, Button } from 'rsuite';
import { useLocation } from 'react-router-dom'
import './container.css';
import 'rsuite/dist/rsuite.css';

const labels = ['1', '2', '3', '4', '5', '6'];

const CustomNavbar = ({ active, onSelect, ...props }) => {
  const [location, setLocation] = useState('');
  const [factor, setFactor] = useState(1);
  const [openConfig, setOpenConfig] = useState(false);

  const handleFactorInput = (value) => {
    if (value < 1) {
      setFactor(1);
    }
    else setFactor(value)
    localStorage.setItem('factor', factor);
  }

  return (
    <div>
    <Container>
      <Header>
        <Navbar appearance="inverse">
          <Navbar.Brand>
            <a style={{ color: "#fff" }}>MagicDABD</a>
          </Navbar.Brand>
          <Nav>
            <Nav.Item href="/">Insertar Torneos</Nav.Item>
            <Nav.Item href="/view">Ver Torneos</Nav.Item>
          </Nav>
          {useLocation().pathname != "/view" && (
            <div className="button-config">
              <ButtonToolbar>
                <Button onClick={() => setOpenConfig(true)}>
                  Configuraciones
                </Button>
              </ButtonToolbar>
            </div>
          )}
          <Drawer open={openConfig} onClose={() => setOpenConfig(false)}>
            <Drawer.Header>
              <Drawer.Title>Configuración</Drawer.Title>
              <Drawer.Actions>
                <Button onClick={() => setOpenConfig(false)}>Cancelar</Button>
                <Button onClick={() => setOpenConfig(false)}appearance="primary">
                  Confirmar
                </Button>
              </Drawer.Actions>
            </Drawer.Header>
            <Drawer.Body>
              <div className="config-tournament min-h-screen">
                <label position="relative">Ajuste el factor de jugadores</label>
                <div style={{ width: 200, marginLeft: 20 }}>
                  <Slider
                    min={0}
                    max={labels.length - 1}
                    value={factor}
                    className="custom-slider"
                    handleStyle={{
                      borderRadius: 15,
                      color: "#fff",
                      fontSize: 24,
                      width: 32,
                      height: 22,
                    }}
                    graduated
                    tooltip={false}
                    handleTitle={labels[factor]}
                    onChange={handleFactorInput}
                  />
                </div>
                <label position="relative">
                  Cantidad de jugadores totales: {Math.pow(4, factor)}
                </label>
              </div>
            </Drawer.Body>
          </Drawer>
        </Navbar>
      </Header>
    </Container>
    </div>
  );
};

export default CustomNavbar;
