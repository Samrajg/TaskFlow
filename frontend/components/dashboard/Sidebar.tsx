import Link from 'next/link';

export default function Sidebar({ user }: { user: any }) {
  return (
    <div className="w-64 bg-white border-r border-gray-200 min-h-screen flex flex-col">
      <div className="p-6">
        <h1 className="text-2xl font-bold text-indigo-600 tracking-tight">TaskFlow</h1>
      </div>
      
      <nav className="flex-1 px-4 space-y-1">
        <Link href="/dashboard" className="bg-indigo-50 text-indigo-700 flex items-center px-3 py-2 rounded-md text-sm font-medium">
          Dashboard
        </Link>
        <Link href="/dashboard" className="text-gray-600 hover:bg-gray-50 hover:text-gray-900 flex items-center px-3 py-2 rounded-md text-sm font-medium">
          My Tasks
        </Link>
        <Link href="/dashboard" className="text-gray-600 hover:bg-gray-50 hover:text-gray-900 flex items-center px-3 py-2 rounded-md text-sm font-medium">
          Calendar
        </Link>
        <Link href="/dashboard" className="text-gray-600 hover:bg-gray-50 hover:text-gray-900 flex items-center px-3 py-2 rounded-md text-sm font-medium">
          Categories
        </Link>
        <Link href="/dashboard" className="text-gray-600 hover:bg-gray-50 hover:text-gray-900 flex items-center px-3 py-2 rounded-md text-sm font-medium">
          Analytics
        </Link>
        <Link href="/dashboard" className="text-gray-600 hover:bg-gray-50 hover:text-gray-900 flex items-center px-3 py-2 rounded-md text-sm font-medium">
          Activity
        </Link>
      </nav>

      <div className="p-4 border-t border-gray-200">
        <div className="flex items-center space-x-3 mb-4">
          <div className="w-10 h-10 rounded-full bg-indigo-100 flex items-center justify-center text-indigo-700 font-bold">
            {user?.name?.charAt(0).toUpperCase()}
          </div>
          <div className="overflow-hidden">
            <p className="text-sm font-medium text-gray-900 truncate">{user?.name}</p>
            <p className="text-xs text-gray-500 truncate">{user?.email}</p>
          </div>
        </div>
        <button 
          onClick={() => {
            localStorage.removeItem('taskflow_token');
            window.location.href = '/login';
          }}
          className="w-full text-left text-sm text-red-600 font-medium hover:text-red-700"
        >
          Logout
        </button>
      </div>
    </div>
  );
}
