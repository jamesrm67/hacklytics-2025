import React, { useState } from 'react';
import './AfterInput.css';

function AfterInput() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [interpretation, setInterpretation] = useState("");
  const [dreamText, setDreamText] = useState("");

  const toggleSidebar = () => {
    setSidebarOpen(!sidebarOpen);
  };

  const handleChange = (e) => {
    setDreamText(e.target.value);
  }

  const handleSubmit = async (e) => {
    e.preventDefault()

    try {
      const response = await fetch("http://127.0.0.1:5000/interpret", {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(dreamText)
      });

      const data = await response.json();
      console.log(data.Interpretation);

      if (response.ok) {
        setInterpretation(data.Interpretation);
        alert("Successfully interpretted text");
      } else {
        const errorData = await response.json();
        console.error('Interpretation Failed:', errorData.error);
      }
    } catch (error) {
      console.error("Interpretation error:", error);
    }
  }

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
            <form onSubmit={handleSubmit}>
              <input
                onChange={handleChange}
                type="text"
                placeholder="Please update your dream..."
                className="dream-input"
              />
              <button value="submit" type="submit" className="dream-button">Regenerate Dream</button>
            </form>
          </div>

        </div>

        {/* Right Column: Dream Interpretation */}
        <div className="right-col dream-interpretation-box">
          {interpretation && (
            <div>
              <h3>Interpretation:</h3>
              <p>{interpretation}</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default AfterInput;