import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Login = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const result = await login({ email, password });
    if (result.success) navigate('/');
    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow p-8">
      <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="email"
          placeholder="Email"
          className="w-full p-2 border rounded mb-4"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 border rounded mb-4"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 text-white p-2 rounded"
        >
          {loading ? 'Loading...' : 'Login'}
        </button>
      </form>
      <p className="mt-4 text-center">
        New user? <Link to="/register" className="text-indigo-600">Register</Link>
      </p>
    </div>
  );
};

export default Login;
