import React, { useState } from 'react';
import './AfterInput.css';

function AfterInput() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="after-input-container">
      {/* Top header with burger (left) and logo (right) */}
      <header className="header-bar">
        <button className="burger-menu" onClick={toggleSidebar}>
          <div className="bar" />
          <div className="bar" />
          <div className="bar" />
        </button>

        <img
          src="/logodc.png"
          alt="Logo"
          className="logo-image"
        />
      </header>

      {/* Navigation Sidebar */}
      <nav
        className="navigation-sidebar"
        style={{ left: sidebarOpen ? '0' : '-350px' }}
      >
        <h3 className="sidebar-title">Dream History</h3>
        <ul className="sidebar-menu">
          <li className="menu-item">02/22/2025 Dream</li>
                    <li className="menu-item">02/21/2025 Dream</li>
                    <li className="menu-item">02/20/2025 Dream</li>
                    <li className="menu-item">02/19/2025 Dream</li>
                    <li className="menu-item">02/18/2025 Dream</li>
                    <li className="menu-item">02/22/2025 Dream</li>
                      <li className="menu-item">02/21/2025 Dream</li>
                      <li className="menu-item">02/20/2025 Dream</li>
                      <li className="menu-item">02/19/2025 Dream</li>
                      <li className="menu-item">02/18/2025 Dream</li>
                      <li className="menu-item">02/22/2025 Dream</li>
                    <li className="menu-item">02/21/2025 Dream</li>
                    <li className="menu-item">02/20/2025 Dream</li>
                    <li className="menu-item">02/19/2025 Dream</li>
                    <li className="menu-item">02/18/2025 Dream</li>
                    <li className="menu-item">02/22/2025 Dream</li>
                              <li className="menu-item">02/21/2025 Dream</li>
                              <li className="menu-item">02/20/2025 Dream</li>
                              <li className="menu-item">02/19/2025 Dream</li>
                              <li className="menu-item">02/18/2025 Dream</li>
        </ul>
      </nav>

      {/* Main content area: Black box on the left; interpretation text on the right */}
      <div className="content-wrapper">
        {/* Left Column: Big black box + Dream Input/Button */}
        <div className="left-col">
          <div className="big-black-box"></div>

          <div className="dream-input-box">
            <input
              type="text"
              placeholder="Please update your dream..."
              className="dream-input"
            />
          </div>

          <button className="dream-button">Regenerate Dream</button>
        </div>

        {/* Right Column: Dream Interpretation */}
        <div className="right-col dream-interpretation-box">
          <p>
            The Dream Interpretation should go here in AfterInput.js.
            You can display a detailed analysis or summary of the dream
            the user entered on the left.
          </p>
        </div>
      </div>
    </div>
  );
}

export default AfterInput;