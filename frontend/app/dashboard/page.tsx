'use client';
import { useEffect, useState } from 'react';
import { fetchApi } from '../../lib/api';
import Sidebar from '../../components/dashboard/Sidebar';
import Header from '../../components/dashboard/Header';
import SummaryCards from '../../components/dashboard/SummaryCards';
import ProgressCard from '../../components/dashboard/ProgressCard';
import TodayTasks from '../../components/dashboard/TodayTasks';
import RecentActivity from '../../components/dashboard/RecentActivity';

export default function DashboardPage() {
  const [data, setData] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const loadDashboard = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await fetchApi('/api/dashboard');
      setData(response);
    } catch (err: any) {
      setError('Unable to load your dashboard. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex">
        <div className="w-64 bg-white border-r border-gray-200 min-h-screen hidden md:block"></div>
        <div className="flex-1 p-8">
          <div className="animate-pulse space-y-6">
            <div className="h-12 bg-gray-200 rounded w-1/4"></div>
            <div className="grid grid-cols-4 gap-6"><div className="h-24 bg-gray-200 rounded"></div><div className="h-24 bg-gray-200 rounded"></div><div className="h-24 bg-gray-200 rounded"></div><div className="h-24 bg-gray-200 rounded"></div></div>
            <div className="h-32 bg-gray-200 rounded"></div>
            <div className="grid grid-cols-3 gap-6"><div className="col-span-2 h-64 bg-gray-200 rounded"></div><div className="h-64 bg-gray-200 rounded"></div></div>
          </div>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error}</p>
          <button onClick={loadDashboard} className="bg-indigo-600 text-white px-4 py-2 rounded">Retry</button>
        </div>
      </div>
    );
  }

  if (!data) return null;

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col md:flex-row">
      <div className="hidden md:block">
        <Sidebar user={data.user} />
      </div>
      
      <div className="flex-1 flex flex-col min-w-0">
        <Header userName={data.user.name} />
        
        <main className="flex-1 p-4 sm:p-8 overflow-y-auto">
          <div className="max-w-7xl mx-auto">
            
            <SummaryCards summary={data.summary} />
            <ProgressCard today={data.today} />
            
            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-8">
              <div className="lg:col-span-2">
                <TodayTasks tasks={data.today_tasks} onRefresh={loadDashboard} />
              </div>
              <div>
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Quick Actions</h3>
                  <div className="space-y-3">
                    <button className="w-full bg-indigo-600 text-white py-2 rounded-md font-medium text-sm hover:bg-indigo-700">+ Add Task</button>
                    <button className="w-full bg-gray-100 text-gray-700 py-2 rounded-md font-medium text-sm hover:bg-gray-200">View All Tasks</button>
                    <button className="w-full bg-gray-100 text-gray-700 py-2 rounded-md font-medium text-sm hover:bg-gray-200">Calendar</button>
                    <button className="w-full bg-gray-100 text-gray-700 py-2 rounded-md font-medium text-sm hover:bg-gray-200">Analytics</button>
                  </div>
                </div>
              </div>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
              <div className="lg:col-span-2 grid grid-cols-1 md:grid-cols-2 gap-8">
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Task Status</h3>
                  <ul className="space-y-3">
                    {data.status_distribution.length === 0 ? <p className="text-sm text-gray-500">No status data</p> : 
                      data.status_distribution.map((s: any) => (
                        <li key={s.status} className="flex justify-between text-sm">
                          <span className="text-gray-600">{s.status}</span>
                          <span className="font-semibold">{s.count}</span>
                        </li>
                      ))
                    }
                  </ul>
                </div>
                <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
                  <h3 className="text-lg font-bold text-gray-900 mb-4">Categories</h3>
                  <ul className="space-y-3">
                    {data.category_distribution.length === 0 ? <p className="text-sm text-gray-500">No category data</p> : 
                      data.category_distribution.map((c: any) => (
                        <li key={c.category_id} className="flex justify-between text-sm">
                          <span className="text-gray-600 flex items-center">
                            <span className="w-2 h-2 rounded-full mr-2" style={{ backgroundColor: c.color || '#ccc' }}></span>
                            {c.category_name}
                          </span>
                          <span className="font-semibold">{c.count}</span>
                        </li>
                      ))
                    }
                  </ul>
                </div>
              </div>
              
              <div>
                <RecentActivity activities={data.recent_activity} />
              </div>
            </div>

          </div>
        </main>
      </div>
    </div>
  );
}
