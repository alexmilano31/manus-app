import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import ProtectedRoute from './components/ProtectedRoute';
import Dashboard from './components/Dashboard';
import Login from './components/Login';
import Register from './components/Register';
import { authService } from './services/api';

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          {/* Routes publiques */}
          <Route path="/login" element={<Login />} />
          <Route path="/register" element={<Register />} />
          
          {/* Routes protégées */}
          <Route path="/dashboard" element={
            <ProtectedRoute>
              <Dashboard />
            </ProtectedRoute>
          } />
          
          {/* Redirection par défaut */}
          <Route path="/" element={
            authService.isAuthenticated() 
              ? <Navigate to="/dashboard" replace /> 
              : <Navigate to="/login" replace />
          } />
        </Routes>
      </div>
    </Router>
  );
}

export default App;