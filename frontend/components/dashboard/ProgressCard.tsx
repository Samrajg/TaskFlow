export default function ProgressCard({ today }: { today: any }) {
  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 mb-8">
      <div className="flex justify-between items-end mb-4">
        <div>
          <h3 className="text-lg font-bold text-gray-900">Today's Progress</h3>
          <p className="text-sm text-gray-500 mt-1">
            {today.total_tasks === 0 
              ? "No tasks scheduled for today." 
              : `${today.completed_tasks} / ${today.total_tasks} tasks completed`}
          </p>
        </div>
        {today.total_tasks > 0 && (
          <div className="text-2xl font-bold text-indigo-600">{today.progress_percentage}%</div>
        )}
      </div>
      
      {today.total_tasks > 0 && (
        <div className="w-full bg-gray-200 rounded-full h-3">
          <div 
            className="bg-indigo-600 h-3 rounded-full transition-all duration-500 ease-in-out" 
            style={{ width: `${today.progress_percentage}%` }}
          ></div>
        </div>
      )}
    </div>
  );
}
