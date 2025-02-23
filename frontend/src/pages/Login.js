import { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import { useNavigate } from 'react-router-dom';
import './Login.css'; 
import { auth } from '../firebase';


function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    const navigate = useNavigate();

    const [success, setSuccess] = useState("");
    const [error, setError] = useState("");

    async function handleLogin(e) {
        e.preventDefault();
        setError(null); // Clear previous errors
        setSuccess(null);

        try {
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            const token = await user.getIdToken();

            const response = await fetch("http://127.0.0.1:5000/login", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(token),
                credentials: 'include'
            });

            const data = await response.json();
            
            if (response.ok) {
                setSuccess(data.message)
                alert("Login successful!");
                navigate('/home');
            } else {
                setError(data.error);
            }
        } catch (error) {
            console.error(error);
            setError("Network error"); // Network or other errors
            alert("Login failed!");
        }
    }

    return (
        <div className="login-container">
            <div className="login-box">
                <img src="/logodc.png" alt="Logo" className="login-logo" />
                <h1 className="login-title">Log In</h1>
                {error && <p className="error-message">{error}</p>}
                {success && <p className="success-message">{success}</p>}
                <form onSubmit={handleLogin} className="login-form">
                    <input 
                        type="email" 
                        value={email} 
                        onChange={(e) => setEmail(e.target.value)} 
                        placeholder="Email" 
                        required 
                        className="login-input"
                    />
                    <input 
                        type="password" 
                        value={password} 
                        onChange={(e) => setPassword(e.target.value)} 
                        placeholder="Password" 
                        required 
                        className="login-input"
                    />
                    <button type="submit" className="login-button">Login</button>
                </form>
            </div>
        </div>
    );
};

export default Login;
