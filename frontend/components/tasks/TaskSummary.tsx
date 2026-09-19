export default function TaskSummary({ summary }: { summary: any }) {
  return (
    <div className="grid grid-cols-2 md:grid-cols-5 gap-4 mb-6">
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
        <div className="text-xs font-medium text-gray-500 mb-1">Total Tasks</div>
        <div className="text-2xl font-bold text-gray-900">{summary.total}</div>
      </div>
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
        <div className="text-xs font-medium text-gray-500 mb-1">Pending</div>
        <div className="text-2xl font-bold text-yellow-600">{summary.pending}</div>
      </div>
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
        <div className="text-xs font-medium text-gray-500 mb-1">In Progress</div>
        <div className="text-2xl font-bold text-blue-600">{summary.in_progress}</div>
      </div>
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
        <div className="text-xs font-medium text-gray-500 mb-1">Completed</div>
        <div className="text-2xl font-bold text-green-600">{summary.completed}</div>
      </div>
      <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100">
        <div className="text-xs font-medium text-gray-500 mb-1">Overdue</div>
        <div className="text-2xl font-bold text-red-600">{summary.overdue}</div>
      </div>
    </div>
  );
}
