export default function Header({ userName }: { userName: string }) {
  const getGreeting = () => {
    const hour = new Date().getHours();
    if (hour < 12) return 'Good Morning';
    if (hour < 18) return 'Good Afternoon';
    return 'Good Evening';
  };

  return (
    <header className="bg-white shadow-sm px-8 py-6 flex flex-col sm:flex-row justify-between items-start sm:items-center">
      <div>
        <h2 className="text-2xl font-bold text-gray-900">{getGreeting()}, {userName} 👋</h2>
        <p className="text-sm text-gray-500 mt-1">Here's your productivity overview for today.</p>
      </div>
      <div className="mt-4 sm:mt-0 flex items-center space-x-4">
        <div className="relative">
          <input 
            type="text" 
            placeholder="Search..." 
            className="border border-gray-300 rounded-full py-1.5 px-4 text-sm focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <button className="text-gray-400 hover:text-gray-600">
          <span className="sr-only">Notifications</span>
          🔔
        </button>
      </div>
    </header>
  );
}
