import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { v4 as uuidv4 } from 'uuid';
import { ChatMessage, Product, RefinementOptions } from '@/types';
import { searchProducts, refineSearch } from '@/utils/api';
import ChatInterface from '@/components/ChatInterface';
import ProductCard from '@/components/ProductCard';
import RefinementPanel from '@/components/RefinementPanel';
import { SparklesIcon, AdjustmentsHorizontalIcon } from '@heroicons/react/24/solid';

const SearchPage: React.FC = () => {
  const router = useRouter();
  const { q } = router.query;

  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [sessionId, setSessionId] = useState<string>('');
  const [suggestions, setSuggestions] = useState<string[]>([]);
  const [isRefinementOpen, setIsRefinementOpen] = useState(false);
  const [refinementOptions, setRefinementOptions] = useState<Partial<RefinementOptions>>({});

  useEffect(() => {
    if (q && typeof q === 'string') {
      handleInitialSearch(q);
    }
  }, [q]);

  const handleInitialSearch = async (query: string) => {
    setIsLoading(true);
    
    // Add user message
    const userMessage: ChatMessage = {
      id: uuidv4(),
      type: 'user',
      content: query,
      timestamp: new Date(),
    };
    
    setMessages([userMessage]);

    try {
      const response = await searchProducts({ query });
      
      setProducts(response.products);
      setSessionId(response.session_id);
      setSuggestions(response.suggestions);

      // Add assistant response
      const assistantMessage: ChatMessage = {
        id: uuidv4(),
        type: 'assistant',
        content: `I found ${response.products.length} great options for "${response.query_processed}". Here are the top recommendations based on reviews, price, and features.`,
        timestamp: new Date(),
        products: response.products,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Search error:', error);
      
      const errorMessage: ChatMessage = {
        id: uuidv4(),
        type: 'assistant',
        content: 'Sorry, I encountered an error while searching for products. Please try again.',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSendMessage = async (message: string) => {
    setIsLoading(true);

    // Add user message
    const userMessage: ChatMessage = {
      id: uuidv4(),
      type: 'user',
      content: message,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      const response = sessionId 
        ? await refineSearch({ query: message, session_id: sessionId })
        : await searchProducts({ query: message });

      setProducts(response.products);
      setSessionId(response.session_id);
      setSuggestions(response.suggestions);

      // Add assistant response
      const assistantMessage: ChatMessage = {
        id: uuidv4(),
        type: 'assistant',
        content: `Updated search results! I found ${response.products.length} products that match your refined criteria.`,
        timestamp: new Date(),
        products: response.products,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Search error:', error);
      
      const errorMessage: ChatMessage = {
        id: uuidv4(),
        type: 'assistant',
        content: 'Sorry, I encountered an error. Please try rephrasing your request.',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleSuggestionClick = (suggestion: string) => {
    handleSendMessage(suggestion);
  };

  const handleRefineSearch = () => {
    setIsRefinementOpen(true);
  };

  const handleApplyRefinements = async (options: Partial<RefinementOptions>) => {
    setRefinementOptions(options);
    setIsLoading(true);

    // Build refinement message
    let refinementQuery = 'Refine my search';
    
    if (options.price_range) {
      refinementQuery += ` with budget between $${options.price_range.min} and $${options.price_range.max}`;
    }
    
    if (options.features && options.features.length > 0) {
      refinementQuery += ` including features: ${options.features.join(', ')}`;
    }
    
    if (options.verified_reviews_only) {
      refinementQuery += ' with verified reviews only';
    }

    // Add user message
    const userMessage: ChatMessage = {
      id: uuidv4(),
      type: 'user',
      content: refinementQuery,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);

    try {
      const response = await refineSearch({
        query: refinementQuery,
        session_id: sessionId,
        price_range: options.price_range,
        features_to_add: options.features,
      });

      setProducts(response.products);
      setSuggestions(response.suggestions);

      // Add assistant response
      const assistantMessage: ChatMessage = {
        id: uuidv4(),
        type: 'assistant',
        content: `Perfect! I've refined your search based on your preferences. Here are ${response.products.length} updated recommendations.`,
        timestamp: new Date(),
        products: response.products,
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Refinement error:', error);
      
      const errorMessage: ChatMessage = {
        id: uuidv4(),
        type: 'assistant',
        content: 'Sorry, I had trouble refining your search. Please try again.',
        timestamp: new Date(),
      };
      
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <button
              onClick={() => router.push('/')}
              className="flex items-center hover:opacity-80 transition-opacity"
            >
              <SparklesIcon className="h-8 w-8 text-blue-600 mr-2" />
              <h1 className="text-xl font-bold text-gray-900">
                AI Shopping Assistant
              </h1>
            </button>
            
            <button
              onClick={handleRefineSearch}
              className="flex items-center bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
            >
              <AdjustmentsHorizontalIcon className="h-5 w-5 mr-2" />
              Refine Search
            </button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6 h-[calc(100vh-8rem)]">
          {/* Chat Interface */}
          <div className="lg:col-span-2 bg-white rounded-lg shadow-sm border h-full">
            <ChatInterface
              messages={messages}
              onSendMessage={handleSendMessage}
              isLoading={isLoading}
              suggestions={suggestions}
              onSuggestionClick={handleSuggestionClick}
            />
          </div>

          {/* Product Results */}
          <div className="lg:col-span-3 h-full">
            <div className="bg-white rounded-lg shadow-sm border h-full p-6">
              <div className="flex items-center justify-between mb-6">
                <h2 className="text-xl font-semibold text-gray-900">
                  Product Recommendations
                </h2>
                {products.length > 0 && (
                  <span className="text-sm text-gray-500">
                    {products.length} result{products.length !== 1 ? 's' : ''}
                  </span>
                )}
              </div>

              <div className="h-full overflow-y-auto">
                {products.length === 0 && !isLoading && (
                  <div className="text-center py-12">
                    <div className="text-gray-400 text-6xl mb-4">🔍</div>
                    <h3 className="text-lg font-medium text-gray-900 mb-2">
                      No products yet
                    </h3>
                    <p className="text-gray-500">
                      Start a conversation to get personalized product recommendations.
                    </p>
                  </div>
                )}

                {isLoading && products.length === 0 && (
                  <div className="text-center py-12">
                    <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
                    <p className="text-gray-500">Searching for the best products...</p>
                  </div>
                )}

                <div className="grid grid-cols-1 xl:grid-cols-2 gap-4">
                  {products.map((product, index) => (
                    <ProductCard
                      key={index}
                      product={product}
                      onRefineSearch={handleRefineSearch}
                    />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Refinement Panel */}
      <RefinementPanel
        isOpen={isRefinementOpen}
        onClose={() => setIsRefinementOpen(false)}
        onApplyRefinements={handleApplyRefinements}
        currentOptions={refinementOptions}
      />
    </div>
  );
};

export default SearchPage;