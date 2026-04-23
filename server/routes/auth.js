import express from 'express';
import jwt from 'jsonwebtoken';
import { body, validationResult } from 'express-validator';
import User from '../models/User.js';
import Classroom from '../models/Classroom.js';
import { protect } from '../middleware/auth.js';

const router = express.Router();

const generateToken = (id) => {
  return jwt.sign({ id }, process.env.JWT_SECRET, { expiresIn: '7d' });
};

router.post('/register', [
  body('email').isEmail().normalizeEmail(),
  body('password').isLength({ min: 6 }),
  body('name').notEmpty().trim()
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }
  
  try {
    const { name, email, password, role, classroomCode } = req.body;
    
    let classroom = null;
    if (classroomCode) {
      classroom = await Classroom.findOne({ code: classroomCode });
      if (!classroom) {
        return res.status(400).json({ message: 'Invalid classroom code' });
      }
    }
    
    const user = await User.create({
      name,
      email,
      password,
      role: role || 'student',
      classroomId: classroom?._id
    });
    
    if (classroom && role !== 'teacher') {
      classroom.students.push(user._id);
      await classroom.save();
    }
    
    const token = generateToken(user._id);
    
    res.status(201).json({
      _id: user._id,
      name: user.name,
      email: user.email,
      role: user.role,
      token,
      classroomId: user.classroomId
    });
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

router.post('/login', async (req, res) => {
  try {
    const { email, password } = req.body;
    const user = await User.findOne({ email });
    
    if (!user || !(await user.comparePassword(password))) {
      return res.status(401).json({ message: 'Invalid credentials' });
    }
    
    const token = generateToken(user._id);
    
    res.json({
      _id: user._id,
      name: user.name,
      email: user.email,
      role: user.role,
      token,
      classroomId: user.classroomId
    });
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
});

export default router;
