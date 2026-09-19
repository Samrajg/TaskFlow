import { fetchApi } from '../../lib/api';

export default function TodayTasks({ tasks, onRefresh }: { tasks: any[], onRefresh: () => void }) {
  
  const handleToggle = async (taskId: string, currentStatus: string) => {
    const newStatus = currentStatus === 'COMPLETED' ? 'PENDING' : 'COMPLETED';
    try {
      await fetchApi(`/api/tasks/${taskId}`, {
        method: 'PATCH',
        body: JSON.stringify({ status: newStatus })
      });
      onRefresh();
    } catch (err) {
      console.error(err);
    }
  };

  if (!tasks || tasks.length === 0) {
    return (
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full flex flex-col items-center justify-center text-center">
        <p className="text-gray-500 mb-4">No tasks yet.</p>
        <p className="text-sm text-gray-400">Start organizing your day by creating your first task.</p>
      </div>
    );
  }

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-full">
      <h3 className="text-lg font-bold text-gray-900 mb-4">Today's Tasks</h3>
      <div className="space-y-4 max-h-[400px] overflow-y-auto pr-2">
        {tasks.map((task: any) => (
          <div key={task.id} className="flex items-start space-x-3 p-3 hover:bg-gray-50 rounded-lg border border-gray-100">
            <div className="pt-1">
              <input 
                type="checkbox" 
                checked={task.status === 'COMPLETED'}
                onChange={() => handleToggle(task.id, task.status)}
                className="h-5 w-5 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
              />
            </div>
            <div className="flex-1">
              <p className={`font-medium ${task.status === 'COMPLETED' ? 'text-gray-400 line-through' : 'text-gray-900'}`}>
                {task.title}
              </p>
              <div className="flex items-center mt-1 space-x-3 text-xs text-gray-500">
                {task.category_name && (
                  <span className="flex items-center">
                    <span 
                      className="w-2 h-2 rounded-full mr-1" 
                      style={{ backgroundColor: task.category_color || '#ccc' }}
                    ></span>
                    {task.category_name}
                  </span>
                )}
                <span className={`px-2 py-0.5 rounded text-[10px] font-semibold ${
                  task.priority === 'HIGH' ? 'bg-red-100 text-red-800' : 
                  task.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' : 
                  'bg-green-100 text-green-800'
                }`}>
                  {task.priority}
                </span>
                {task.due_time && <span>{task.due_time}</span>}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
