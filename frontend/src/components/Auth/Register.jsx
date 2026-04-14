import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Register = () => {
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    role: 'student'
  });
  const [loading, setLoading] = useState(false);
  const { register } = useAuth();
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    const result = await register(formData);
    if (result.success) navigate('/');
    setLoading(false);
  };

  return (
    <div className="max-w-md mx-auto bg-white rounded-lg shadow p-8">
      <h2 className="text-2xl font-bold mb-6 text-center">Register</h2>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Name"
          className="w-full p-2 border rounded mb-4"
          value={formData.name}
          onChange={(e) => setFormData({ ...formData, name: e.target.value })}
          required
        />
        <input
          type="email"
          placeholder="Email"
          className="w-full p-2 border rounded mb-4"
          value={formData.email}
          onChange={(e) => setFormData({ ...formData, email: e.target.value })}
          required
        />
        <input
          type="password"
          placeholder="Password"
          className="w-full p-2 border rounded mb-4"
          value={formData.password}
          onChange={(e) => setFormData({ ...formData, password: e.target.value })}
          required
        />
        <select
          className="w-full p-2 border rounded mb-4"
          value={formData.role}
          onChange={(e) => setFormData({ ...formData, role: e.target.value })}
        >
          <option value="student">Student</option>
          <option value="teacher">Teacher</option>
        </select>
        <button
          type="submit"
          disabled={loading}
          className="w-full bg-indigo-600 text-white p-2 rounded"
        >
          {loading ? 'Loading...' : 'Register'}
        </button>
      </form>
      <p className="mt-4 text-center">
        Already have an account? <Link to="/login" className="text-indigo-600">Login</Link>
      </p>
    </div>
  );
};

export default Register;
