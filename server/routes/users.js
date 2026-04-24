import express from 'express';
import { getUserProfile, getUserQuestions, getUserAnswers } from '../controllers/userController.js';

const router = express.Router();

router.route('/:id')
  .get(getUserProfile);

router.route('/:id/questions')
  .get(getUserQuestions);

router.route('/:id/answers')
  .get(getUserAnswers);

export default router;
