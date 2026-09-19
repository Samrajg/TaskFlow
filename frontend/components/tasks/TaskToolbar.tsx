export default function TaskToolbar({ 
  categories, search, setSearch, status, setStatus, priority, setPriority, categoryId, setCategoryId, dueDate, setDueDate, sortBy, setSortBy 
}: any) {
  return (
    <div className="bg-white p-4 rounded-xl shadow-sm border border-gray-100 mb-6 flex flex-col md:flex-row flex-wrap gap-4 items-center justify-between">
      <div className="w-full md:w-auto flex-1">
        <input 
          type="text" 
          placeholder="Search tasks..." 
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="w-full border border-gray-300 rounded-md py-1.5 px-3 text-sm focus:ring-indigo-500 focus:border-indigo-500"
        />
      </div>
      
      <div className="flex flex-wrap gap-3 w-full md:w-auto">
        <select value={status} onChange={(e) => setStatus(e.target.value)} className="border border-gray-300 rounded-md py-1.5 px-3 text-sm">
          <option value="">All Status</option>
          <option value="PENDING">Pending</option>
          <option value="IN_PROGRESS">In Progress</option>
          <option value="COMPLETED">Completed</option>
          <option value="CANCELLED">Cancelled</option>
        </select>

        <select value={priority} onChange={(e) => setPriority(e.target.value)} className="border border-gray-300 rounded-md py-1.5 px-3 text-sm">
          <option value="">All Priorities</option>
          <option value="HIGH">High</option>
          <option value="MEDIUM">Medium</option>
          <option value="LOW">Low</option>
        </select>

        <select value={categoryId} onChange={(e) => setCategoryId(e.target.value)} className="border border-gray-300 rounded-md py-1.5 px-3 text-sm">
          <option value="">All Categories</option>
          {(categories || []).map((c: any) => (
            <option key={c.id} value={c.id}>{c.name}</option>
          ))}
        </select>

        <select value={dueDate} onChange={(e) => setDueDate(e.target.value)} className="border border-gray-300 rounded-md py-1.5 px-3 text-sm">
          <option value="">Any Due Date</option>
          <option value="TODAY">Today</option>
          <option value="OVERDUE">Overdue</option>
          <option value="NONE">No Due Date</option>
        </select>

        <select value={sortBy} onChange={(e) => setSortBy(e.target.value)} className="border border-gray-300 rounded-md py-1.5 px-3 text-sm bg-gray-50">
          <option value="NEWEST">Sort: Newest</option>
          <option value="OLDEST">Sort: Oldest</option>
          <option value="DUE_DATE">Sort: Due Date</option>
          <option value="PRIORITY">Sort: Priority</option>
        </select>
      </div>
    </div>
  );
}
