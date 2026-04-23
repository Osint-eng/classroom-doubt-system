import React, { useState } from 'react';
import { Outlet, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useSocket } from '../context/SocketContext';
import { FiHome, FiHelpCircle, FiTag, FiAward, FiUser, FiLogOut, FiMoon, FiSun, FiBell } from 'react-icons/fi';
import NotificationsDropdown from './NotificationsDropdown';

export default function Layout() {
  const { user, logout } = useAuth();
  const { unreadCount } = useSocket();
  const navigate = useNavigate();
  const [darkMode, setDarkMode] = useState(localStorage.getItem('darkMode') === 'true');

  const toggleDarkMode = () => {
    setDarkMode(!darkMode);
    localStorage.setItem('darkMode', !darkMode);
    document.documentElement.classList.toggle('dark');
  };

  return (
    <div className={darkMode ? 'dark' : ''}>
      <div className="min-h-screen bg-gray-50 dark:bg-gray-900">
        {/* Header */}
        <header className="bg-white dark:bg-gray-800 shadow-sm fixed top-0 w-full z-50">
          <div className="container mx-auto px-4">
            <div className="flex justify-between items-center h-16">
              <Link to="/" className="text-2xl font-bold text-blue-600 dark:text-blue-400">
                DoubtSolve
              </Link>
              
              <div className="flex items-center space-x-4">
                <button
                  onClick={() => navigate('/ask')}
                  className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition"
                >
                  Ask Question
                </button>
                
                <button onClick={toggleDarkMode} className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                  {darkMode ? <FiSun size={20} /> : <FiMoon size={20} />}
                </button>
                
                <NotificationsDropdown unreadCount={unreadCount} />
                
                <div className="relative group">
                  <button className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700">
                    <img
                      src={user?.avatar || `https://ui-avatars.com/api/?name=${user?.name}`}
                      alt={user?.name}
                      className="w-8 h-8 rounded-full"
                    />
                    <span className="hidden md:inline text-gray-700 dark:text-gray-300">{user?.name}</span>
                  </button>
                  
                  <div className="absolute right-0 mt-2 w-48 bg-white dark:bg-gray-800 rounded-lg shadow-lg hidden group-hover:block">
                    <Link to={`/profile/${user?._id}`} className="block px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700">
                      Profile
                    </Link>
                    <button onClick={logout} className="block w-full text-left px-4 py-2 hover:bg-gray-100 dark:hover:bg-gray-700">
                      Logout
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </header>

        {/* Sidebar and Main Content */}
        <div className="container mx-auto px-4 pt-20">
          <div className="flex gap-6">
            {/* Left Sidebar */}
            <aside className="hidden lg:block w-64">
              <nav className="sticky top-20">
                <Link to="/" className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
                  <FiHome /> <span>Home</span>
                </Link>
                <Link to="/tags" className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
                  <FiTag /> <span>Tags</span>
                </Link>
                <Link to="/leaderboard" className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
                  <FiAward /> <span>Leaderboard</span>
                </Link>
                {user?.role === 'teacher' && (
                  <div className="mt-4 pt-4 border-t border-gray-200 dark:border-gray-700">
                    <p className="text-xs uppercase text-gray-500 dark:text-gray-400 px-3 mb-2">Teacher Tools</p>
                    <Link to="/classroom/manage" className="flex items-center space-x-3 p-3 rounded-lg hover:bg-gray-100">
                      <FiUser /> <span>Manage Classroom</span>
                    </Link>
                  </div>
                )}
              </nav>
            </aside>

            {/* Main Content */}
            <main className="flex-1 min-w-0">
              <Outlet />
            </main>

            {/* Right Sidebar */}
            <aside className="hidden xl:block w-80">
              <div className="sticky top-20">
                <div className="bg-white dark:bg-gray-800 rounded-lg p-4 shadow-sm mb-4">
                  <h3 className="font-semibold mb-3">Your Stats</h3>
                  <div className="space-y-2 text-sm">
                    <p>Reputation: {user?.reputation || 0}</p>
                    <p>Badges: {user?.badges?.length || 0}</p>
                  </div>
                </div>
              </div>
            </aside>
          </div>
        </div>
      </div>
    </div>
  );
}
