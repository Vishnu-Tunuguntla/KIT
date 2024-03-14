import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function DropdownBar() {
  const [isOpen, setIsOpen] = useState(false);
  const [isVisible, setIsVisible] = useState(false);
  const navigate = useNavigate();

  const navigateToUploadVideo = () => {
    navigate('/upload-video');
    setIsOpen(false);
    setIsVisible(false);
  };

  const navigateToHome = () => {
    navigate('/'); // Navigate to the home page
    setIsOpen(false);
    setIsVisible(false);
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
                <button onClick={navigateToHome}>Home</button> {/* Add navigation to home page */}
              </li>
              <li>
                <button onClick={navigateToUploadVideo}>Upload Video</button>
              </li>
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