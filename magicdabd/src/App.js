import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import React, { useEffect, useState } from "react";
import NewTorneo from './pages/NewTorneo.js';
import ViewTorneo from './pages/ViewTorneo.js';
import logo from './logo.svg';
import './App.css';

const APIUrl = "http://127.0.0.1:8000";

function App() {
  const [jugadores, setJugadores] = useState([]);
  useEffect(() => {
    async function fetchData() {
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
    }
    fetchData();
  }, []);

  return (
    <Router>
      <div className="App">
          <main className="main-content">
            <Routes>
              <Route path='/' element={<NewTorneo />} />
              <Route path="/new" element={<NewTorneo />} />
              <Route path="/view" element={<ViewTorneo />} />
            </Routes>
            <header className="App-header">
              <img src={logo} className="App-logo" alt="logo" />
              <p>
                Edit <code>src/App.js</code> and save to reload.
              </p>
              <a
                className="App-link"
                href="https://reactjs.org"
                target="_blank"
                rel="noopener noreferrer"
                >
                Learn React
              </a>
            </header>
        </main>
      </div>
    </Router>
  );
}

export default App;
