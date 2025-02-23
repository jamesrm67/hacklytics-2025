import { initializeApp } from "firebase/app";
import { getAuth } from "firebase/auth";
import { getFirestore } from "firebase/firestore";

const firebaseConfig = {
    apiKey: "AIzaSyA7Az_oZzSm5xaB2V11Gc4TQ7IyGCsaGfg",
    authDomain: "hacklytics2025-5efcb.firebaseapp.com",
    projectId: "hacklytics2025-5efcb",
    storageBucket: "hacklytics2025-5efcb.firebasestorage.app",
    messagingSenderId: "907450549489",
    appId: "1:907450549489:web:b5423817d6da142d329550"
  };

// Initialize Firebase
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

export { auth };