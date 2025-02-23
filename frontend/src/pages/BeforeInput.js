import React, { useState } from 'react';
import './BeforeInput.css'; // Optional if you want to move the styles into a separate CSS file.

function BeforeInput() {
  const [sidebarOpen, setSidebarOpen] = useState(false);

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  return (
    <div className="before-input-container">
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

      {/* Main content area: large textbox + centered button */}
      <div className="content-wrapper">
        <div className="dream-input-box">
          <textarea
            placeholder="Please enter your dream..."
            className="dream-input"
          />
          <button className="dream-button">Generate Dream</button>
        </div>
      </div>
    </div>
  );
}

export default BeforeInput;