import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { getQuestionById, addAnswer } from '../../services/api';
import { useAuth } from '../../context/AuthContext';
import toast from 'react-hot-toast';

const QuestionDetail = () => {
  const { id } = useParams();
  const [question, setQuestion] = useState(null);
  const [answers, setAnswers] = useState([]);
  const [newAnswer, setNewAnswer] = useState('');
  const [loading, setLoading] = useState(true);
  const { user } = useAuth();

  useEffect(() => {
    fetchQuestion();
  }, [id]);

  const fetchQuestion = async () => {
  try {
    const res = await getQuestionById(id);
    console.log("API Response:", res.data); // Debug: see what's returned
    setQuestion(res.data);  // Changed from res.data.question
    setAnswers(res.data.answers || []);
  } catch (error) {
    console.error("Error:", error);
    toast.error('Failed to load question');
  } finally {
    setLoading(false);
  }
};

  const handleAddAnswer = async (e) => {
    e.preventDefault();
    if (!user) {
      toast.error('Please login to answer');
      return;
    }
    try {
      const res = await addAnswer(id, newAnswer);
      setAnswers([...answers, res.data]);
      setNewAnswer('');
      toast.success('Answer added!');
    } catch (error) {
      toast.error('Failed to add answer');
    }
  };

  if (loading) {
    return <div className="text-center py-10">Loading...</div>;
  }

  if (!question) {
    return <div className="text-center py-10">Question not found</div>;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-lg shadow p-6 mb-8">
        <h1 className="text-3xl font-bold mb-4">{question.title}</h1>
        <p className="text-gray-700 whitespace-pre-wrap">{question.description}</p>
        <div className="mt-4 text-sm text-gray-500">
          Asked by {question.author_info?.name}
        </div>
      </div>

      <div className="mb-8">
        <h2 className="text-2xl font-bold mb-4">{answers.length} Answers</h2>
        {answers.map((answer) => (
          <div key={answer._id} className="bg-white rounded-lg shadow p-4 mb-4">
            <p className="text-gray-700">{answer.content}</p>
            <div className="mt-2 text-sm text-gray-500">
              Answered by {answer.author_info?.name}
            </div>
          </div>
        ))}
      </div>

      {user && (
        <div className="bg-white rounded-lg shadow p-6">
          <h3 className="text-xl font-bold mb-4">Your Answer</h3>
          <form onSubmit={handleAddAnswer}>
            <textarea
              rows="5"
              className="w-full p-2 border rounded mb-4"
              value={newAnswer}
              onChange={(e) => setNewAnswer(e.target.value)}
              required
            />
            <button
              type="submit"
              className="bg-indigo-600 text-white px-6 py-2 rounded"
            >
              Post Answer
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default QuestionDetail;
