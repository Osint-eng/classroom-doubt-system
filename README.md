# Classroom Doubt Management System

A Stack Overflow-inspired platform for classroom doubt resolution with real-time notifications, reputation system, and role-based access control (Students & Teachers).

## 🚀 Features

- **Role-based System**: Students ask questions, Teachers moderate and accept answers
- **Real-time Notifications**: Instant alerts when questions get answered using Socket.io
- **Reputation & Badges**: Gamification system encouraging quality contributions
- **Rich Text Editor**: Support for code blocks with syntax highlighting and images
- **Voting System**: Upvote/downvote questions and answers
- **Tag System**: Organize questions by subjects/topics
- **Search & Filters**: Full-text search with filtering by unanswered/solved
- **Classroom Management**: Teachers create classrooms, students join via invite code
- **Dark Mode**: Toggle between light and dark themes
- **Responsive Design**: Mobile-friendly layout

## 🛠️ Tech Stack

### Frontend
- React 18 with Vite
- Tailwind CSS for styling
- React Router v6 for navigation
- TanStack React Query for data fetching
- Socket.io-client for real-time features
- TipTap for rich text editing
- Axios for API calls

### Backend
- Node.js with Express.js
- MongoDB with Mongoose ODM
- JWT for authentication
- Socket.io for real-time communication
- Cloudinary for image uploads
- bcrypt for password hashing

## 📋 Prerequisites

- Node.js (v16 or higher)
- MongoDB (local or Atlas)
- npm or yarn package manager

## 🔧 Installation

### 1. Clone the repository
```bash
git clone <your-repo-url>
cd classroom-doubt-system
