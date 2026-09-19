export default function SummaryCards({ summary }: { summary: any }) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div className="text-sm font-medium text-gray-500 mb-1">Total Tasks</div>
        <div className="text-3xl font-bold text-gray-900">{summary.total_tasks}</div>
        <div className="text-xs text-gray-400 mt-2">All tasks in your account</div>
      </div>
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div className="text-sm font-medium text-gray-500 mb-1">Completed</div>
        <div className="text-3xl font-bold text-green-600">{summary.completed_tasks}</div>
        <div className="text-xs text-gray-400 mt-2">Successfully finished</div>
      </div>
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div className="text-sm font-medium text-gray-500 mb-1">Pending</div>
        <div className="text-3xl font-bold text-yellow-600">{summary.pending_tasks}</div>
        <div className="text-xs text-gray-400 mt-2">Requires your attention</div>
      </div>
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <div className="text-sm font-medium text-gray-500 mb-1">Overdue</div>
        <div className="text-3xl font-bold text-red-600">{summary.overdue_tasks}</div>
        <div className="text-xs text-gray-400 mt-2">Past their due date</div>
      </div>
    </div>
  );
}
