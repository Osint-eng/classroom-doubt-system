import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { SocketProvider } from './context/SocketContext';
import PrivateRoute from './components/PrivateRoute';
import AuthPage from './pages/AuthPage';
import HomePage from './pages/HomePage';
import AskQuestionPage from './pages/AskQuestionPage';
import QuestionDetailPage from './pages/QuestionDetailPage';
import TagsPage from './pages/TagsPage';
import LeaderboardPage from './pages/LeaderboardPage';
import ProfilePage from './pages/ProfilePage';
import Layout from './components/Layout';

function App() {
  return (
    <Router>
      <AuthProvider>
        <SocketProvider>
          <Routes>
            <Route path="/auth" element={<AuthPage />} />
            <Route element={<PrivateRoute />}>
              <Route element={<Layout />}>
                <Route path="/" element={<HomePage />} />
                <Route path="/ask" element={<AskQuestionPage />} />
                <Route path="/question/:id" element={<QuestionDetailPage />} />
                <Route path="/tags" element={<TagsPage />} />
                <Route path="/leaderboard" element={<LeaderboardPage />} />
                <Route path="/profile/:id" element={<ProfilePage />} />
              </Route>
            </Route>
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </SocketProvider>
      </AuthProvider>
    </Router>
  );
}

export default App;
