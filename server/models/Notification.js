import mongoose from 'mongoose';

const notificationSchema = new mongoose.Schema({
  userId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  type: {
    type: String,
    enum: ['new_answer', 'answer_accepted', 'new_upvote', 'new_question'],
    required: true
  },
  message: String,
  isRead: {
    type: Boolean,
    default: false
  },
  link: String,
  createdAt: {
    type: Date,
    default: Date.now
  }
});

export default mongoose.model('Notification', notificationSchema);
