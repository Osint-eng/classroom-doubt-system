import Question from '../models/Question.js';
import Answer from '../models/Answer.js';
import User from '../models/User.js';
import Notification from '../models/Notification.js';

export const voteQuestion = async (req, res) => {
  try {
    const { id } = req.params;
    const { vote } = req.body; // 'up' or 'down'
    
    const question = await Question.findById(id);
    if (!question) {
      return res.status(404).json({ message: 'Question not found' });
    }
    
    // Update question votes
    if (vote === 'up') {
      question.votes += 1;
      // Update reputation of question author
      await User.findByIdAndUpdate(question.author, { $inc: { reputation: 2 } });
    } else if (vote === 'down') {
      question.votes -= 1;
      await User.findByIdAndUpdate(question.author, { $inc: { reputation: -2 } });
    }
    
    await question.save();
    res.json(question);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

export const voteAnswer = async (req, res) => {
  try {
    const { id } = req.params;
    const { vote } = req.body;
    
    const answer = await Answer.findById(id);
    if (!answer) {
      return res.status(404).json({ message: 'Answer not found' });
    }
    
    if (vote === 'up') {
      answer.votes += 1;
      await User.findByIdAndUpdate(answer.author, { $inc: { reputation: 5 } });
    } else if (vote === 'down') {
      answer.votes -= 1;
      await User.findByIdAndUpdate(answer.author, { $inc: { reputation: -2 } });
    }
    
    await answer.save();
    
    // Notify answer author about upvote
    if (vote === 'up' && answer.author.toString() !== req.user.id) {
      await Notification.create({
        userId: answer.author,
        type: 'new_upvote',
        message: `${req.user.name} upvoted your answer`,
        link: `/question/${answer.questionId}`
      });
      req.io.to(`user_${answer.author}`).emit('new_upvote', { answerId: answer._id });
    }
    
    res.json(answer);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
