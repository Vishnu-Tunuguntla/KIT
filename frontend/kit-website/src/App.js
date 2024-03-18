import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import DropdownBar from './DropdownBar';
import './DropdownBar.css';
import './App.css';
import './InventoryPage.css';
import UploadVideoPage from './UploadVideoPage';
import HomePage from './HomePage';
import ProcessingAndQueriesPage from './ProcessingAndQueriesPage';
import InventoryPage from './InventoryPage';

function App() {
  return (
    <Router>
      <div className="App">
        <DropdownBar />
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/upload-video" element={<UploadVideoPage />} />
          <Route path="/processing-and-queries" element={<ProcessingAndQueriesPage />} />
          <Route path="/inventory" element={<InventoryPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;