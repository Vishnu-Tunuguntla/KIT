import React, { useState, useRef } from 'react';
import axios from 'axios';
import './UploadVideoPage.css'; // Ensure this path matches the location of your CSS file

function UploadVideoPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const fileInputRef = useRef(null);
  const backendHost = "http://localhost:5000"; //"http://34.233.181.229:5000"; // "http://localhost:5000";

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      setFileName(file.name); // Set the file name for display
    }
  };
  const handleExecute = async () => {
    try {
      await axios.post(`${backendHost}/api/execute`);
      alert('Extraction and analysis executed successfully!');
    } catch (error) {
      console.error('Error executing extraction and analysis:', error);
      alert('Error executing extraction and analysis. Please try again.');
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      alert('Please select a file before uploading.');
      return;
    }

    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      const response = await axios.post(`${backendHost}/api/upload`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log(response.data.message);
      alert('Video uploaded successfully!');

      // Clear the selected file and reset the file input for the next upload
      setSelectedFile(null);
      setFileName('');
      if (fileInputRef.current) {
        fileInputRef.current.value = null;
      }

      // Execute extraction and analysis right after the successful upload
      await handleExecute();
    } catch (error) {
      console.error('Error uploading video:', error);
      // Constructing a user-friendly error message based on the error response
      let errorMessage = 'Upload failed.';
      if (error.response) {
        errorMessage += ` Server responded with status code ${error.response.status}.`;
        if (error.response.data && error.response.data.error) {
          errorMessage += ` Error details: ${error.response.data.error}`;
        }
      } else if (error.request) {
        errorMessage = 'Could not connect to the server. Please check your internet connection and try again.';
      } else {
        errorMessage = 'An unexpected error occurred. Please try again.';
      }
      alert(errorMessage);
    }
  };


  return (
    <div className="page-container">
      <div className="upload-container">
        <div className="file-name">{fileName || 'No file selected'}</div>
        <div className="button-container">
          {/* Hidden file input */}
          <input type="file" ref={fileInputRef} onChange={handleFileChange} className="file-input" style={{ display: 'none' }} />
          {/* Button to trigger file input */}
          <button className="select-button" onClick={() => fileInputRef.current.click()}>Select Video</button>
          {/* Button to upload the selected file */}
          <button onClick={handleUpload} className="upload-button">Upload Video</button>
        </div>
      </div>
    </div>
  );
}

export default UploadVideoPage;