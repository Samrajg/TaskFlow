import os

# Root Welcome Page
page_tsx = """import Link from 'next/link';

export default function Home() {
  return (
    <main className="min-h-screen bg-gray-50 flex flex-col items-center">
      {/* Header */}
      <header className="w-full bg-white shadow-sm py-4 px-8 flex justify-between items-center">
        <div className="text-2xl font-bold text-indigo-600 tracking-tight">TaskFlow</div>
        <Link href="/login" className="text-indigo-600 font-medium hover:text-indigo-800 transition">
          Sign In
        </Link>
      </header>

      {/* Hero */}
      <section className="flex-1 flex flex-col items-center justify-center text-center px-4 w-full max-w-4xl mx-auto py-20">
        <h1 className="text-5xl md:text-6xl font-extrabold text-gray-900 mb-6">
          Smart Daily Task Management
        </h1>
        <p className="text-xl text-gray-500 mb-10 max-w-2xl">
          Plan your day. Complete your tasks. Track your productivity.
        </p>
        <Link 
          href="/login" 
          className="bg-indigo-600 text-white font-semibold text-lg px-10 py-4 rounded-full shadow-lg hover:bg-indigo-700 hover:shadow-xl transition-all"
        >
          Get Started
        </Link>
      </section>

      {/* Features */}
      <section className="bg-white w-full py-20 px-8">
        <div className="max-w-5xl mx-auto">
          <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">Why TaskFlow?</h2>
          <div className="grid md:grid-cols-3 gap-12">
            <div className="text-center">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Organize Tasks</h3>
              <p className="text-gray-600">Keep all your daily tasks organized in one place.</p>
            </div>
            <div className="text-center">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Prioritize Work</h3>
              <p className="text-gray-600">Set task priorities and focus on what matters.</p>
            </div>
            <div className="text-center">
              <h3 className="text-xl font-bold text-gray-900 mb-4">Track Progress</h3>
              <p className="text-gray-600">Monitor completed, pending and overdue tasks.</p>
            </div>
          </div>
        </div>
      </section>
    </main>
  );
}
"""
with open("frontend/app/page.tsx", "w") as f: f.write(page_tsx)
