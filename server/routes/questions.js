import express from 'express';
import { protect } from '../middleware/auth.js';
import { getQuestions, createQuestion, getQuestionById, markAsSolved } from '../controllers/questionController.js';

const router = express.Router();

router.route('/')
  .get(getQuestions)
  .post(protect, createQuestion);

router.route('/:id')
  .get(getQuestionById);

router.route('/:id/solve')
  .patch(protect, markAsSolved);

export default router;
