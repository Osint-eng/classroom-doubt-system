import Question from '../models/Question.js';
import Notification from '../models/Notification.js';
import User from '../models/User.js';

export const getQuestions = async (req, res) => {
  try {
    const { page = 1, limit = 10, filter, tag, search } = req.query;
    const query = { classroomId: req.user.classroomId };
    
    if (filter === 'unanswered') {
      query.answers = { $size: 0 };
    } else if (filter === 'solved') {
      query.status = 'solved';
    }
    
    if (tag) {
      query.tags = tag;
    }
    
    if (search) {
      query.$text = { $search: search };
    }
    
    const questions = await Question.find(query)
      .populate('author', 'name reputation')
      .sort('-createdAt')
      .limit(limit * 1)
      .skip((page - 1) * limit);
    
    const total = await Question.countDocuments(query);
    
    res.json({
      questions,
      totalPages: Math.ceil(total / limit),
      currentPage: page
    });
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

export const createQuestion = async (req, res) => {
  try {
    const { title, body, tags } = req.body;
    
    const question = await Question.create({
      title,
      body,
      tags,
      author: req.user.id,
      classroomId: req.user.classroomId
    });
    
    const populatedQuestion = await question.populate('author', 'name reputation');
    
    // Award badge for first question
    const userQuestions = await Question.countDocuments({ author: req.user.id });
    if (userQuestions === 1) {
      req.user.badges.push({ name: 'First Question', earnedAt: new Date() });
      await req.user.save();
    }
    
    // Notify classroom members
    req.io.to(`classroom_${req.user.classroomId}`).emit('new_question', {
      question: populatedQuestion,
      classroomId: req.user.classroomId
    });
    
    res.status(201).json(populatedQuestion);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

export const getQuestionById = async (req, res) => {
  try {
    const question = await Question.findById(req.params.id)
      .populate('author', 'name reputation avatar')
      .populate({
        path: 'answers',
        populate: { path: 'author', select: 'name reputation avatar' }
      });
    
    if (!question) {
      return res.status(404).json({ message: 'Question not found' });
    }
    
    // Increment views
    question.views += 1;
    await question.save();
    
    res.json(question);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

export const markAsSolved = async (req, res) => {
  try {
    const question = await Question.findById(req.params.id);
    
    if (question.author.toString() !== req.user.id && req.user.role !== 'teacher') {
      return res.status(403).json({ message: 'Only author or teacher can mark as solved' });
    }
    
    question.status = 'solved';
    question.solvedAnswerId = req.body.answerId;
    await question.save();
    
    res.json(question);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
