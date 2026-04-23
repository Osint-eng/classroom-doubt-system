import express from 'express';
import mongoose from 'mongoose';
import cors from 'cors';
import helmet from 'helmet';
import dotenv from 'dotenv';
import { createServer } from 'http';
import { Server } from 'socket.io';
import authRoutes from './routes/auth.js';
import questionRoutes from './routes/questions.js';
import answerRoutes from './routes/answers.js';
import voteRoutes from './routes/votes.js';
import tagRoutes from './routes/tags.js';
import userRoutes from './routes/users.js';
import classroomRoutes from './routes/classroom.js';
import notificationRoutes from './routes/notifications.js';
import { errorHandler } from './middleware/errorHandler.js';

dotenv.config();

const app = express();
const httpServer = createServer(app);
const io = new Server(httpServer, {
  cors: {
    origin: process.env.FRONTEND_URL,
    credentials: true
  }
});

// Middleware
app.use(helmet());
app.use(cors({ origin: process.env.FRONTEND_URL, credentials: true }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Socket.io middleware
app.use((req, res, next) => {
  req.io = io;
  next();
});

// Routes
app.use('/api/auth', authRoutes);
app.use('/api/questions', questionRoutes);
app.use('/api/questions', answerRoutes);
app.use('/api/votes', voteRoutes);
app.use('/api/tags', tagRoutes);
app.use('/api/users', userRoutes);
app.use('/api/classroom', classroomRoutes);
app.use('/api/notifications', notificationRoutes);

// Error handling
app.use(errorHandler);

// Socket.io connection handling
io.on('connection', (socket) => {
  console.log('New client connected');
  
  socket.on('join classroom', (classroomId) => {
    socket.join(`classroom_${classroomId}`);
  });
  
  socket.on('join user', (userId) => {
    socket.join(`user_${userId}`);
  });
  
  socket.on('disconnect', () => {
    console.log('Client disconnected');
  });
});

// MongoDB connection
mongoose.connect(process.env.MONGODB_URI)
  .then(() => console.log('MongoDB connected'))
  .catch(err => console.error('MongoDB connection error:', err));

const PORT = process.env.PORT || 5000;
httpServer.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
