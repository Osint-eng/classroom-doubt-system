import express from 'express';
import { getTags, getQuestionsByTag } from '../controllers/tagController.js';

const router = express.Router();

router.route('/')
  .get(getTags);

router.route('/:name')
  .get(getQuestionsByTag);

export default router;
