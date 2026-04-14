import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { createQuestion } from '../../services/api';
import toast from 'react-hot-toast';

const AskQuestion = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    title: '',
    description: '',
    subject: '',
    tags: ''
  });
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await createQuestion(formData);
      toast.success('Question posted successfully!');
      navigate(`/questions/${res.data._id}`);
    } catch (error) {
      toast.error('Failed to post question');
    }
    setLoading(false);
  };

  return (
    <div className="max-w-4xl mx-auto bg-white rounded-lg shadow p-6">
      <h1 className="text-3xl font-bold mb-6">Ask a Question</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Title"
          className="w-full p-2 border rounded mb-4"
          value={formData.title}
          onChange={(e) => setFormData({ ...formData, title: e.target.value })}
          required
        />
        <textarea
          rows="6"
          placeholder="Detailed description..."
          className="w-full p-2 border rounded mb-4"
          value={formData.description}
          onChange={(e) => setFormData({ ...formData, description: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Subject"
          className="w-full p-2 border rounded mb-4"
          value={formData.subject}
          onChange={(e) => setFormData({ ...formData, subject: e.target.value })}
          required
        />
        <input
          type="text"
          placeholder="Tags (comma-separated)"
          className="w-full p-2 border rounded mb-4"
          value={formData.tags}
          onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
        />
        <button
          type="submit"
          disabled={loading}
          className="bg-indigo-600 text-white px-6 py-2 rounded"
        >
          {loading ? 'Posting...' : 'Post Question'}
        </button>
      </form>
    </div>
  );
};

export default AskQuestion;
