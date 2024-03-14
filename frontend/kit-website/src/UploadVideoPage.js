import React, { useState, useRef } from 'react';
import axios from 'axios';

function UploadVideoPage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const fileInputRef = useRef(null);

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    const formData = new FormData();
    formData.append('video', selectedFile);

    try {
      const response = await axios.post('http://127.0.0.1:5000/api/upload', formData);
      console.log(response.data.message);
      alert('Video uploaded successfully!');
      // Clear the selected file and reset the file input
      setSelectedFile(null);
      fileInputRef.current.value = null;
    } catch (error) {
      console.error('Error uploading video:', error);

      if (error.response) {
        // Server responded with a status code outside of 2xx range
        let errorMessage = 'Upload failed. ';

        if (error.response.status === 400) {
          errorMessage += 'Bad request. Please check the video file format and size.';
        } else if (error.response.status === 500) {
          errorMessage += 'Internal server error. Please try again later.';
        } else {
          errorMessage += `Server responded with status code ${error.response.status}.`;
        }

        if (error.response.data && error.response.data.error) {
          errorMessage += ` Error details: ${error.response.data.error}`;
        }

        alert(errorMessage);
      } else if (error.request) {
        // The request was made, but no response from the server
        alert('Could not connect to the server. Please check your internet connection and try again.');
      } else {
        // Something else happened during setup or the request
        alert('An unexpected error occurred. Please try again.');
      }
    }
  };

  return (
    <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100vh' }}>
      <input type="file" ref={fileInputRef} onChange={handleFileChange} />
      <button onClick={handleUpload}>Upload Video</button>
    </div>
  );
}

export default UploadVideoPage;