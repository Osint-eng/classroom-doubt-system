import jwt from 'jsonwebtoken';
import User from '../models/User.js';

export const protect = async (req, res, next) => {
  try {
    let token;
    
    if (req.headers.authorization?.startsWith('Bearer')) {
      token = req.headers.authorization.split(' ')[1];
    }
    
    if (!token) {
      return res.status(401).json({ message: 'Not authorized' });
    }
    
    const decoded = jwt.verify(token, process.env.JWT_SECRET);
    req.user = await User.findById(decoded.id).select('-password');
    next();
  } catch (error) {
    res.status(401).json({ message: 'Not authorized' });
  }
};

export const isTeacher = (req, res, next) => {
  if (req.user.role !== 'teacher') {
    return res.status(403).json({ message: 'Access denied. Teachers only.' });
  }
  next();
};

export const isOwner = (Model) => async (req, res, next) => {
  const item = await Model.findById(req.params.id);
  if (!item) {
    return res.status(404).json({ message: 'Item not found' });
  }
  
  if (item.author.toString() !== req.user.id && req.user.role !== 'teacher') {
    return res.status(403).json({ message: 'Not authorized to modify this resource' });
  }
  next();
};
