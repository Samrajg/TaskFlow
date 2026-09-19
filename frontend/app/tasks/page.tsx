'use client';
import { useEffect, useState } from 'react';
import { fetchApi } from '../../lib/api';
import Sidebar from '../../components/dashboard/Sidebar';
import Header from '../../components/dashboard/Header';
import TaskSummary from '../../components/tasks/TaskSummary';
import TaskToolbar from '../../components/tasks/TaskToolbar';
import TaskTable from '../../components/tasks/TaskTable';
import TaskFormModal from '../../components/tasks/TaskFormModal';
import DeleteTaskDialog from '../../components/tasks/DeleteTaskDialog';
import TaskDetailsModal from '../../components/tasks/TaskDetailsModal';

export default function TasksPage() {
  const [tasks, setTasks] = useState<any[]>([]);
  const [categories, setCategories] = useState<any[]>([]);
  const [summary, setSummary] = useState({ total: 0, pending: 0, in_progress: 0, completed: 0, overdue: 0 });
  
  const [user, setUser] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  // Filters state
  const [search, setSearch] = useState('');
  const [status, setStatus] = useState('');
  const [priority, setPriority] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [dueDate, setDueDate] = useState('');
  const [sortBy, setSortBy] = useState('NEWEST');

  // Modals state
  const [isFormOpen, setIsFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState<any>(null);
  const [isDeleteOpen, setIsDeleteOpen] = useState(false);
  const [taskToDelete, setTaskToDelete] = useState<any>(null);
  const [isDetailsOpen, setIsDetailsOpen] = useState(false);
  const [viewingTask, setViewingTask] = useState<any>(null);
  const [toastMessage, setToastMessage] = useState('');

  const loadData = async () => {
    try {
      setLoading(true);
      setError('');
      
      const dashboardReq = fetchApi('/api/dashboard');
      const catsReq = fetchApi('/api/categories');
      
      const queryParams = new URLSearchParams();
      if (search) queryParams.append('search', search);
      if (status) queryParams.append('status', status);
      if (priority) queryParams.append('priority', priority);
      if (categoryId) queryParams.append('category_id', categoryId);
      if (dueDate) queryParams.append('due_date', dueDate);
      if (sortBy) queryParams.append('sort_by', sortBy);
      
      const tasksReq = fetchApi(`/api/tasks?${queryParams.toString()}`);

      const [dashData, catsData, tasksData] = await Promise.all([dashboardReq, catsReq, tasksReq]);
      
      setUser(dashData.user);
      setCategories(catsData.items);
      setTasks(tasksData.items);
      
      // Calculate summary locally from tasksData for simplicity if we don't have a direct endpoint,
      // but dashboardData has total/pending/completed/overdue! We can use that for global or compute from filtered:
      
      const total = dashData.summary.total_tasks;
      const completed = dashData.summary.completed_tasks;
      const pending = dashData.summary.pending_tasks; 
      const overdue = dashData.summary.overdue_tasks;
      // dashData doesn't specifically separate IN_PROGRESS cleanly in its old schema summary maybe? 
      // Actually it groups PENDING+IN_PROGRESS. Let's just compute from tasks list for precision on current view:
      
      let p = 0, i = 0, c = 0, o = 0;
      const todayDate = new Date().toISOString().split('T')[0];
      
      tasksData.items.forEach((t: any) => {
        if (t.status === 'PENDING') p++;
        if (t.status === 'IN_PROGRESS') i++;
        if (t.status === 'COMPLETED') c++;
        if (t.due_date && t.due_date < todayDate && t.status !== 'COMPLETED' && t.status !== 'CANCELLED') o++;
      });
      
      setSummary({ total: tasksData.total, pending: p, in_progress: i, completed: c, overdue: o });

    } catch (err: any) {
      setError('Unable to load your tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, [search, status, priority, categoryId, dueDate, sortBy]);

  const showToast = (msg: string) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(''), 3000);
  };

  const handleDelete = async () => {
    if (!taskToDelete) return;
    try {
      await fetchApi(`/api/tasks/${taskToDelete.id}`, { method: 'DELETE' });
      showToast('Task deleted.');
      setIsDeleteOpen(false);
      setTaskToDelete(null);
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  const handleStatusChange = async (taskId: string, newStatus: string) => {
    try {
      await fetchApi(`/api/tasks/${taskId}`, {
        method: 'PATCH',
        body: JSON.stringify({ status: newStatus })
      });
      if (newStatus === 'COMPLETED') showToast('Task completed.');
      else showToast('Status updated.');
      loadData();
    } catch (err: any) {
      alert(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col md:flex-row">
      <div className="hidden md:block">
        <Sidebar user={user} />
      </div>
      
      <div className="flex-1 flex flex-col min-w-0">
        <Header userName={user?.name || 'User'} />
        
        <main className="flex-1 p-4 sm:p-8 overflow-y-auto">
          <div className="max-w-7xl mx-auto">
            
            <div className="flex justify-between items-center mb-6">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">My Tasks</h1>
                <p className="text-sm text-gray-500 mt-1">Create, organize and track your tasks.</p>
              </div>
              <button 
                onClick={() => { setEditingTask(null); setIsFormOpen(true); }}
                className="bg-indigo-600 text-white px-4 py-2 rounded-md font-medium text-sm hover:bg-indigo-700"
              >
                + Create Task
              </button>
            </div>

            <TaskSummary summary={summary} />

            <TaskToolbar 
              categories={categories}
              search={search} setSearch={setSearch}
              status={status} setStatus={setStatus}
              priority={priority} setPriority={setPriority}
              categoryId={categoryId} setCategoryId={setCategoryId}
              dueDate={dueDate} setDueDate={setDueDate}
              sortBy={sortBy} setSortBy={setSortBy}
            />

            {error && (
              <div className="bg-red-50 text-red-600 p-4 rounded-md mb-6">
                <p>{error}</p>
                <button onClick={loadData} className="mt-2 text-sm font-semibold underline">Retry</button>
              </div>
            )}

            {!error && (
              <div className="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
                <TaskTable 
                  tasks={tasks} 
                  loading={loading}
                  onEdit={(t) => { setEditingTask(t); setIsFormOpen(true); }}
                  onDelete={(t) => { setTaskToDelete(t); setIsDeleteOpen(true); }}
                  onView={(t) => { setViewingTask(t); setIsDetailsOpen(true); }}
                  onStatusChange={handleStatusChange}
                />
              </div>
            )}

          </div>
        </main>
      </div>

      {isFormOpen && (
        <TaskFormModal 
          isOpen={isFormOpen}
          onClose={() => setIsFormOpen(false)}
          task={editingTask}
          categories={categories}
          onSuccess={(msg) => {
            setIsFormOpen(false);
            showToast(msg);
            loadData();
          }}
        />
      )}

      {isDeleteOpen && (
        <DeleteTaskDialog 
          isOpen={isDeleteOpen}
          onClose={() => setIsDeleteOpen(false)}
          onConfirm={handleDelete}
          taskName={taskToDelete?.title || 'this task'}
        />
      )}

      {isDetailsOpen && viewingTask && (
        <TaskDetailsModal 
          isOpen={isDetailsOpen}
          onClose={() => setIsDetailsOpen(false)}
          task={viewingTask}
        />
      )}

      {toastMessage && (
        <div className="fixed bottom-4 right-4 bg-gray-900 text-white px-6 py-3 rounded-lg shadow-lg text-sm font-medium animate-fade-in-up">
          {toastMessage}
        </div>
      )}

    </div>
  );
}
