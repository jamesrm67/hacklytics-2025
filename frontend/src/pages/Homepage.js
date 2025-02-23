import React from "react";
import { useNavigate } from "react-router-dom";
import "./Login.css"; // Using the same styles

function Home() {
  const navigate = useNavigate();

  return (
    <div className="home-container">
      <div className="home-box">
        {/* Logo */}
        <img src="/logodc.png" alt="Logo" className="home-logo" />

        {/* Big Title */}
        <h1 className="home-title">Spill Your Dreams</h1>

        {/* Buttons */}
        <div className="home-buttons">
          <button className="home-button" onClick={() => navigate("/register")}>Register</button>
          <button className="home-button" onClick={() => navigate("/login")}>Login</button>
        </div>

        {/* Clickable Arrow */}
        <img 
          src="/arrow.png"
          alt="Go to next page" 
          className="home-arrow" 
          onClick={() => navigate("/home")} 
        />
      </div>
    </div>
  );
}

export default Home;
