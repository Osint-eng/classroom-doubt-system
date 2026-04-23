import Answer from '../models/Answer.js';
import Question from '../models/Question.js';
import Notification from '../models/Notification.js';
import User from '../models/User.js';

export const postAnswer = async (req, res) => {
  try {
    const { body } = req.body;
    const question = await Question.findById(req.params.id);
    
    if (!question) {
      return res.status(404).json({ message: 'Question not found' });
    }
    
    const answer = await Answer.create({
      body,
      author: req.user.id,
      questionId: question._id
    });
    
    question.answers.push(answer._id);
    await question.save();
    
    const populatedAnswer = await answer.populate('author', 'name reputation');
    
    // Create notification for question author
    if (question.author.toString() !== req.user.id) {
      await Notification.create({
        userId: question.author,
        type: 'new_answer',
        message: `${req.user.name} answered your question: ${question.title}`,
        link: `/question/${question._id}`
      });
      
      req.io.to(`user_${question.author}`).emit('new_answer', {
        questionId: question._id,
        answer: populatedAnswer
      });
    }
    
    res.status(201).json(populatedAnswer);
  } catch (error) {
    res.status(400).json({ message: error.message });
  }
};

export const acceptAnswer = async (req, res) => {
  try {
    const answer = await Answer.findById(req.params.aid);
    const question = await Question.findById(req.params.id);
    
    if (question.author.toString() !== req.user.id && req.user.role !== 'teacher') {
      return res.status(403).json({ message: 'Only author or teacher can accept answers' });
    }
    
    // Mark all answers as not accepted
    await Answer.updateMany(
      { questionId: question._id },
      { isAccepted: false }
    );
    
    answer.isAccepted = true;
    await answer.save();
    
    // Update question status
    question.status = 'solved';
    question.solvedAnswerId = answer._id;
    await question.save();
    
    // Update reputation
    const answerAuthor = await User.findById(answer.author);
    answerAuthor.reputation += 10;
    await answerAuthor.save();
    
    // Award badge for first accepted answer
    const acceptedAnswers = await Answer.countDocuments({
      author: answer.author,
      isAccepted: true
    });
    
    if (acceptedAnswers === 1) {
      answerAuthor.badges.push({ name: 'First Accepted Answer', earnedAt: new Date() });
      await answerAuthor.save();
    }
    
    // Create notification
    await Notification.create({
      userId: answer.author,
      type: 'answer_accepted',
      message: `Your answer was accepted for: ${question.title}`,
      link: `/question/${question._id}`
    });
    
    req.io.to(`user_${answer.author}`).emit('answer_accepted', {
      questionId: question._id,
      answerId: answer._id
    });
    
    res.json(answer);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
