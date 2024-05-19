import './App.css';

import React, { useState, useEffect } from 'react';
import axios from 'axios';

function App() {
  const [currentTime, setCurrentTime] = useState('');

  useEffect(() => {
    axios.get('/api/ping/')
      .then(response => {
        setCurrentTime(response.data.timestamp);
      })
      .catch(error => {
        console.error('error: ', error);
      });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <h1>Current Time</h1>
        <p>{currentTime ? `Server time: ${currentTime}` : 'Loading...'}</p>
      </header>
    </div>
  );
}

export default App;
