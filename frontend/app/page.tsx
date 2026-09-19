import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center bg-gray-50 text-gray-900 p-4">
      <div className="max-w-3xl text-center space-y-6 bg-white p-12 rounded-2xl shadow-xl border border-gray-100">
        <h1 className="text-5xl font-extrabold tracking-tight text-indigo-600">
          TaskFlow
        </h1>
        <h2 className="text-2xl font-medium text-gray-700">
          Smart Daily Task Management
        </h2>
        <p className="text-lg text-gray-500 max-w-xl mx-auto">
          Plan your day, manage your tasks, and track your productivity from one place.
        </p>
        <div className="pt-8">
          <Link 
            href="/login" 
            className="inline-block bg-indigo-600 text-white font-semibold text-lg px-8 py-4 rounded-full hover:bg-indigo-700 transition-colors shadow-lg hover:shadow-indigo-200"
          >
            Get Started
          </Link>
        </div>
      </div>
    </main>
  );
}
