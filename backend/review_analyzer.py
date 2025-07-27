import requests
import random
from typing import Dict, List
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob
import re

class ReviewAnalyzer:
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
    
    def analyze_product_reviews(self, product: Dict) -> Dict:
        """Analyze reviews for a product and return sentiment summary"""
        
        # For demo purposes, we'll generate mock review data
        # In a real implementation, you'd scrape actual reviews
        mock_reviews = self._generate_mock_reviews(product)
        
        return self._analyze_reviews(mock_reviews)
    
    def _generate_mock_reviews(self, product: Dict) -> List[str]:
        """Generate realistic mock reviews based on product info"""
        
        product_title = product.get("title", "").lower()
        rating = product.get("rating", 4.0)
        
        # Generate reviews based on rating
        positive_reviews = []
        negative_reviews = []
        
        # Positive review templates
        positive_templates = [
            "Great quality! Exactly what I was looking for.",
            "Excellent value for money. Highly recommend!",
            "Perfect fit and finish. Very satisfied with this purchase.",
            "Fast shipping and great product. Will buy again.",
            "Sturdy build quality and works as expected.",
            "Love the design and functionality. 5 stars!",
            "Best purchase I've made in a while. Worth every penny.",
            "Exceeded my expectations. Great customer service too.",
            "High quality materials and excellent craftsmanship.",
            "Perfect for my needs. Great product overall."
        ]
        
        # Negative review templates
        negative_templates = [
            "Poor quality materials. Broke after a few uses.",
            "Not as described. Disappointed with this purchase.",
            "Overpriced for what you get. Look elsewhere.",
            "Cheap construction. Would not recommend.",
            "Arrived damaged and customer service was unhelpful.",
            "Doesn't work as advertised. Waste of money.",
            "Poor build quality. Expected much better.",
            "Misleading product description. Not worth it.",
            "Broke within a week of normal use.",
            "Terrible experience. Save your money."
        ]
        
        # Generate reviews based on rating
        num_reviews = random.randint(10, 30)
        reviews = []
        
        for _ in range(num_reviews):
            # Probability of positive review based on rating
            positive_prob = rating / 5.0
            
            if random.random() < positive_prob:
                review = random.choice(positive_templates)
                # Add product-specific details
                if "wallet" in product_title:
                    review += " The leather feels premium and the card slots are perfect."
                elif "mouse" in product_title:
                    review += " Great DPI settings and comfortable grip."
                elif "headphones" in product_title:
                    review += " Amazing sound quality and comfortable fit."
                reviews.append(review)
            else:
                review = random.choice(negative_templates)
                # Add product-specific complaints
                if "wallet" in product_title:
                    review += " The leather started peeling after a month."
                elif "mouse" in product_title:
                    review += " The buttons feel mushy and tracking is inconsistent."
                elif "headphones" in product_title:
                    review += " Uncomfortable after wearing for more than an hour."
                reviews.append(review)
        
        return reviews
    
    def _analyze_reviews(self, reviews: List[str]) -> Dict:
        """Analyze sentiment and extract insights from reviews"""
        
        if not reviews:
            return {
                "review_score": 0.5,
                "good_reviews": "No reviews available",
                "bad_reviews": "No reviews available",
                "purchases": 0
            }
        
        # Analyze sentiment for each review
        sentiments = []
        positive_reviews = []
        negative_reviews = []
        
        for review in reviews:
            # Use VADER for sentiment analysis
            vader_score = self.vader_analyzer.polarity_scores(review)
            
            # Use TextBlob as secondary analysis
            blob = TextBlob(review)
            textblob_score = blob.sentiment.polarity
            
            # Combine scores (weighted average)
            combined_score = (vader_score['compound'] * 0.7) + (textblob_score * 0.3)
            sentiments.append(combined_score)
            
            # Categorize reviews
            if combined_score > 0.1:
                positive_reviews.append(review)
            elif combined_score < -0.1:
                negative_reviews.append(review)
        
        # Calculate overall review score
        avg_sentiment = sum(sentiments) / len(sentiments) if sentiments else 0
        review_score = (avg_sentiment + 1) / 2  # Normalize to 0-1 range
        
        # Summarize positive and negative aspects
        good_summary = self._summarize_positive_reviews(positive_reviews)
        bad_summary = self._summarize_negative_reviews(negative_reviews)
        
        # Estimate purchases based on review count and sentiment
        purchases = len(reviews) * random.randint(10, 50)
        
        return {
            "review_score": round(review_score, 2),
            "good_reviews": good_summary,
            "bad_reviews": bad_summary,
            "purchases": purchases
        }
    
    def _summarize_positive_reviews(self, reviews: List[str]) -> str:
        """Summarize positive aspects from reviews"""
        if not reviews:
            return "No positive reviews found"
        
        # Extract common positive keywords
        positive_keywords = []
        common_phrases = [
            "great quality", "excellent", "perfect", "love", "amazing",
            "highly recommend", "worth", "satisfied", "exceeded expectations",
            "fast shipping", "good value", "sturdy", "comfortable"
        ]
        
        found_phrases = []
        for review in reviews:
            review_lower = review.lower()
            for phrase in common_phrases:
                if phrase in review_lower and phrase not in found_phrases:
                    found_phrases.append(phrase)
        
        if found_phrases:
            summary = f"Customers praise the {', '.join(found_phrases[:3])}."
        else:
            summary = "Customers generally report positive experiences."
        
        # Add specific details
        sample_review = reviews[0] if reviews else ""
        if "leather" in sample_review.lower():
            summary += " Premium materials noted."
        if "shipping" in sample_review.lower():
            summary += " Fast delivery appreciated."
        
        return summary
    
    def _summarize_negative_reviews(self, reviews: List[str]) -> str:
        """Summarize negative aspects from reviews"""
        if not reviews:
            return "No significant negative feedback"
        
        # Extract common negative keywords
        negative_phrases = [
            "poor quality", "broke", "disappointed", "not as described",
            "overpriced", "cheap", "waste of money", "poor build",
            "arrived damaged", "doesn't work", "uncomfortable"
        ]
        
        found_issues = []
        for review in reviews:
            review_lower = review.lower()
            for phrase in negative_phrases:
                if phrase in review_lower and phrase not in found_issues:
                    found_issues.append(phrase)
        
        if found_issues:
            summary = f"Some customers reported issues with {', '.join(found_issues[:2])}."
        else:
            summary = "Minor complaints about quality and durability."
        
        # Add specific concerns
        sample_review = reviews[0] if reviews else ""
        if "broke" in sample_review.lower():
            summary += " Durability concerns mentioned."
        if "price" in sample_review.lower():
            summary += " Value for money questioned."
        
        return summary
    
    def scrape_amazon_reviews(self, product_url: str) -> List[str]:
        """Scrape reviews from Amazon product page"""
        # This is a placeholder for actual review scraping
        # In practice, you'd need to handle Amazon's anti-bot measures
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            # Note: This is simplified and may not work with actual Amazon pages
            # You'd need to implement proper scraping with appropriate delays and proxies
            response = requests.get(product_url, headers=headers)
            
            if response.status_code == 200:
                # Parse reviews from HTML (simplified)
                # In reality, you'd use BeautifulSoup to extract review text
                return ["Sample scraped review text"]
            else:
                return []
                
        except Exception as e:
            print(f"Failed to scrape reviews: {e}")
            return []
    
    def analyze_review_trends(self, reviews: List[str]) -> Dict:
        """Analyze trends in reviews over time"""
        # This could analyze sentiment changes, common complaint patterns, etc.
        trends = {
            "sentiment_trend": "stable",
            "common_issues": [],
            "improving_aspects": []
        }
        
        return trends