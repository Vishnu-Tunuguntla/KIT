import React, { useState } from 'react';
import axios from 'axios';
import './ProcessingAndQueriesPage.css';

function ProcessingAndQueriesPage() {
  const [queryResult, setQueryResult] = useState(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const backendHost = process.env.REACT_APP_BACKEND_HOST || "http://localhost:5000";

  const handleQuery = async (endpoint) => {
    try {
      const response = await axios.get(`${backendHost}/api/${endpoint}`);
      setQueryResult(response.data);
      setCurrentIndex(0);
    } catch (error) {
      console.error('Error querying data:', error);
      alert('Error querying data. Please try again.');
    }
  };

  const handleDelete = async (endpoint) => {
    try {
      await axios.delete(`${backendHost}/api/${endpoint}`);
      handleClear()
      alert('Deletion successful!');
    } catch (error) {
      console.error('Error deleting data:', error);
      alert('Error deleting data. Please try again.');
    }
  };

  const handleExecute = async () => {
    try {
      await axios.post('http://127.0.0.1:5000/api/execute');
      alert('Extraction and analysis executed successfully!');
    } catch (error) {
      console.error('Error executing extraction and analysis:', error);
      alert('Error executing extraction and analysis. Please try again.');
    }
  };

  const handleClear = () => {
    setQueryResult(null);
    setCurrentIndex(0);
  };

  const handleNext = () => {
    setCurrentIndex((prevIndex) => (prevIndex + 1) % queryResult.length);
  };

  const handlePrevious = () => {
    setCurrentIndex((prevIndex) => (prevIndex - 1 + queryResult.length) % queryResult.length);
  };

  return (
    <div className="processing-queries-page">
      <div className="page-header">
        <h2>Processing and Queries</h2>
      </div>
      <div className="query-buttons">
        <button onClick={() => handleQuery('query-all-videos')}>Query All Videos</button>
        <button onClick={() => handleQuery('query-unprocessed-videos')}>Query Unprocessed Videos</button>
        <button onClick={() => handleQuery('query-processed-videos')}>Query Processed Videos</button>
        <button onClick={() => handleQuery('query-frames')}>Query Frames</button>
        <button onClick={() => handleDelete('delete-all-videos')}>Delete All Videos</button>
        <button onClick={() => handleDelete('delete-all-frames')}>Delete All Frames</button>
        <button onClick={() => handleDelete('delete-all-data')}>Delete All Data</button>
        <button onClick={handleExecute}>Execute Extraction and Analysis</button>
        <button onClick={handleClear}>Clear</button>
      </div>
      <div className="query-result">
        {queryResult === null ? (
          <p>Click a query button to view data.</p>
        ) : queryResult.length === 0 ? (
          <p>No data available.</p>
        ) : (
          <div>
            <button onClick={handlePrevious}>Previous</button>
            <button onClick={handleNext}>Next</button>
            <div className="media-container">
              {queryResult[currentIndex].startsWith('data:image/') ? (
                <img
                  src={queryResult[currentIndex]}
                  alt="Query Result"
                  onError={(e) => {
                    console.error('Failed to load image:', queryResult[currentIndex]);
                    e.target.onerror = null; // prevents looping
                    e.target.src = 'path/to/default/image.jpg';
                  }}
                />
              ) : (
                <video key={queryResult[currentIndex]} controls width="100%">
                  <source src={queryResult[currentIndex]} type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default ProcessingAndQueriesPage;