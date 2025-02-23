import { useState } from 'react';
import { signInWithEmailAndPassword } from 'firebase/auth';
import axios from 'axios';
import { auth } from '../firebase';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');

    async function handleLogin(e) {
        e.preventDefault();

        try {
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            const token = await user.getIdToken();


            if (response.status === 200) {
                alert("Login successful!");
                window.location.href = '/dashboard';
            }
        } catch (error) {
            console.error(error);
            alert("Login failed!");
        }
    }

    return (
        <div>
            <h1>Login</h1>
            <form onSubmit={handleLogin}>
                <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
                <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Password" required />
                <button type="submit">Login</button>
            </form>
        </div>
    );
};

export default Login;
