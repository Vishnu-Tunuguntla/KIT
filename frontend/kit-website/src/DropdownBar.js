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
    navigate('/');
    setIsOpen(false);
    setIsVisible(false);
  };

  const navigateToProcessingAndQueries = () => {
    navigate('/processing-and-queries');
    setIsOpen(false);
    setIsVisible(false);
  };

  const navigateToInventory = () => {
    navigate('/inventory');
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
                <button onClick={navigateToHome}>Home</button>
              </li>
              <li>
                <button onClick={navigateToUploadVideo}>Upload Video</button>
              </li>
              <li>
                <button onClick={navigateToProcessingAndQueries}>Processing and Queries</button>
              </li>
              <li>
                <button onClick={navigateToInventory}>Inventory</button>
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