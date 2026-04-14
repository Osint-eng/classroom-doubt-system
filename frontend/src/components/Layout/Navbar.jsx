import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <nav className="bg-white shadow-lg">
      <div className="container mx-auto px-4">
        <div className="flex justify-between items-center h-16">
          <Link to="/" className="font-bold text-xl text-indigo-600">
            Classroom Doubt System
          </Link>
          <div className="flex items-center space-x-4">
            <Link to="/" className="text-gray-700 hover:text-indigo-600">
              Questions
            </Link>
            {user && user.role === 'student' && (
              <Link to="/ask" className="bg-indigo-600 text-white px-4 py-2 rounded-lg">
                Ask Question
              </Link>
            )}
            {user && (
              <Link to="/dashboard" className="text-gray-700 hover:text-indigo-600">
                Dashboard
              </Link>
            )}
            {user ? (
              <>
                <span className="text-gray-600">
                  {user.name} ({user.role})
                </span>
                <button onClick={handleLogout} className="text-red-600">
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-gray-700">
                  Login
                </Link>
                <Link to="/register" className="bg-indigo-600 text-white px-4 py-2 rounded-lg">
                  Register
                </Link>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
