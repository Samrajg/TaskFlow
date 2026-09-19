import Link from 'next/link';

export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50 flex flex-col">
      <header className="bg-white shadow px-8 py-4 flex justify-between items-center">
        <h1 className="text-xl font-bold text-indigo-600">TaskFlow</h1>
        <div className="flex space-x-4">
          <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">Dashboard</Link>
          <Link href="/tasks" className="text-gray-600 hover:text-gray-900">Tasks</Link>
          <Link href="/calendar" className="text-gray-600 hover:text-gray-900">Calendar</Link>
          <Link href="/analytics" className="text-gray-600 hover:text-gray-900">Analytics</Link>
          <Link href="/activity" className="text-gray-600 hover:text-gray-900">Activity</Link>
          <Link href="/settings" className="text-gray-600 hover:text-gray-900">Settings</Link>
          <Link href="/login" className="text-red-600 hover:text-red-800 font-medium">Logout</Link>
        </div>
      </header>
      <main className="flex-1 p-8 max-w-6xl mx-auto w-full">
        <h2 className="text-3xl font-bold text-gray-900 mb-6">Welcome to TaskFlow</h2>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-100 h-64 flex items-center justify-center">
          <p className="text-gray-500">Dashboard functionality coming soon.</p>
        </div>
      </main>
    </div>
  );
}
