import React, { useEffect, useState } from "react";
import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import NewTorneo from './pages/NewTorneo.js';
import ViewTorneo from './pages/ViewTorneo.js';
import CustomNavbar from './components/Navbar.js';
import './App.css';

const APIUrl = "http://127.0.0.1:8000";

function App() {
  const [jugadores, setJugadores] = useState([]);
  const [torneos, setTorneos] = useState([]);
  const [active, setActive] = useState('new');

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch(`${APIUrl}/jugadores`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          mode: 'cors'
        })
        const data = await response.json()
        console.log(data)
        setJugadores(data)
        localStorage.setItem('jugadores', JSON.stringify(jugadores));
      } catch (e) {
        console.error(e)
      }
    }
    fetchData();
  }, []);

  useEffect(() => {
    async function fetchData() {
      try {
        const response = await fetch(`${APIUrl}/torneos`, {
          method: 'GET',
          headers: {
            'Content-Type': 'application/json'
          },
          mode: 'cors'
        })
        const data = await response.json()
        console.log(data)
        setTorneos(data)
        localStorage.setItem('torneos', JSON.stringify(torneos));
      } catch (e) {
        console.error(e)
      }
    }
    fetchData();
  }, []);

  return (
    <Router>
      <div className="App">
        <CustomNavbar></CustomNavbar>
        <main className="main-content min-h-screen min-w-screen">
          <Routes>
            <Route path='/' element={<NewTorneo />} />
            <Route path="/view" element={<ViewTorneo />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
