import React, { useState } from 'react';
import { useRouter } from 'next/router';
import { MagnifyingGlassIcon, SparklesIcon } from '@heroicons/react/24/solid';

const exampleQueries = [
  "I want a budget-friendly gaming mouse with RGB lighting",
  "Looking for a leather wallet with RFID blocking and keychain",
  "Need wireless noise-cancelling headphones for under $150",
  "Find me a durable water bottle for hiking",
  "I want a comfortable office chair for working from home",
];

const HomePage: React.FC = () => {
  const [query, setQuery] = useState('');
  const router = useRouter();

  const handleSearch = (searchQuery: string) => {
    if (searchQuery.trim()) {
      router.push(`/search?q=${encodeURIComponent(searchQuery.trim())}`);
    }
  };

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    handleSearch(query);
  };

  const handleExampleClick = (example: string) => {
    setQuery(example);
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <SparklesIcon className="h-8 w-8 text-blue-600 mr-2" />
              <h1 className="text-xl font-bold text-gray-900">
                AI Shopping Assistant
              </h1>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center">
          {/* Hero Section */}
          <div className="mb-12">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
              Find the Perfect Product with{' '}
              <span className="text-blue-600">AI-Powered Search</span>
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Tell us what you're looking for in plain English, and our AI will 
              find the best products based on reviews, prices, and features.
            </p>
          </div>

          {/* Search Form */}
          <form onSubmit={handleSubmit} className="mb-12">
            <div className="max-w-2xl mx-auto">
              <div className="relative">
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="I want a budget-friendly gaming mouse with RGB lighting..."
                  className="w-full px-6 py-4 text-lg border-2 border-gray-300 rounded-full focus:outline-none focus:ring-4 focus:ring-blue-500 focus:border-blue-500 shadow-lg"
                />
                <button
                  type="submit"
                  disabled={!query.trim()}
                  className="absolute right-2 top-2 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white p-3 rounded-full transition-colors duration-200 shadow-lg"
                >
                  <MagnifyingGlassIcon className="h-6 w-6" />
                </button>
              </div>
              <button
                type="submit"
                disabled={!query.trim()}
                className="mt-4 bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white font-semibold py-3 px-8 rounded-full transition-colors duration-200 shadow-lg"
              >
                Find Products
              </button>
            </div>
          </form>

          {/* Example Queries */}
          <div className="mb-16">
            <h3 className="text-lg font-semibold text-gray-700 mb-4">
              Try these examples:
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 max-w-4xl mx-auto">
              {exampleQueries.map((example, index) => (
                <button
                  key={index}
                  onClick={() => handleExampleClick(example)}
                  className="bg-white hover:bg-blue-50 border border-gray-200 hover:border-blue-300 rounded-lg p-4 text-left transition-colors duration-200 shadow-sm hover:shadow-md"
                >
                  <div className="text-sm text-gray-600 line-clamp-3">
                    "{example}"
                  </div>
                </button>
              ))}
            </div>
          </div>

          {/* Features Section */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
            <div className="bg-white rounded-lg p-6 shadow-lg">
              <div className="text-blue-600 text-3xl mb-4">🎯</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Smart Matching
              </h3>
              <p className="text-gray-600">
                Our AI understands your requirements and finds products that 
                match your specific needs and preferences.
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-lg">
              <div className="text-blue-600 text-3xl mb-4">📊</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Review Analysis
              </h3>
              <p className="text-gray-600">
                We analyze thousands of reviews to give you insights into 
                what customers love and what to watch out for.
              </p>
            </div>

            <div className="bg-white rounded-lg p-6 shadow-lg">
              <div className="text-blue-600 text-3xl mb-4">💬</div>
              <h3 className="text-lg font-semibold text-gray-900 mb-2">
                Conversational Search
              </h3>
              <p className="text-gray-600">
                Refine your search naturally by chatting with our AI. 
                Add features, change budget, or explore alternatives.
              </p>
            </div>
          </div>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-white border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center text-gray-500">
            <p>&copy; 2024 AI Shopping Assistant. Powered by LangGraph and OpenAI.</p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default HomePage;