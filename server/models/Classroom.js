import mongoose from 'mongoose';

const classroomSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true
  },
  code: {
    type: String,
    required: true,
    unique: true
  },
  teacher: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User',
    required: true
  },
  students: [{
    type: mongoose.Schema.Types.ObjectId,
    ref: 'User'
  }],
  subject: String,
  description: String,
  createdAt: {
    type: Date,
    default: Date.now
  }
});

export default mongoose.model('Classroom', classroomSchema);
