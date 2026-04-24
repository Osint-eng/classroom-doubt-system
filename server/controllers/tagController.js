import Question from '../models/Question.js';

export const getTags = async (req, res) => {
  try {
    const tags = await Question.aggregate([
      { $unwind: '$tags' },
      { $group: { _id: '$tags', count: { $sum: 1 } } },
      { $sort: { count: -1 } }
    ]);
    res.json(tags);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};

export const getQuestionsByTag = async (req, res) => {
  try {
    const { name } = req.params;
    const questions = await Question.find({ tags: name })
      .populate('author', 'name reputation')
      .sort('-createdAt');
    res.json(questions);
  } catch (error) {
    res.status(500).json({ message: error.message });
  }
};
