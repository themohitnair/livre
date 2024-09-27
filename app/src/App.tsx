import './App.css'

import Register from './Register';
import Login from './Login';

import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import React from 'react';

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/register" element={<Register />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
};


export default App;
