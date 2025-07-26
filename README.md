
# Globbal Search Engine

A custom search engine built with Flask that allows users to search through indexed web content with keyword-based scoring.

## Features

- **Web Search Interface**: Clean, simple search interface with a custom design
- **Keyword-Based Scoring**: Advanced search algorithm that weights keywords and phrases
- **Web Crawler**: Automated web crawling system using Selenium
- **Database Storage**: SQLAlchemy-based data persistence with PostgreSQL support
- **Responsive Design**: Mobile-friendly interface with custom CSS styling

## Architecture

### Core Components

- **Flask Web Server** (`main.py`): Handles search requests and serves the web interface
- **Database Layer** (`db.py`, `model.py`): SQLAlchemy ORM with transaction management
- **Web Crawler** (`crawler/`): Selenium-based crawler for indexing web content
- **Search Algorithm**: Keyword matching with weighted scoring system

### Database Schema

- **URLs Table**: Stores indexed webpage URLs and titles
- **Keywords Table**: Stores extracted keywords with weights for each URL

## Setup and Installation

### Prerequisites

- Python 3.11+
- PostgreSQL database
- Chrome/Chromium browser (for crawling)

### Environment Variables

Set the following environment variable:

```bash
DATABASE_URL=postgresql://username:password@host:port/database
```

### Running the Application

1. Install dependencies (handled automatically by Replit)
2. Set up your database URL in the environment
3. Run the application:

```bash
python main.py
```

The server will start on `http://0.0.0.0:8080`

## Usage

### Searching

1. Navigate to the homepage
2. Enter your search query in the search box
3. Results are ranked by keyword relevance and weight

### API Endpoints

- `GET /` - Homepage with search interface
- `GET /search?q=<query>` - HTML search results page
- `GET /query/<text>` - JSON API for search results
- `GET /jsonstuff/<text>` - Legacy JSON search endpoint

## Web Crawler

The crawler system (`crawler/`) uses Selenium to:

- Automatically discover and index web pages
- Extract keywords and phrases from page content
- Calculate relevance weights for search terms
- Store indexed data in the database

### Running the Crawler

```bash
python -m crawler
```

## Search Algorithm

The search system uses a multi-layered approach:

1. **Keyword Extraction**: Identifies relevant terms from web content
2. **Weight Calculation**: Assigns importance scores to keywords
3. **Query Matching**: Matches user queries against indexed keywords
4. **Result Ranking**: Orders results by cumulative keyword weights

## Development

### Database Transactions

The project uses a custom `@db_transaction` decorator for safe database operations:

```python
@db.db_transaction
def my_function(session=None):
    # Database operations here
    pass
```

### Adding New Features

1. Database changes: Modify `model.py` for schema updates
2. Search logic: Update the query functions in `main.py`
3. UI changes: Edit templates in `templates/` and styles in `static/style.css`

## File Structure

```
├── main.py              # Flask application and search endpoints
├── db.py                # Database connection and transaction management
├── model.py             # SQLAlchemy models (URLs, Keywords)
├── links.json           # Static link data for testing
├── crawler/             # Web crawling system
│   ├── __main__.py      # Main crawler logic
│   └── funnyevals.py    # Crawled data storage
├── templates/           # HTML templates
│   ├── index.html       # Homepage
│   └── searchtemplate.html # Search results page
└── static/              # Static assets
    ├── style.css        # Custom styling
    └── globbal.png      # Logo
```

## Deployment

This project is designed to run on Replit with automatic dependency management and deployment capabilities.

## License

This project is open source and available under standard terms.
