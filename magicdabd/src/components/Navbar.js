import { useEffect, useState } from "react";
import { Container, Header, Slider, Nav, Navbar } from 'rsuite';
import { Drawer, ButtonToolbar, Button } from 'rsuite';
import { Form, DatePicker, Cascader, Panel } from 'rsuite';

import { useLocation } from 'react-router-dom'
import './container.css';
import 'rsuite/dist/rsuite.css';

const APIUrl = "http://127.0.0.1:8000";
const labels = ['1', '2', '3', '4', '5', '6'];
let partidas = []

const CustomNavbar = ({ active, onSelect, ...props }) => {
  const [factor, setFactor] = useState(1);
  const [openConfig, setOpenConfig] = useState(false);
  const [tree, setTree] = useState(null)
  const [cascader, setCascader] = useState(null);
  const [fecha, setFecha] = useState(null);

  const handleFactorInput = (value) => {
    if (value < 1) {
      setFactor(1);
    }
    else setFactor(value)
    localStorage.setItem('factor', factor);
  }

  async function fetchTorneos() {
    console.log(cascader)
    console.log(fecha)
    let month = fecha.getMonth()+1
    if (month < 10)
      month = '0'+String(month)
    const date = fecha.getFullYear()+'-'+month+'-'+fecha.getDate()
    const response = await fetch(`${APIUrl}/partidas?` + new URLSearchParams({
      fecha: date,
      ciudad: cascader['ciudad'],
      provincia: cascader['provincia']
    }), {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      },
      mode: 'cors'
    })
    partidas = await response.json()
  }

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch(`${APIUrl}/ciudades`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          mode: 'cors'
        })
        const data = await response.json()
        console.log(`Ciudades obtenidos: ${data.length}`)
        // ciudades = data
        let tree = []
        for (const provincia of data) {
          let children = []
          for (const ciudad of provincia['ciudades']) {
            children.push({label: ciudad, value: {provincia: provincia['provincia'], ciudad: ciudad}})
          }
          tree.push({label: provincia['provincia'], value: provincia['provincia'], children: children})
          setTree(tree)
        }
        console.log(tree)
      } catch (e) {
        console.error(e)
      }
    }
    fetchData();
  }, []);

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
          <div className="button-config">
            <ButtonToolbar>
              <Button onClick={() => setOpenConfig(true)}>
                Configuraciones
              </Button>
            </ButtonToolbar>
          </div>
          <Drawer open={openConfig} onClose={() => setOpenConfig(false)}>
            <Drawer.Header>
              <Drawer.Title>Configuración</Drawer.Title>
              <Drawer.Actions>
                <Button onClick={() => setOpenConfig(false)}>Cancelar</Button>
                <Button onClick={() => {setOpenConfig(false); fetchTorneos()}}appearance="primary">
                  Confirmar
                </Button>
              </Drawer.Actions>
            </Drawer.Header>
            {useLocation().pathname == "/" && (
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
            </Drawer.Body> )}
            {useLocation().pathname == "/view" && (
              <Drawer.Body>
                <Panel>
                  <Form>
                    <Form.Group controlId="datePicker">
                      <Form.ControlLabel>Fecha:</Form.ControlLabel>
                      <Form.Control name="datePicker" accepter={DatePicker}
                                    onChange={(date) => setFecha(date)} />
                    </Form.Group>

                    <Form.Group controlId="cascader">
                      <Form.ControlLabel>Provincia/Ciudad:</Form.ControlLabel>
                      <Form.Control name="cascader" accepter={Cascader} 
                                    data={tree} columnWidth={200}
                                    onChange={(value, event) => setCascader(value)} />
                    </Form.Group>
                  </Form>
                </Panel>
              </Drawer.Body>
            )}
          </Drawer>
        </Navbar>
      </Header>
    </Container>
    </div>
  );
};

export { partidas };
export default CustomNavbar;
