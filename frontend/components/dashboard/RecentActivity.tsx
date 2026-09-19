export default function RecentActivity({ activities }: { activities: any[] }) {
  if (!activities || activities.length === 0) {
    return (
      <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
        <h3 className="text-lg font-bold text-gray-900 mb-4">Recent Activity</h3>
        <p className="text-gray-500 text-sm">No recent activity.</p>
      </div>
    );
  }

  const getIcon = (action: string) => {
    switch(action) {
      case 'COMPLETED': return '✓';
      case 'CREATED': return '+';
      case 'UPDATED': return '✏️';
      default: return '•';
    }
  };

  const getTimeAgo = (dateStr: string) => {
    const date = new Date(dateStr);
    const now = new Date();
    const diff = Math.floor((now.getTime() - date.getTime()) / 60000); // minutes
    
    if (diff < 1) return 'Just now';
    if (diff < 60) return `${diff} minutes ago`;
    const hours = Math.floor(diff / 60);
    if (hours < 24) return `${hours} hours ago`;
    return `${Math.floor(hours / 24)} days ago`;
  };

  return (
    <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100">
      <h3 className="text-lg font-bold text-gray-900 mb-6">Recent Activity</h3>
      <div className="space-y-6">
        {activities.map((act) => (
          <div key={act.id} className="flex">
            <div className="flex flex-col items-center mr-4">
              <div className="w-8 h-8 bg-gray-100 rounded-full flex items-center justify-center text-sm">
                {getIcon(act.action)}
              </div>
              <div className="w-px h-full bg-gray-200 mt-2"></div>
            </div>
            <div className="pb-2">
              <p className="text-sm font-medium text-gray-900">
                {act.action === 'COMPLETED' ? 'Completed a task' : 
                 act.action === 'CREATED' ? 'Created a task' : 
                 'Updated a task'}
              </p>
              <p className="text-xs text-gray-500 mt-1">{act.task_title || 'Unknown task'}</p>
              <p className="text-xs text-gray-400 mt-1">{getTimeAgo(act.created_at)}</p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
