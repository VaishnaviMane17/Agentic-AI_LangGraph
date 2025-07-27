# AI-Powered Shopping Assistant

An intelligent shopping assistant built with LangGraph and React that helps users find the best products using natural language queries. The system analyzes product reviews, compares prices, and provides personalized recommendations through a conversational interface.

## Features

### LangGraph AI Agent
- **Natural Language Processing**: Understands shopping queries in plain English
- **Multi-step Workflow**: Uses LangGraph state machine for query parsing → product search → review analysis → ranking
- **Smart Product Matching**: Analyzes product features, prices, and customer reviews
- **Iterative Refinement**: Handles follow-up questions and search modifications
- **Session Memory**: Maintains conversation context for better recommendations

### Frontend Interface
- **Modern React/Next.js UI**: Clean, responsive design with Tailwind CSS
- **Chat Interface**: Conversational AI interaction on the left panel
- **Product Cards**: Detailed product information with review summaries
- **Refinement Panel**: Advanced filters for price, features, and preferences
- **Real-time Search**: Live product recommendations as you chat

### Review Analysis
- **Sentiment Analysis**: Uses VADER and TextBlob for review sentiment scoring
- **Smart Summarization**: Extracts positive and negative aspects from reviews
- **Purchase Insights**: Shows customer purchase patterns and ratings

## Technology Stack

### Backend
- **LangGraph**: State machine orchestration for AI workflow
- **LangChain**: LLM integration and prompt management
- **FastAPI**: REST API server
- **OpenAI GPT-4**: Natural language understanding
- **VADER Sentiment**: Review sentiment analysis
- **BeautifulSoup**: Web scraping for product data
- **SerpAPI**: Google Shopping integration (optional)

### Frontend
- **Next.js 14**: React framework with TypeScript
- **Tailwind CSS**: Utility-first styling
- **Heroicons**: Icon library
- **Axios**: HTTP client for API calls

## Project Structure

```
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── shopping_agent.py       # LangGraph workflow implementation
│   ├── product_search.py       # Product search and scraping
│   ├── review_analyzer.py      # Review analysis and sentiment
│   └── .env.example           # Environment variables template
├── frontend/
│   ├── src/
│   │   ├── components/        # React components
│   │   ├── pages/            # Next.js pages
│   │   ├── types/            # TypeScript definitions
│   │   ├── utils/            # API utilities
│   │   └── styles/           # CSS styles
│   ├── package.json
│   └── tailwind.config.js
├── requirements.txt           # Python dependencies
└── README.md
```

## Setup Instructions

### Backend Setup

1. **Install Python Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Run the Backend Server**
   ```bash
   cd backend
   python main.py
   ```
   
   The API will be available at `http://localhost:8000`

### Frontend Setup

1. **Install Node.js Dependencies**
   ```bash
   cd frontend
   npm install
   ```

2. **Run the Development Server**
   ```bash
   npm run dev
   ```
   
   The frontend will be available at `http://localhost:3000`

## Usage

### Basic Search
1. Open the application at `http://localhost:3000`
2. Enter a natural language query like: "I want a budget-friendly gaming mouse with RGB lighting"
3. Review the AI-powered product recommendations
4. Use the chat interface to refine your search

### Advanced Features
- **Refinement Panel**: Click "Refine Search" to set price ranges, add/remove features
- **Conversational Refinement**: Ask follow-up questions like "show me wireless options" or "under $50"
- **Review Analysis**: Each product shows summarized positive and negative reviews

## API Endpoints

### POST /search
Search for products based on natural language query.

**Request:**
```json
{
  "query": "leather wallet with RFID blocking",
  "price_range": {"min": 20, "max": 100},
  "features_to_add": ["wireless"],
  "features_to_remove": ["cheap"]
}
```

**Response:**
```json
{
  "products": [...],
  "session_id": "uuid",
  "query_processed": "wallet",
  "suggestions": ["Add brand preference", "Adjust price range"]
}
```

### POST /refine
Refine an existing search session.

## LangGraph Workflow

The AI agent follows this state machine:

1. **parse_query**: Extract product type, features, and constraints
2. **search_products**: Find relevant products using Google Shopping
3. **summarize_reviews**: Analyze customer reviews and sentiment
4. **return_results**: Rank and select top 3 products
5. **refine_search**: Handle iterative improvements

## Development Notes

### Mock Data
The system includes comprehensive mock data for development/testing when external APIs are not available.

### Review Analysis
- Uses VADER sentiment analysis for emotional tone
- TextBlob for additional sentiment validation
- Generates realistic review summaries based on product ratings

### Extensibility
- Easy to add new product sources
- Configurable scoring algorithms
- Modular component architecture

## Configuration

### Environment Variables
```bash
OPENAI_API_KEY=your_openai_api_key_here
SERPAPI_API_KEY=your_serpapi_key_here_optional
```

### Frontend Environment
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Implement your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.
