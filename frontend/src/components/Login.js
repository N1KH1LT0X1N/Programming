import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:8000/token', 
        new URLSearchParams({
          username: username,
          password: password
        }),
        {
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
          }
        }
      );
      localStorage.setItem('token', response.data.access_token);
      navigate('/dashboard');
    } catch (error) {
      console.error('Login failed', error);
      alert('Login failed!');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Login</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="usernameInput" className="form-label">Username</label>
          <input 
            type="text" 
            className="form-control" 
            id="usernameInput" 
            value={username} 
            onChange={(e) => setUsername(e.target.value)} 
            required 
          />
        </div>
        <div className="mb-3">
          <label htmlFor="passwordInput" className="form-label">Password</label>
          <input 
            type="password" 
            className="form-control" 
            id="passwordInput" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
        </div>
        <button type="submit" className="btn btn-primary">Login</button>
      </form>
      <p className="mt-3">Don't have an account? <a href="/register">Register here</a></p>
    </div>
  );
}

export default Login;
