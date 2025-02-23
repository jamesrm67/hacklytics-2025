import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import BeforeInput from './pages/BeforeInput';
import AfterInput from './pages/AfterInput';

import './App.css';

function App() {
  return (
    <div className="App">
      <Router>
        <Routes>
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          <Route path="/home" element={<BeforeInput />} />
          <Route path="/processed" element={<AfterInput />} />
        </Routes>
      </Router>
    </div>
  );
}

export default App;
