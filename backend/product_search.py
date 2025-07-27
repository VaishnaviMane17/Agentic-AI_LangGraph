import requests
import time
import random
from typing import List, Dict, Optional
from bs4 import BeautifulSoup
import os

class ProductSearcher:
    def __init__(self):
        self.serpapi_key = os.getenv("SERPAPI_API_KEY")
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
    
    def search(self, product_type: str, features: List[str], 
               price_range: Optional[Dict] = None, max_results: int = 10) -> List[Dict]:
        """Search for products using Google Shopping"""
        
        # Build search query
        query = self._build_search_query(product_type, features, price_range)
        
        if self.serpapi_key:
            return self._search_with_serpapi(query, max_results)
        else:
            # Use mock data for development/testing
            return self._get_mock_products(product_type, features, max_results)
    
    def _build_search_query(self, product_type: str, features: List[str], 
                           price_range: Optional[Dict] = None) -> str:
        """Build search query from parameters"""
        query_parts = [product_type]
        query_parts.extend(features)
        
        if price_range:
            if price_range.get("min"):
                query_parts.append(f"over ${price_range['min']}")
            if price_range.get("max"):
                query_parts.append(f"under ${price_range['max']}")
        
        return " ".join(query_parts)
    
    def _search_with_serpapi(self, query: str, max_results: int) -> List[Dict]:
        """Search using SerpAPI (Google Shopping)"""
        try:
            url = "https://serpapi.com/search.json"
            params = {
                "q": query,
                "engine": "google_shopping",
                "api_key": self.serpapi_key,
                "num": max_results
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            products = []
            for item in data.get("shopping_results", [])[:max_results]:
                product = {
                    "title": item.get("title", ""),
                    "price": item.get("price", ""),
                    "price_numeric": self._extract_price_numeric(item.get("price", "")),
                    "image_url": item.get("thumbnail", ""),
                    "product_url": item.get("link", ""),
                    "source": item.get("source", ""),
                    "rating": item.get("rating", 0),
                    "reviews_count": item.get("reviews", 0)
                }
                products.append(product)
            
            return products
            
        except Exception as e:
            print(f"SerpAPI search failed: {e}")
            # Fallback to mock data
            return self._get_mock_products(query.split()[0] if query else "product", [], max_results)
    
    def _get_mock_products(self, product_type: str, features: List[str], max_results: int) -> List[Dict]:
        """Generate mock product data for development"""
        
        # Sample product templates based on common categories
        mock_data = {
            "wallet": [
                {
                    "title": "Premium Leather Bifold Wallet with RFID Blocking",
                    "price": "$29.99",
                    "price_numeric": 29.99,
                    "image_url": "https://via.placeholder.com/300x300/8B4513/FFFFFF?text=Leather+Wallet",
                    "product_url": "https://example.com/product/1",
                    "source": "Amazon",
                    "rating": 4.5,
                    "reviews_count": 1250
                },
                {
                    "title": "Minimalist Carbon Fiber Wallet with Money Clip",
                    "price": "$19.99",
                    "price_numeric": 19.99,
                    "image_url": "https://via.placeholder.com/300x300/2F2F2F/FFFFFF?text=Carbon+Wallet",
                    "product_url": "https://example.com/product/2",
                    "source": "Best Buy",
                    "rating": 4.2,
                    "reviews_count": 890
                },
                {
                    "title": "Vintage Brown Leather Wallet with Keychain Attachment",
                    "price": "$39.95",
                    "price_numeric": 39.95,
                    "image_url": "https://via.placeholder.com/300x300/8B4513/FFFFFF?text=Vintage+Wallet",
                    "product_url": "https://example.com/product/3",
                    "source": "Etsy",
                    "rating": 4.7,
                    "reviews_count": 567
                }
            ],
            "mouse": [
                {
                    "title": "Gaming Mouse with RGB Lighting and Programmable Buttons",
                    "price": "$49.99",
                    "price_numeric": 49.99,
                    "image_url": "https://via.placeholder.com/300x300/FF0000/FFFFFF?text=RGB+Gaming+Mouse",
                    "product_url": "https://example.com/product/4",
                    "source": "Newegg",
                    "rating": 4.6,
                    "reviews_count": 2340
                },
                {
                    "title": "Wireless Ergonomic Mouse for Office Work",
                    "price": "$24.99",
                    "price_numeric": 24.99,
                    "image_url": "https://via.placeholder.com/300x300/0000FF/FFFFFF?text=Wireless+Mouse",
                    "product_url": "https://example.com/product/5",
                    "source": "Amazon",
                    "rating": 4.3,
                    "reviews_count": 1567
                },
                {
                    "title": "Budget Gaming Mouse with High DPI Sensor",
                    "price": "$15.99",
                    "price_numeric": 15.99,
                    "image_url": "https://via.placeholder.com/300x300/00FF00/FFFFFF?text=Budget+Gaming",
                    "product_url": "https://example.com/product/6",
                    "source": "Walmart",
                    "rating": 4.0,
                    "reviews_count": 892
                }
            ],
            "headphones": [
                {
                    "title": "Wireless Noise-Cancelling Over-Ear Headphones",
                    "price": "$129.99",
                    "price_numeric": 129.99,
                    "image_url": "https://via.placeholder.com/300x300/000000/FFFFFF?text=Noise+Cancel",
                    "product_url": "https://example.com/product/7",
                    "source": "Best Buy",
                    "rating": 4.8,
                    "reviews_count": 3456
                },
                {
                    "title": "Budget Wired Gaming Headset with Microphone",
                    "price": "$39.99",
                    "price_numeric": 39.99,
                    "image_url": "https://via.placeholder.com/300x300/FF00FF/FFFFFF?text=Gaming+Headset",
                    "product_url": "https://example.com/product/8",
                    "source": "Amazon",
                    "rating": 4.1,
                    "reviews_count": 1789
                },
                {
                    "title": "Premium Bluetooth Earbuds with Charging Case",
                    "price": "$89.99",
                    "price_numeric": 89.99,
                    "image_url": "https://via.placeholder.com/300x300/FFFFFF/000000?text=Bluetooth+Buds",
                    "product_url": "https://example.com/product/9",
                    "source": "Target",
                    "rating": 4.4,
                    "reviews_count": 2134
                }
            ]
        }
        
        # Try to find relevant products based on product type
        products = []
        for key, items in mock_data.items():
            if key.lower() in product_type.lower() or product_type.lower() in key.lower():
                products.extend(items)
                break
        
        # If no specific category found, use mixed products
        if not products:
            all_products = []
            for items in mock_data.values():
                all_products.extend(items)
            products = random.sample(all_products, min(len(all_products), max_results))
        
        # Add some randomization to simulate real search results
        for product in products[:max_results]:
            # Add some variation to prices and ratings
            base_price = product["price_numeric"]
            variation = random.uniform(0.9, 1.1)
            product["price_numeric"] = round(base_price * variation, 2)
            product["price"] = f"${product['price_numeric']}"
            
            # Add mock purchase data
            product["purchases"] = random.randint(50, 5000)
        
        return products[:max_results]
    
    def _extract_price_numeric(self, price_str: str) -> float:
        """Extract numeric price from price string"""
        if not price_str:
            return 0.0
        
        # Remove currency symbols and extract number
        import re
        numbers = re.findall(r'[\d,]+\.?\d*', price_str.replace(',', ''))
        if numbers:
            try:
                return float(numbers[0])
            except ValueError:
                return 0.0
        return 0.0
    
    def scrape_product_details(self, product_url: str) -> Dict:
        """Scrape additional product details from the product page"""
        try:
            response = requests.get(product_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # This is a simplified version - in reality, you'd need specific selectors for each site
            details = {
                "description": "",
                "specifications": [],
                "additional_images": []
            }
            
            # Try to find description
            desc_selectors = [
                '[data-testid="product-description"]',
                '.product-description',
                '#product-description',
                '.description'
            ]
            
            for selector in desc_selectors:
                desc_elem = soup.select_one(selector)
                if desc_elem:
                    details["description"] = desc_elem.get_text(strip=True)
                    break
            
            return details
            
        except Exception as e:
            print(f"Failed to scrape product details: {e}")
            return {"description": "", "specifications": [], "additional_images": []}