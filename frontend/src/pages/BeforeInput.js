import React, { useState } from 'react';
import AfterInput from './AfterInput';
import './BeforeInput.css';

function BeforeInput() {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [dreamText, setDreamText] = useState('');
    const [analysisData, setAnalysisData] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const toggleSidebar = () => {
        setSidebarOpen(!sidebarOpen);
    };

    const handleGenerateDream = () => {
        setLoading(true);
        setError(null);
        fetch('/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ dream: dreamText }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            setAnalysisData(data);
            setLoading(false);
        })
        .catch(err => {
            setError(err.message);
            setLoading(false);
        });
    };

    if (analysisData) {
        return <AfterInput analysisData={analysisData} />;
    }

    return (
        <div className="before-input-container">
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
                <div className="dream-input-box">
                    <textarea
                        placeholder="Please enter your dream..."
                        className="dream-input"
                        value={dreamText}
                        onChange={(e) => setDreamText(e.target.value)}
                    />
                    <button className="dream-button" onClick={handleGenerateDream} disabled={loading}>
                        {loading ? 'Generating...' : 'Generate Dream'}
                    </button>
                    {error && <p className="error-message">{error}</p>}
                </div>
            </div>
        </div>
    );
}

export default BeforeInput;