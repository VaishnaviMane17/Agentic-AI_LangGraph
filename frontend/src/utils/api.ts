import axios from 'axios';
import { SearchRequest, SearchResponse } from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
});

export const searchProducts = async (request: SearchRequest): Promise<SearchResponse> => {
  try {
    const response = await api.post('/search', request);
    return response.data;
  } catch (error) {
    console.error('Search API error:', error);
    throw new Error('Failed to search products');
  }
};

export const refineSearch = async (request: SearchRequest): Promise<SearchResponse> => {
  try {
    const response = await api.post('/refine', request);
    return response.data;
  } catch (error) {
    console.error('Refine API error:', error);
    throw new Error('Failed to refine search');
  }
};

export const healthCheck = async (): Promise<boolean> => {
  try {
    const response = await api.get('/health');
    return response.data.status === 'healthy';
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
};