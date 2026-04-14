import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Toaster } from 'react-hot-toast';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Layout/Navbar';
import Login from './components/Auth/Login';
import Register from './components/Auth/Register';
import QuestionList from './components/Questions/QuestionList';
import QuestionDetail from './components/Questions/QuestionDetail';
import AskQuestion from './components/Questions/AskQuestion';
import StudentDashboard from './components/Dashboard/StudentDashboard';
import TeacherDashboard from './components/Dashboard/TeacherDashboard';

const PrivateRoute = ({ children, allowedRoles }) => {
  const { user } = useAuth();
  if (!user) return <Navigate to="/login" />;
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/" />;
  }
  return children;
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main className="container mx-auto px-4 py-8 max-w-7xl">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/register" element={<Register />} />
              <Route path="/" element={<QuestionList />} />
              <Route path="/questions/:id" element={<QuestionDetail />} />
              <Route
                path="/ask"
                element={
                  <PrivateRoute allowedRoles={['student']}>
                    <AskQuestion />
                  </PrivateRoute>
                }
              />
              <Route
                path="/dashboard"
                element={
                  <PrivateRoute>
                    <StudentDashboard />
                  </PrivateRoute>
                }
              />
            </Routes>
          </main>
        </div>
        <Toaster position="top-right" />
      </AuthProvider>
    </Router>
  );
}

export default App;
