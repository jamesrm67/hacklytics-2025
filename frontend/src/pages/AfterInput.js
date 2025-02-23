import React, { useState } from 'react';
import './AfterInput.css';

function AfterInput({ analysisData }) {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [updatedDreamText, setUpdatedDreamText] = useState('');
    const [newAnalysisData, setNewAnalysisData] = useState(analysisData);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
function AfterInput() {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [interpretation, setInterpretation] = useState("");
  const [dreamText, setDreamText] = useState("");

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
            },
            body: JSON.stringify({ dream: updatedDreamText || newAnalysisData.originalDream }), //Use updated text, or original if empty.
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