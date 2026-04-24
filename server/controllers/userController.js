import User from '../models/User.js';
import Question from '../models/Question.js';
import Answer from '../models/Answer.js';

export const getUserProfile = async (req, res) => {
  try {
    const user = await User.findById(req.params.id)
      .select('-password');
    if (!user) {
      return res.status(404).json({ message: 'User not found' });
    }
    res.json(user);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

export const getUserQuestions = async (req, res) => {
  try {
    const questions = await Question.find({ author: req.params.id })
      .populate('author', 'name')
      .sort('-createdAt');
    res.json(questions);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

export const getUserAnswers = async (req, res) => {
  try {
    const answers = await Answer.find({ author: req.params.id })
      .populate('questionId', 'title')
      .sort('-createdAt');
    res.json(answers);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
