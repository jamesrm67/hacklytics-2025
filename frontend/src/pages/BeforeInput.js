import React, { useState, useEffect } from 'react';
import { auth } from '../firebase';
import { onAuthStateChanged } from 'firebase/auth';
import AfterInput from './AfterInput';
import './BeforeInput.css';

function BeforeInput() {
    const [sidebarOpen, setSidebarOpen] = useState(false);
    const [dreamText, setDreamText] = useState('');
    const [analysisData, setAnalysisData] = useState(null);
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

    const handleGenerateDream = async () => {
        console.log(idToken)
        setLoading(true);
        setError(null);
        fetch('http://127.0.0.1:5000/analyze', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${idToken}}`,
            },
            body: JSON.stringify({ dream: dreamText }),
        })
        .then(async response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return await response.json();
        })
        .then(data => {
            setAnalysisData(data);
            setLoading(false);
        })
        .catch(err => {
            setError(err.message);
            setLoading(false);
            alert(err.message);
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