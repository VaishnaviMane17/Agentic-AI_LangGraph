import React from 'react';
import Image from 'next/image';
import { Product } from '@/types';
import { StarIcon, ShoppingBagIcon, ExternalLinkIcon } from '@heroicons/react/24/solid';

interface ProductCardProps {
  product: Product;
  onRefineSearch: () => void;
}

const ProductCard: React.FC<ProductCardProps> = ({ product, onRefineSearch }) => {
  const renderStars = (score: number) => {
    const stars = Math.round(score * 5);
    return (
      <div className="flex items-center">
        {[...Array(5)].map((_, i) => (
          <StarIcon
            key={i}
            className={`h-4 w-4 ${
              i < stars ? 'text-yellow-400' : 'text-gray-300'
            }`}
          />
        ))}
        <span className="ml-1 text-sm text-gray-600">
          ({(score * 5).toFixed(1)})
        </span>
      </div>
    );
  };

  return (
    <div className="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-200 overflow-hidden">
      {/* Product Image */}
      <div className="relative h-48 w-full">
        <Image
          src={product.image_url}
          alt={product.title}
          fill
          className="object-cover"
          sizes="(max-width: 768px) 100vw, (max-width: 1200px) 50vw, 33vw"
        />
      </div>

      {/* Product Content */}
      <div className="p-4">
        {/* Title and Price */}
        <div className="mb-3">
          <h3 className="text-lg font-semibold text-gray-900 line-clamp-2 mb-1">
            {product.title}
          </h3>
          <div className="flex items-center justify-between">
            <span className="text-2xl font-bold text-blue-600">
              {product.price}
            </span>
            {renderStars(product.score)}
          </div>
        </div>

        {/* Purchase Count */}
        <div className="flex items-center mb-3 text-sm text-gray-600">
          <ShoppingBagIcon className="h-4 w-4 mr-1" />
          <span>{product.purchases.toLocaleString()} purchases</span>
        </div>

        {/* Reviews Summary */}
        <div className="space-y-2 mb-4">
          <div className="bg-green-50 border border-green-200 rounded-md p-2">
            <h4 className="text-xs font-semibold text-green-800 mb-1">
              👍 Positive Reviews
            </h4>
            <p className="text-xs text-green-700">{product.good_reviews}</p>
          </div>
          
          <div className="bg-red-50 border border-red-200 rounded-md p-2">
            <h4 className="text-xs font-semibold text-red-800 mb-1">
              👎 Common Concerns
            </h4>
            <p className="text-xs text-red-700">{product.bad_reviews}</p>
          </div>
        </div>

        {/* Why We Picked This */}
        <div className="bg-blue-50 border border-blue-200 rounded-md p-2 mb-4">
          <h4 className="text-xs font-semibold text-blue-800 mb-1">
            🎯 Why we picked this
          </h4>
          <p className="text-xs text-blue-700">{product.reasoning}</p>
        </div>

        {/* Action Buttons */}
        <div className="flex space-x-2">
          <a
            href={product.product_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium py-2 px-3 rounded-md transition-colors duration-200 flex items-center justify-center"
          >
            <ExternalLinkIcon className="h-4 w-4 mr-1" />
            View Product
          </a>
          <button
            onClick={onRefineSearch}
            className="flex-1 bg-gray-100 hover:bg-gray-200 text-gray-700 text-sm font-medium py-2 px-3 rounded-md transition-colors duration-200"
          >
            Refine Search
          </button>
        </div>
      </div>
    </div>
  );
};

export default ProductCard;