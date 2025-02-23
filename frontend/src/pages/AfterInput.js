import React, { useState, useEffect } from 'react';
import { onAuthStateChanged } from 'firebase/auth';
import { auth } from '../firebase';
import './AfterInput.css';

function AfterInput({ analysisData }) {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [updatedDreamText, setUpdatedDreamText] = useState('');
    const [newAnalysisData, setNewAnalysisData] = useState(analysisData);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [idToken, setIdToken] = useState("");

    useEffect(() => {
      const unsubscribe = onAuthStateChanged(auth, async (user) => {
      if (user) {
        // User is signed in, get ID token
        const token = await user.getIdToken();
        setIdToken(token); // Store ID token in state
      } else {
        // User is signed out
        setIdToken(null);
        // Optionally redirect to login page if needed
      }
      });
      return () => unsubscribe(); // Unsubscribe on unmount
    }, [auth]);

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    const handleRegenerateDream = () => {
        setLoading(true);
        setError(null);
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${idToken}}`
            },
            body: JSON.stringify({ dream: updatedDreamText || newAnalysisData.originalDream }), //Use updated text, or original if empty.
            credentials: 'include'
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            setNewAnalysisData(data);
            setLoading(false);
        })
        .catch(err => {
            setError(err.message);
            setLoading(false);
        });
    };

    return (
        <div className="after-input-container">
            <header className="header-bar">
                <button className="burger-menu" onClick={toggleSidebar}>
                    <div className="bar" />
                    <div className="bar" />
                    <div className="bar" />
                </button>
                <img src="/logodc.png" alt="Logo" className="logo-image" />
            </header>
            <nav className="navigation-sidebar" style={{ left: sidebarOpen ? '0' : '-350px' }}>
                <h3 className="sidebar-title">Dream History</h3>
                <ul className="sidebar-menu">
                    {/* Your dream history items */}
                </ul>
            </nav>
            <div className="content-wrapper">
                <div className="left-col">
                    <img
                        src={`data:image/png;base64,${newAnalysisData.image_data}`}
                        alt="Generated Dream"
                        className="dream-image"
                    />

                    <div className="dream-input-box">
                        <input
                            type="text"
                            placeholder="Please update your dream..."
                            className="dream-input"
                            value={updatedDreamText}
                            onChange={(e) => setUpdatedDreamText(e.target.value)}
                        />
                    </div>

                    <button className="dream-button" onClick={handleRegenerateDream} disabled={loading}>
                        {loading ? 'Regenerating...' : 'Regenerate Dream'}
                    </button>
                    {error && <p className="error-message">{error}</p>}
                </div>

                <div className="right-col dream-interpretation-box">
                    <p>{newAnalysisData.analysis}</p>
                </div>
            </div>
        </div>
    );
}

export default AfterInput;