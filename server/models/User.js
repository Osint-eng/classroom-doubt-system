import mongoose from 'mongoose';
import bcrypt from 'bcryptjs';

const userSchema = new mongoose.Schema({
  name: {
    type: String,
    required: true,
    trim: true
  },
  email: {
    type: String,
    required: true,
    unique: true,
    lowercase: true
  },
  password: {
    type: String,
    required: true
  },
  role: {
    type: String,
    enum: ['student', 'teacher'],
    default: 'student'
  },
  reputation: {
    type: Number,
    default: 0
  },
  badges: [{
    name: String,
    earnedAt: Date
  }],
  classroomId: {
    type: mongoose.Schema.Types.ObjectId,
    ref: 'Classroom'
  },
  avatar: String,
  createdAt: {
    type: Date,
    default: Date.now
  }
});

userSchema.pre('save', async function(next) {
  if (!this.isModified('password')) return next();
  this.password = await bcrypt.hash(this.password, 10);
  next();
});

userSchema.methods.comparePassword = async function(password) {
  return await bcrypt.compare(password, this.password);
};

export default mongoose.model('User', userSchema);
