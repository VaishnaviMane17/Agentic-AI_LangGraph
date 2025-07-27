import os
import uuid
from typing import Dict, List, Optional, TypedDict, Annotated
from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage
from product_search import ProductSearcher
from review_analyzer import ReviewAnalyzer
import json

class ShoppingState(TypedDict):
    query: str
    session_id: str
    parsed_intent: Dict
    products: List[Dict]
    analyzed_products: List[Dict]
    final_results: List[Dict]
    price_range: Optional[Dict]
    features_to_add: Optional[List[str]]
    features_to_remove: Optional[List[str]]
    suggestions: List[str]
    error: Optional[str]

class ShoppingAgent:
    def __init__(self):
        self.llm = ChatOpenAI(
            model="gpt-4", 
            temperature=0.1,
            openai_api_key=os.getenv("OPENAI_API_KEY")
        )
        self.product_searcher = ProductSearcher()
        self.review_analyzer = ReviewAnalyzer()
        self.sessions = {}  # Store session memory
        
        # Build the LangGraph workflow
        self.workflow = self._build_workflow()
    
    def _build_workflow(self) -> StateGraph:
        """Build the LangGraph state machine workflow"""
        
        def parse_query(state: ShoppingState) -> ShoppingState:
            """Extract intent, product type, and features from input"""
            query = state["query"]
            
            system_prompt = """You are an expert at parsing shopping queries. 
            Extract the following information from the user's query:
            1. Product type (e.g., "wallet", "mouse", "headphones")
            2. Key features mentioned (e.g., "leather", "RGB", "wireless")
            3. Budget/price constraints if mentioned
            4. Brand preferences if any
            5. Use case or purpose
            
            Return your analysis as a JSON object with these fields:
            - product_type
            - features
            - price_constraint
            - brand_preference
            - use_case
            """
            
            try:
                response = self.llm.invoke([
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=f"Parse this shopping query: {query}")
                ])
                
                # Extract JSON from response
                parsed_intent = self._extract_json_from_response(response.content)
                state["parsed_intent"] = parsed_intent
                
            except Exception as e:
                state["error"] = f"Failed to parse query: {str(e)}"
                
            return state
        
        def search_products(state: ShoppingState) -> ShoppingState:
            """Search Google Shopping for relevant products"""
            if state.get("error"):
                return state
                
            try:
                parsed = state["parsed_intent"]
                products = self.product_searcher.search(
                    product_type=parsed.get("product_type", ""),
                    features=parsed.get("features", []),
                    price_range=state.get("price_range"),
                    max_results=10
                )
                state["products"] = products
                
            except Exception as e:
                state["error"] = f"Failed to search products: {str(e)}"
                
            return state
        
        def summarize_reviews(state: ShoppingState) -> ShoppingState:
            """Analyze reviews and sentiment for each product"""
            if state.get("error") or not state.get("products"):
                return state
                
            try:
                analyzed_products = []
                for product in state["products"]:
                    analysis = self.review_analyzer.analyze_product_reviews(product)
                    analyzed_products.append({
                        **product,
                        **analysis
                    })
                
                state["analyzed_products"] = analyzed_products
                
            except Exception as e:
                state["error"] = f"Failed to analyze reviews: {str(e)}"
                
            return state
        
        def return_results(state: ShoppingState) -> ShoppingState:
            """Select top 3 products based on similarity and review score"""
            if state.get("error") or not state.get("analyzed_products"):
                return state
                
            try:
                # Score and rank products
                scored_products = []
                query = state["query"]
                
                for product in state["analyzed_products"]:
                    score = self._calculate_product_score(product, query, state["parsed_intent"])
                    reasoning = self._generate_reasoning(product, score, state["parsed_intent"])
                    
                    scored_products.append({
                        **product,
                        "score": score,
                        "reasoning": reasoning
                    })
                
                # Sort by score and take top 3
                top_products = sorted(scored_products, key=lambda x: x["score"], reverse=True)[:3]
                state["final_results"] = top_products
                
                # Generate suggestions for refinement
                state["suggestions"] = self._generate_suggestions(state["parsed_intent"], top_products)
                
            except Exception as e:
                state["error"] = f"Failed to rank results: {str(e)}"
                
            return state
        
        def refine_search(state: ShoppingState) -> ShoppingState:
            """Handle search refinements"""
            # Modify the query based on refinement parameters
            if state.get("features_to_add"):
                for feature in state["features_to_add"]:
                    state["query"] += f" with {feature}"
            
            if state.get("features_to_remove"):
                # This is simplified - in a real implementation, you'd need more sophisticated query modification
                for feature in state["features_to_remove"]:
                    state["query"] = state["query"].replace(feature, "")
            
            # Reset processed data to rerun the pipeline
            state["parsed_intent"] = {}
            state["products"] = []
            state["analyzed_products"] = []
            state["final_results"] = []
            
            return state
        
        # Build the graph
        workflow = StateGraph(ShoppingState)
        
        # Add nodes
        workflow.add_node("parse_query", parse_query)
        workflow.add_node("search_products", search_products)  
        workflow.add_node("summarize_reviews", summarize_reviews)
        workflow.add_node("return_results", return_results)
        workflow.add_node("refine_search", refine_search)
        
        # Add edges
        workflow.add_edge("parse_query", "search_products")
        workflow.add_edge("search_products", "summarize_reviews")
        workflow.add_edge("summarize_reviews", "return_results")
        workflow.add_edge("return_results", END)
        workflow.add_edge("refine_search", "parse_query")
        
        # Set entry point
        workflow.set_entry_point("parse_query")
        
        return workflow.compile()
    
    def _extract_json_from_response(self, response: str) -> Dict:
        """Extract JSON from LLM response"""
        try:
            # Find JSON in the response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start != -1 and end != 0:
                json_str = response[start:end]
                return json.loads(json_str)
        except:
            pass
        
        # Fallback to structured parsing
        return {
            "product_type": "unknown",
            "features": [],
            "price_constraint": None,
            "brand_preference": None,
            "use_case": "general"
        }
    
    def _calculate_product_score(self, product: Dict, query: str, parsed_intent: Dict) -> float:
        """Calculate relevance score for a product"""
        score = 0.0
        
        # Base score from review sentiment
        score += product.get("review_score", 0) * 0.4
        
        # Price score (lower price = higher score, within reason)
        price = product.get("price_numeric", 0)
        if price > 0:
            # Normalize price score (this is simplified)
            price_score = max(0, 1 - (price / 1000))  # Assume $1000 as high price
            score += price_score * 0.2
        
        # Feature matching score
        features = parsed_intent.get("features", [])
        title = product.get("title", "").lower()
        feature_matches = sum(1 for feature in features if feature.lower() in title)
        if features:
            score += (feature_matches / len(features)) * 0.3
        
        # Purchase count score (normalized)
        purchases = product.get("purchases", 0)
        if purchases > 0:
            purchase_score = min(1.0, purchases / 1000)  # Normalize to 1000 purchases
            score += purchase_score * 0.1
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _generate_reasoning(self, product: Dict, score: float, parsed_intent: Dict) -> str:
        """Generate explanation for why this product was selected"""
        reasons = []
        
        if score > 0.8:
            reasons.append("Excellent match for your requirements")
        elif score > 0.6:
            reasons.append("Good match with minor trade-offs")
        else:
            reasons.append("Decent option but may not meet all criteria")
        
        if product.get("review_score", 0) > 0.7:
            reasons.append("highly rated by customers")
        
        if product.get("purchases", 0) > 100:
            reasons.append("popular choice with many purchases")
        
        return ". ".join(reasons) + "."
    
    def _generate_suggestions(self, parsed_intent: Dict, products: List[Dict]) -> List[str]:
        """Generate suggestions for search refinement"""
        suggestions = [
            "Adjust price range",
            "Add specific brand preference",
            "Include additional features",
            "Focus on higher-rated products"
        ]
        
        # Add context-specific suggestions
        if parsed_intent.get("product_type"):
            suggestions.append(f"Search for different {parsed_intent['product_type']} styles")
        
        return suggestions[:3]  # Return top 3 suggestions
    
    async def process_search(self, query: str, session_id: Optional[str] = None, 
                           price_range: Optional[Dict] = None,
                           features_to_add: Optional[List[str]] = None,
                           features_to_remove: Optional[List[str]] = None) -> Dict:
        """Process a new search request"""
        
        if not session_id:
            session_id = str(uuid.uuid4())
        
        # Initialize state
        initial_state = ShoppingState(
            query=query,
            session_id=session_id,
            parsed_intent={},
            products=[],
            analyzed_products=[],
            final_results=[],
            price_range=price_range,
            features_to_add=features_to_add,
            features_to_remove=features_to_remove,
            suggestions=[],
            error=None
        )
        
        # Run the workflow
        result = self.workflow.invoke(initial_state)
        
        # Store session for future refinements
        self.sessions[session_id] = result
        
        # Format response
        return {
            "products": [self._format_product_result(p) for p in result.get("final_results", [])],
            "session_id": session_id,
            "query_processed": result.get("parsed_intent", {}).get("product_type", query),
            "suggestions": result.get("suggestions", [])
        }
    
    async def refine_search(self, query: str, session_id: str,
                          price_range: Optional[Dict] = None,
                          features_to_add: Optional[List[str]] = None,
                          features_to_remove: Optional[List[str]] = None) -> Dict:
        """Refine an existing search"""
        
        if session_id not in self.sessions:
            # If no session found, treat as new search
            return await self.process_search(query, session_id, price_range, features_to_add, features_to_remove)
        
        # Get previous state and modify it
        state = self.sessions[session_id].copy()
        state["query"] = query
        state["price_range"] = price_range
        state["features_to_add"] = features_to_add
        state["features_to_remove"] = features_to_remove
        
        # Run refinement
        refined_state = self.workflow.invoke(state, {"start": "refine_search"})
        
        # Update session
        self.sessions[session_id] = refined_state
        
        return {
            "products": [self._format_product_result(p) for p in refined_state.get("final_results", [])],
            "session_id": session_id,
            "query_processed": refined_state.get("parsed_intent", {}).get("product_type", query),
            "suggestions": refined_state.get("suggestions", [])
        }
    
    def _format_product_result(self, product: Dict) -> Dict:
        """Format product for API response"""
        return {
            "title": product.get("title", ""),
            "price": product.get("price", ""),
            "image_url": product.get("image_url", ""),
            "product_url": product.get("product_url", ""),
            "purchases": product.get("purchases", 0),
            "good_reviews": product.get("good_reviews", ""),
            "bad_reviews": product.get("bad_reviews", ""),
            "score": round(product.get("score", 0), 2),
            "reasoning": product.get("reasoning", "")
        }