import React, { useState } from 'react';
import { useNavigate } from 'react-router';
import './Login.css';

function Register() {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
  });

  const [error, setError] = useState(null);
  const [success, setSuccess] = useState(null);
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError(null); // Clear previous errors
    setSuccess(null);

    try {
      const response = await fetch('http://127.0.0.1:5000/register', { // Your Flask backend URL
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(formData),
      });

      const data = await response.json();

      if (response.ok) {
        setSuccess(data.message);
        // Optionally redirect or clear form after successful registration
        setFormData({ name: '', email: '', password: '' }); // Clear the form
        navigate('/login');
      } else {
        setError(data.error);  // Display error from the backend
      }
    } catch (err) {
      setError('An error occurred during registration.'); // Network or other errors
      console.error("Registration error:", err);
    }
  };

  return (
    <div className="login-container">
      <div className="login-box">
        {/* Logo */}
        <img src="/logodc.png" alt="Logo" className="login-logo" />
        <h1 className="login-title">Register</h1>
        {error && <p className="error-message">{error}</p>}
        {success && <p className="success-message">{success}</p>}
        <form onSubmit={handleSubmit} className="login-form">
          <input 
            type="text" 
            name="name" 
            placeholder="Name" 
            value={formData.name} 
            onChange={handleChange} 
            required 
            className="login-input"
          />
          <input 
            type="email" 
            name="email" 
            placeholder="Email" 
            value={formData.email} 
            onChange={handleChange} 
            required 
            className="login-input"
          />
          <input 
            type="password" 
            name="password" 
            placeholder="Password" 
            value={formData.password} 
            onChange={handleChange} 
            required 
            className="login-input"
          />
          <button type="submit" className="login-button">Register</button>
        </form>
      </div>
    </div>
  );
}

export default Register;