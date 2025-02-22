import * as React from 'react';

import './App.css';
import Chatbot from './Chatbot';

function App() {
  return (
    <div>
      <header className="app-header">
        <h1>Chatbot UI</h1>
      </header>
      <main>
        <Chatbot />
      </main>
    </div>
  );
}

export default App;
