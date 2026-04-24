import express from 'express';
import { protect } from '../middleware/auth.js';
import { voteQuestion, voteAnswer } from '../controllers/voteController.js';

const router = express.Router();

router.post('/question/:id', protect, voteQuestion);
router.post('/answer/:id', protect, voteAnswer);

export default router;
