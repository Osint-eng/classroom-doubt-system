import mongoose from 'mongoose';

const questionSchema = new mongoose.Schema({
  title: {
    type: String,
    required: true,
    trim: true
  },
  body: {
    type: String,
    required: true
  },
  tags: [{
    type: String,
    trim: true
  }],
  author: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  votes: {
    type: Number,
    default: 0
  },
  answers: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Answer'
  }],
  status: {
    type: String,
    enum: ['open', 'solved'],
    default: 'open'
  },
  views: {
    type: Number,
    default: 0
  },
  classroomId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Classroom',
    required: true
  },
  solvedAnswerId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Answer'
  },
  createdAt: {
    type: Date,
    default: Date.now
  },
  updatedAt: Date
});

questionSchema.index({ title: 'text', body: 'text' });

export default mongoose.model('Question', questionSchema);
