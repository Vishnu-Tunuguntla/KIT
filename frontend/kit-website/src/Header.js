import React from 'react';
import { useNavigate } from 'react-router-dom';

function HeaderNav() {
  const navigate = useNavigate();

  return (
    <div className="header-nav">
      <div className="header-title">K.I.T.</div> {/* Placeholder for your app name */}
      <div className="nav-buttons">
        <button onClick={() => navigate('/')}>Home</button>
        <button onClick={() => navigate('/upload-video')}>Upload Video</button>
        <button onClick={() => navigate('/inventory')}>Inventory</button>
      </div>
    </div>
  );
}

export default HeaderNav;
