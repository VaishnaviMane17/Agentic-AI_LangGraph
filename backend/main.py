from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import uvicorn
from shopping_agent import ShoppingAgent
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Shopping Assistant API", version="1.0.0")

# CORS middleware to allow frontend connections
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the shopping agent
shopping_agent = ShoppingAgent()

class SearchRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    price_range: Optional[Dict[str, float]] = None
    features_to_add: Optional[List[str]] = None
    features_to_remove: Optional[List[str]] = None

class ProductResult(BaseModel):
    title: str
    price: str
    image_url: str
    product_url: str
    purchases: int
    good_reviews: str
    bad_reviews: str
    score: float
    reasoning: str

class SearchResponse(BaseModel):
    products: List[ProductResult]
    session_id: str
    query_processed: str
    suggestions: List[str]

@app.get("/")
async def root():
    return {"message": "AI Shopping Assistant API is running"}

@app.post("/search", response_model=SearchResponse)
async def search_products(request: SearchRequest):
    try:
        # Process the search request through LangGraph
        result = await shopping_agent.process_search(
            query=request.query,
            session_id=request.session_id,
            price_range=request.price_range,
            features_to_add=request.features_to_add,
            features_to_remove=request.features_to_remove
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/refine")
async def refine_search(request: SearchRequest):
    try:
        # Refine the existing search
        result = await shopping_agent.refine_search(
            query=request.query,
            session_id=request.session_id,
            price_range=request.price_range,
            features_to_add=request.features_to_add,
            features_to_remove=request.features_to_remove
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)