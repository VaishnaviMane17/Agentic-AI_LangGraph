export interface Product {
  title: string;
  price: string;
  image_url: string;
  product_url: string;
  purchases: number;
  good_reviews: string;
  bad_reviews: string;
  score: number;
  reasoning: string;
}

export interface SearchResponse {
  products: Product[];
  session_id: string;
  query_processed: string;
  suggestions: string[];
}

export interface SearchRequest {
  query: string;
  session_id?: string;
  price_range?: {
    min?: number;
    max?: number;
  };
  features_to_add?: string[];
  features_to_remove?: string[];
}

export interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  products?: Product[];
}

export interface RefinementOptions {
  price_range: {
    min: number;
    max: number;
  };
  features: string[];
  verified_reviews_only: boolean;
}