import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import axios from 'axios';
import { formatDistanceToNow } from 'date-fns';
import { FiThumbsUp, FiMessageCircle, FiEye } from 'react-icons/fi';

export default function HomePage() {
  const [filter, setFilter] = useState('all');
  const [search, setSearch] = useState('');

  const { data, isLoading } = useQuery({
    queryKey: ['questions', filter, search],
    queryFn: async () => {
      const { data } = await axios.get(`http://localhost:5000/api/questions`, {
        params: { filter, search }
      });
      return data;
    }
  });

  if (isLoading) return <div className="text-center py-8">Loading...</div>;

  return (
    <div>
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-4">All Questions</h1>
        
        <div className="flex gap-4 mb-6">
          <button
            onClick={() => setFilter('all')}
            className={`px-4 py-2 rounded-lg ${filter === 'all' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700'}`}
          >
            All
          </button>
          <button
            onClick={() => setFilter('unanswered')}
            className={`px-4 py-2 rounded-lg ${filter === 'unanswered' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700'}`}
          >
            Unanswered
          </button>
          <button
            onClick={() => setFilter('solved')}
            className={`px-4 py-2 rounded-lg ${filter === 'solved' ? 'bg-blue-600 text-white' : 'bg-gray-200 dark:bg-gray-700'}`}
          >
            Solved
          </button>
        </div>
        
        <input
          type="text"
          placeholder="Search questions..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full p-3 border rounded-lg dark:bg-gray-800 dark:border-gray-700"
        />
      </div>
      
      <div className="space-y-4">
        {data?.questions?.map((question) => (
          <div key={question._id} className="bg-white dark:bg-gray-800 rounded-lg shadow-sm p-6 hover:shadow-md transition">
            <Link to={`/question/${question._id}`}>
              <h2 className="text-xl font-semibold text-gray-900 dark:text-white mb-2 hover:text-blue-600">
                {question.title}
              </h2>
            </Link>
            
            <div className="flex items-center gap-6 text-sm text-gray-500 dark:text-gray-400 mb-3">
              <div className="flex items-center gap-1">
                <FiThumbsUp /> {question.votes} votes
              </div>
              <div className="flex items-center gap-1">
                <FiMessageCircle /> {question.answers?.length || 0} answers
              </div>
              <div className="flex items-center gap-1">
                <FiEye /> {question.views} views
              </div>
            </div>
            
            <div className="flex flex-wrap gap-2 mb-3">
              {question.tags?.map(tag => (
                <span key={tag} className="px-2 py-1 bg-blue-100 dark:bg-blue-900 text-blue-600 dark:text-blue-300 text-xs rounded">
                  {tag}
                </span>
              ))}
            </div>
            
            <div className="text-sm text-gray-500 dark:text-gray-400">
              asked {formatDistanceToNow(new Date(question.createdAt))} ago by {question.author?.name}
            </div>
          </div>
        ))}
      </div>
      
      {data?.questions?.length === 0 && (
        <div className="text-center py-12 text-gray-500">No questions found</div>
      )}
    </div>
  );
}
