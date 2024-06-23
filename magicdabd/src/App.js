import { Route, BrowserRouter as Router, Routes } from "react-router-dom";
import React, { useEffect, useState } from "react";
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
    }
    fetchData();
  }, []);

  return (
    <div className="App">
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
    </div>
  );
}

export default App;
