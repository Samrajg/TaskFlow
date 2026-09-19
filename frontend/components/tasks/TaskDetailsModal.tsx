export default function TaskDetailsModal({ isOpen, onClose, task }: any) {
  if (!isOpen || !task) return null;
  return (
    <div className="fixed inset-0 z-50 overflow-y-auto" role="dialog" aria-modal="true">
      <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
        <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={onClose}></div>
        <span className="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>
        <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
          <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div className="flex justify-between items-start mb-4">
              <h3 className="text-xl font-bold text-gray-900">{task.title}</h3>
              <button onClick={onClose} className="text-gray-400 hover:text-gray-500">&times;</button>
            </div>
            
            <div className="space-y-4">
              <div>
                <h4 className="text-xs font-semibold text-gray-500 uppercase">Description</h4>
                <p className="mt-1 text-sm text-gray-900 whitespace-pre-wrap">{task.description || 'No description provided.'}</p>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="text-xs font-semibold text-gray-500 uppercase">Category</h4>
                  <p className="mt-1 text-sm text-gray-900">
                    {task.category_name ? (
                      <span className="flex items-center">
                        <span className="w-2 h-2 rounded-full mr-2" style={{ backgroundColor: task.category_color || '#ccc' }}></span>
                        {task.category_name}
                      </span>
                    ) : 'No Category'}
                  </p>
                </div>
                <div>
                  <h4 className="text-xs font-semibold text-gray-500 uppercase">Priority</h4>
                  <p className="mt-1 text-sm text-gray-900">{task.priority}</p>
                </div>
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="text-xs font-semibold text-gray-500 uppercase">Status</h4>
                  <p className="mt-1 text-sm text-gray-900">{task.status}</p>
                </div>
                <div>
                  <h4 className="text-xs font-semibold text-gray-500 uppercase">Due</h4>
                  <p className="mt-1 text-sm text-gray-900">
                    {task.due_date ? `${task.due_date} ${task.due_time || ''}` : 'No due date'}
                  </p>
                </div>
              </div>

              <div className="border-t border-gray-100 pt-4 grid grid-cols-2 gap-4 text-xs text-gray-500">
                <div>
                  <span className="font-semibold block">Created</span>
                  {new Date(task.created_at).toLocaleString()}
                </div>
                <div>
                  <span className="font-semibold block">Updated</span>
                  {new Date(task.updated_at).toLocaleString()}
                </div>
                {task.completed_at && (
                  <div className="col-span-2">
                    <span className="font-semibold block">Completed At</span>
                    {new Date(task.completed_at).toLocaleString()}
                  </div>
                )}
              </div>
            </div>
          </div>
          <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button onClick={onClose} type="button" className="w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 sm:mt-0 sm:w-auto sm:text-sm">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
