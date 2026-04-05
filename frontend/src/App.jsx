import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import MainLayout from './layouts/MainLayout';
import Home from './pages/Home';
import Agents from './pages/Agents';
import Zones from './pages/Zones';

import Infrastructure from './pages/Infrastructure';

function App() {
  return (
    <Router>
      <MainLayout>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/agents" element={<Agents />} />
          <Route path="/zones" element={<Zones />} />
          <Route path="/infrastructure" element={<Infrastructure />} />
        </Routes>
      </MainLayout>
    </Router>
  );
}

export default App;
