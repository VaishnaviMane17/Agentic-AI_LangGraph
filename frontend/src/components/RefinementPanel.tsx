import React, { useState } from 'react';
import { RefinementOptions } from '@/types';
import { AdjustmentsHorizontalIcon, XMarkIcon } from '@heroicons/react/24/outline';

interface RefinementPanelProps {
  isOpen: boolean;
  onClose: () => void;
  onApplyRefinements: (options: Partial<RefinementOptions>) => void;
  currentOptions?: Partial<RefinementOptions>;
}

const RefinementPanel: React.FC<RefinementPanelProps> = ({
  isOpen,
  onClose,
  onApplyRefinements,
  currentOptions = {},
}) => {
  const [priceRange, setPriceRange] = useState({
    min: currentOptions.price_range?.min || 0,
    max: currentOptions.price_range?.max || 500,
  });
  
  const [newFeature, setNewFeature] = useState('');
  const [features, setFeatures] = useState<string[]>(
    currentOptions.features || []
  );
  
  const [verifiedOnly, setVerifiedOnly] = useState(
    currentOptions.verified_reviews_only || false
  );

  const handleAddFeature = () => {
    if (newFeature.trim() && !features.includes(newFeature.trim())) {
      setFeatures([...features, newFeature.trim()]);
      setNewFeature('');
    }
  };

  const handleRemoveFeature = (featureToRemove: string) => {
    setFeatures(features.filter((f) => f !== featureToRemove));
  };

  const handleApply = () => {
    onApplyRefinements({
      price_range: priceRange,
      features,
      verified_reviews_only: verifiedOnly,
    });
    onClose();
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleAddFeature();
    }
  };

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 z-50 flex items-center justify-center">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md m-4 max-h-[90vh] overflow-y-auto">
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b">
          <div className="flex items-center">
            <AdjustmentsHorizontalIcon className="h-5 w-5 mr-2 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900">
              Refine Your Search
            </h3>
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
          >
            <XMarkIcon className="h-6 w-6" />
          </button>
        </div>

        {/* Content */}
        <div className="p-4 space-y-6">
          {/* Price Range */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Price Range
            </label>
            <div className="space-y-3">
              <div className="flex items-center space-x-4">
                <div className="flex-1">
                  <label className="block text-xs text-gray-500 mb-1">Min</label>
                  <input
                    type="number"
                    value={priceRange.min}
                    onChange={(e) =>
                      setPriceRange({ ...priceRange, min: Number(e.target.value) })
                    }
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    min="0"
                  />
                </div>
                <div className="flex-1">
                  <label className="block text-xs text-gray-500 mb-1">Max</label>
                  <input
                    type="number"
                    value={priceRange.max}
                    onChange={(e) =>
                      setPriceRange({ ...priceRange, max: Number(e.target.value) })
                    }
                    className="w-full border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    min="0"
                  />
                </div>
              </div>
              <div className="text-center text-sm text-gray-600">
                ${priceRange.min} - ${priceRange.max}
              </div>
            </div>
          </div>

          {/* Features */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-3">
              Add/Remove Features
            </label>
            
            {/* Add Feature Input */}
            <div className="flex space-x-2 mb-3">
              <input
                type="text"
                value={newFeature}
                onChange={(e) => setNewFeature(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="e.g., wireless, waterproof"
                className="flex-1 border border-gray-300 rounded-md px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <button
                onClick={handleAddFeature}
                disabled={!newFeature.trim()}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-300 text-white px-4 py-2 rounded-md transition-colors"
              >
                Add
              </button>
            </div>

            {/* Current Features */}
            <div className="flex flex-wrap gap-2">
              {features.map((feature, index) => (
                <span
                  key={index}
                  className="inline-flex items-center bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full"
                >
                  {feature}
                  <button
                    onClick={() => handleRemoveFeature(feature)}
                    className="ml-2 text-blue-600 hover:text-blue-800"
                  >
                    <XMarkIcon className="h-4 w-4" />
                  </button>
                </span>
              ))}
            </div>
          </div>

          {/* Verified Reviews Toggle */}
          <div>
            <label className="flex items-center space-x-3">
              <input
                type="checkbox"
                checked={verifiedOnly}
                onChange={(e) => setVerifiedOnly(e.target.checked)}
                className="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
              />
              <div>
                <span className="text-sm font-medium text-gray-700">
                  Verified Reviews Only
                </span>
                <p className="text-xs text-gray-500">
                  Show only products with verified customer reviews
                </p>
              </div>
            </label>
          </div>
        </div>

        {/* Footer */}
        <div className="flex space-x-3 p-4 border-t bg-gray-50">
          <button
            onClick={onClose}
            className="flex-1 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium py-2 px-4 rounded-md transition-colors"
          >
            Cancel
          </button>
          <button
            onClick={handleApply}
            className="flex-1 bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors"
          >
            Apply Refinements
          </button>
        </div>
      </div>
    </div>
  );
};

export default RefinementPanel;