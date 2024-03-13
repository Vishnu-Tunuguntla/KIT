import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom'; // Import useNavigate

function DropdownBar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const navigate = useNavigate(); // Use the useNavigate hook

  const navigateToUploadVideo = () => {
    navigate('/upload-video'); // Use navigate instead of history.push
    setIsOpen(false); // Close the dropdown menu
    setIsVisible(false); // Hide the dropdown bar
  };

  return (
    <>
      {isVisible && (
        <div className={`dropdown-bar ${isVisible ? 'visible' : ''}`}>
          <button className="dropdown-toggle" onClick={() => {
            setIsOpen(false);
            setIsVisible(false);
          }}>
            {isOpen ? 'Close Menu' : 'Menu'}
          </button>
          {isOpen && (
            <ul className="dropdown-menu">
              <li>
                <button onClick={navigateToUploadVideo}>Upload Video</button>
              </li>
              {/* Add more dropdown menu items as needed */}
            </ul>
          )}
        </div>
      )}
      {!isVisible && <button className="toggle-button" onClick={() => {
        setIsVisible(true);
        setIsOpen(true);
        }}>Open Menu</button>}
    </>
  );
}

export default DropdownBar;
