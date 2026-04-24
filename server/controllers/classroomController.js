import Classroom from '../models/Classroom.js';
import User from '../models/User.js';
import crypto from 'crypto';

const generateClassroomCode = () => {
  return crypto.randomBytes(4).toString('hex').toUpperCase();
};

export const createClassroom = async (req, res) => {
  try {
    const { name, subject, description } = req.body;
    const code = generateClassroomCode();
    
    const classroom = await Classroom.create({
      name,
      code,
      teacher: req.user.id,
      subject,
      description
    });
    
    // Update user's classroom
    req.user.classroomId = classroom._id;
    await req.user.save();
    
    res.status(201).json(classroom);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

export const joinClassroom = async (req, res) => {
  try {
    const { code } = req.body;
    const classroom = await Classroom.findOne({ code });
    
    if (!classroom) {
      return res.status(404).json({ message: 'Invalid classroom code' });
    }
    
    if (!classroom.students.includes(req.user.id)) {
      classroom.students.push(req.user.id);
      await classroom.save();
    }
    
    req.user.classroomId = classroom._id;
    await req.user.save();
    
    res.json({ message: 'Joined classroom successfully', classroom });
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

export const getClassroomDetails = async (req, res) => {
  try {
    const classroom = await Classroom.findById(req.params.id)
      .populate('teacher', 'name email')
      .populate('students', 'name email');
    
    if (!classroom) {
      return res.status(404).json({ message: 'Classroom not found' });
    }
    
    res.json(classroom);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
