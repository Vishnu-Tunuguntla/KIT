import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import DropdownBar from './DropdownBar';
import './DropdownBar.css';
import './App.css';
import UploadVideoPage from './UploadVideoPage';
import HomePage from './HomePage'; // Import the HomePage component

function App() {
  return (
    <Router>
      <div className="App">
        <DropdownBar />
        <Routes>
          <Route path="/" element={<HomePage />} /> {/* Add route for the home page */}
          <Route path="/upload-video" element={<UploadVideoPage />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;