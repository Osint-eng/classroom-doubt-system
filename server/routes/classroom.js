import express from 'express';
import { protect, isTeacher } from '../middleware/auth.js';
import { createClassroom, joinClassroom, getClassroomDetails } from '../controllers/classroomController.js';

const router = express.Router();

router.post('/create', protect, isTeacher, createClassroom);
router.post('/join', protect, joinClassroom);
router.get('/:id', protect, getClassroomDetails);

export default router;
