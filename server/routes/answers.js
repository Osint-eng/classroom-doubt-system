import express from 'express';
import { protect } from '../middleware/auth.js';
import { postAnswer, acceptAnswer } from '../controllers/answerController.js';

const router = express.Router({ mergeParams: true });

router.route('/')
  .post(protect, postAnswer);

router.route('/:aid/accept')
  .patch(protect, acceptAnswer);

export default router;
