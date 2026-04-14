import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { getQuestions } from '../../services/api';

const QuestionList = () => {
  const [questions, setQuestions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getQuestions()
      .then((res) => {
        setQuestions(res.data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        setLoading(false);
      });
  }, []);

  if (loading) {
    return <div className="text-center py-10">Loading questions...</div>;
  }

  return (
    <div>
      <h1 className="text-3xl font-bold mb-6">All Questions</h1>
      {questions.length === 0 ? (
        <p className="text-gray-500">No questions yet. Be the first to ask!</p>
      ) : (
        questions.map((q) => (
          <div key={q._id} className="bg-white rounded-lg shadow p-4 mb-4">
            <Link
              to={`/questions/${q._id}`}
              className="text-xl font-semibold text-indigo-600 hover:text-indigo-800"
            >
              {q.title}
            </Link>
            <p className="text-gray-600 mt-2">{q.description?.substring(0, 150)}...</p>
            <div className="mt-2 text-sm text-gray-500">
              Asked by {q.author_info?.name} • {new Date(q.createdAt).toLocaleDateString()}
            </div>
          </div>
        ))
      )}
    </div>
  );
};

export default QuestionList;
