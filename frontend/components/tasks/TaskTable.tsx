export default function TaskTable({ tasks, loading, onEdit, onDelete, onView, onStatusChange }: any) {
  
  if (loading) {
    return (
      <div className="p-8 text-center text-gray-500">
        <div className="animate-pulse space-y-4">
          <div className="h-10 bg-gray-200 rounded w-full"></div>
          <div className="h-10 bg-gray-200 rounded w-full"></div>
          <div className="h-10 bg-gray-200 rounded w-full"></div>
        </div>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="p-12 text-center">
        <p className="text-gray-500 mb-2 font-medium">No tasks found</p>
        <p className="text-sm text-gray-400">Try changing your search or filters, or create your first task.</p>
      </div>
    );
  }

  return (
    <div className="overflow-x-auto">
      <table className="min-w-full divide-y divide-gray-200">
        <thead className="bg-gray-50">
          <tr>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Task</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden sm:table-cell">Category</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Priority</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Status</th>
            <th scope="col" className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider hidden md:table-cell">Due</th>
            <th scope="col" className="relative px-6 py-3"><span className="sr-only">Actions</span></th>
          </tr>
        </thead>
        <tbody className="bg-white divide-y divide-gray-200">
          {tasks.map((task: any) => (
            <tr key={task.id} className="hover:bg-gray-50">
              <td className="px-6 py-4">
                <div className="flex items-center">
                  <div className="pt-1 mr-3">
                    <input 
                      type="checkbox" 
                      checked={task.status === 'COMPLETED'}
                      onChange={() => onStatusChange(task.id, task.status === 'COMPLETED' ? 'PENDING' : 'COMPLETED')}
                      className="h-4 w-4 rounded border-gray-300 text-indigo-600 focus:ring-indigo-500 cursor-pointer"
                    />
                  </div>
                  <div>
                    <div className={`text-sm font-medium ${task.status === 'COMPLETED' ? 'text-gray-400 line-through' : 'text-gray-900'}`}>{task.title}</div>
                    {task.description && (
                      <div className="text-xs text-gray-500 truncate max-w-[200px] lg:max-w-[300px]">{task.description}</div>
                    )}
                  </div>
                </div>
              </td>
              <td className="px-6 py-4 whitespace-nowrap hidden sm:table-cell">
                {task.category_name ? (
                  <span className="flex items-center text-sm text-gray-500">
                    <span className="w-2 h-2 rounded-full mr-2" style={{ backgroundColor: task.category_color || '#ccc' }}></span>
                    {task.category_name}
                  </span>
                ) : (
                  <span className="text-sm text-gray-400">No Category</span>
                )}
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <span className={`px-2 inline-flex text-xs leading-5 font-semibold rounded-full ${
                  task.priority === 'HIGH' ? 'bg-red-100 text-red-800' : 
                  task.priority === 'MEDIUM' ? 'bg-yellow-100 text-yellow-800' : 
                  'bg-green-100 text-green-800'
                }`}>
                  {task.priority}
                </span>
              </td>
              <td className="px-6 py-4 whitespace-nowrap">
                <select 
                  value={task.status} 
                  onChange={(e) => onStatusChange(task.id, e.target.value)}
                  className={`text-xs font-semibold rounded-full px-2 py-1 border-0 ${
                    task.status === 'COMPLETED' ? 'bg-green-100 text-green-800' :
                    task.status === 'IN_PROGRESS' ? 'bg-blue-100 text-blue-800' :
                    task.status === 'PENDING' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-gray-100 text-gray-800'
                  }`}
                >
                  <option value="PENDING">PENDING</option>
                  <option value="IN_PROGRESS">IN PROGRESS</option>
                  <option value="COMPLETED">COMPLETED</option>
                  <option value="CANCELLED">CANCELLED</option>
                </select>
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 hidden md:table-cell">
                {task.due_date ? (
                  <div className="flex flex-col">
                    <span className={new Date(task.due_date) < new Date(new Date().toISOString().split('T')[0]) && task.status !== 'COMPLETED' ? 'text-red-600 font-semibold' : ''}>
                      {task.due_date}
                    </span>
                    {task.due_time && <span className="text-xs text-gray-400">{task.due_time}</span>}
                  </div>
                ) : (
                  <span className="text-gray-400">No due date</span>
                )}
              </td>
              <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div className="flex justify-end space-x-2">
                  <button onClick={() => onView(task)} className="text-gray-600 hover:text-gray-900">View</button>
                  <button onClick={() => onEdit(task)} className="text-indigo-600 hover:text-indigo-900">Edit</button>
                  <button onClick={() => onDelete(task)} className="text-red-600 hover:text-red-900">Delete</button>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
