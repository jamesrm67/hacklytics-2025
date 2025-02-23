import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
    apiKey: "AIzaSyBEZvPUjd8Yd59OzUEL7R0hhCAfeaUzkV4",
    authDomain: "hacklytics-c838e.firebaseapp.com",
    projectId: "hacklytics-c838e",
    storageBucket: "hacklytics-c838e.firebasestorage.app",
    messagingSenderId: "1017415322065",
    appId: "1:1017415322065:web:58e70801b97e350f3af8f0",
    measurementId: "G-LDFLY7EBEZ"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { auth };