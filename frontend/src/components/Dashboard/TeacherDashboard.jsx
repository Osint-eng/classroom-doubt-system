import React, { useState, useEffect } from 'react';
import { getDashboard } from '../../services/api';

const TeacherDashboard = () => {
  const [data, setData] = useState(null);

  useEffect(() => {
    getDashboard()
      .then((res) => setData(res.data))
      .catch((err) => console.error(err));
  }, []);

  if (!data) {
    return <div className="text-center py-10">Loading dashboard...</div>;
  }

  return (
    <div className="max-w-4xl mx-auto">
      <h1 className="text-3xl font-bold mb-6">Teacher Dashboard</h1>
      <div className="bg-white rounded-lg shadow p-6">
        <div className="grid grid-cols-2 gap-4">
          <div className="text-center">
            <div className="text-2xl font-bold text-indigo-600">
              {data.stats?.totalAnswers || 0}
            </div>
            <div>Answers Given</div>
          </div>
          <div className="text-center">
            <div className="text-2xl font-bold text-yellow-600">
              {data.stats?.reputation || 0}
            </div>
            <div>Reputation</div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TeacherDashboard;
