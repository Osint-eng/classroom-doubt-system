import express from 'express';
import { protect } from '../middleware/auth.js';
import { getNotifications, markAsRead } from '../controllers/notificationController.js';

const router = express.Router();

router.route('/')
  .get(protect, getNotifications);

router.route('/read')
  .patch(protect, markAsRead);

export default router;
