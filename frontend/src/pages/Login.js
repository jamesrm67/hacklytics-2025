import { useState } from 'react';
import { getAuth, signInWithEmailAndPassword } from 'firebase/auth';
import axios from 'axios';

function Login() {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const auth = getAuth();

    async function handleLogin(e) {
        e.preventDefault();

        try {
            const userCredential = await signInWithEmailAndPassword(auth, email, password);
            const user = userCredential.user;
            const token = await user.getIdToken();

            const response = await axios.post('http://localhost:5000/login', { token });

            if (response.status === 200) {
                alert("Login successful!");
                window.location.href = '/dashboard';
            }
        } catch (error) {
            console.error(error);
            alert("Login failed!");
        }
    }
}

return {
    
}