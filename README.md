# ☕ Coffee RAG Chatbot
<img width="2752" height="1536" alt="RAG" src="https://github.com/user-attachments/assets/e2daa4ff-9133-4384-806a-28ad902aa5d5" />


A Retrieval-Augmented Generation (RAG) chatbot that combines web scraping and AI to answer questions about coffee products. This project demonstrates how to build an intelligent assistant that stays up-to-date with real-world data by scraping fresh information and making it queryable through natural language.

## 🎯 What Does It Do?

This project has two main components:

1. **Web Scraper**: Fetches the latest coffee product details from DAK Coffee Roasters using Scrapy + Zyte API
2. **RAG Pipeline**: Stores the data in a vector database (ChromaDB) and enables natural language queries powered by OpenAI's GPT-4

Ask questions like:
- "List all coffees with fruity notes"
- "Show me Ethiopian coffees grown above 1800 meters"
- "What coffees use the washed processing method?"
- "Recommend something with chocolate and caramel flavors"

The bot retrieves relevant context from the vector store and generates accurate, grounded responses.

## 🚀 Why This Project?

**AI models are constant, but the internet is ever-evolving.** LLMs have knowledge cutoff dates, but real-world product inventories, prices, and availability change daily. This project shows how to:

- Keep your LLM updated with fresh web data
- Handle JavaScript-heavy websites without complex selector maintenance
- Build semantic search over product catalogs
- Create practical RAG pipelines for real-world applications

This pattern works for any domain: e-commerce, real estate, restaurants, documentation, market research, etc.

## 📋 Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (fast Python package installer)
- [Zyte API](https://www.zyte.com/zyte-api/) account (for web scraping)
- [OpenAI API](https://platform.openai.com/) account (for embeddings and chat)

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/apscrapes/coffee-rag-chatbot.git
cd coffee-rag-chatbot
```

### 2. Install Dependencies

```bash
uv sync
```

This will create a virtual environment and install all required packages.

### 3. Configure API Keys

#### For the Scraper (Zyte API)

Edit `scraper/coffee_scraper/settings.py`:

```python
ZYTE_API_KEY = "YOUR_ZYTE_API_KEY_HERE"
```

Get your Zyte API key from: https://app.zyte.com/o/your-org/api-access

#### For the RAG Pipeline (OpenAI API)

Set your OpenAI API key as an environment variable:

```bash
export OPENAI_API_KEY="your-openai-api-key-here"
```

Or on Windows:
```cmd
set OPENAI_API_KEY=your-openai-api-key-here
```

Get your OpenAI API key from: https://platform.openai.com/api-keys

## 📖 Usage

### Step 1: Scrape Fresh Coffee Data

Navigate to the scraper directory and run the spider:

```bash
cd scraper
scrapy crawl dak_coffee -O ../data/coffee_data.json
```

**What this does:**
- Fetches the shop page from Coffee Roaster website
- Extracts product URLs for all coffees
- Visits each product page and extracts details using Zyte API's auto-extraction
- Saves everything to `data/coffee_data.json`

**Expected output:**
```
[scrapy.core.engine] INFO: Spider opened
[dak_coffee] INFO: Scraping shop page...
[dak_coffee] INFO: Found 24 coffee products
[scrapy.core.engine] INFO: Closing spider (finished)
```

The scraper will create a JSON file like:
```json
[
  {
    "product_url": "https://www.dakcoffeeroasters.com/shop/coffee/ethiopia-guji",
    "item_main": "Ethiopia Guji - Washed. Notes of bergamot, jasmine tea, and stone fruit. Grown at 1900-2100m..."
  }
]
```

### Step 2: Build the Vector Store & Chat

Open the Jupyter notebook:

```bash
cd ../rag-pipeline/notebook
jupyter notebook coffeebot_RAG_Pipeline.ipynb
```

Or use any notebook environment (VS Code, JupyterLab, etc.)

#### Run the cells in order:

**Cells 1-7: Setup**
- Load dependencies
- Read the JSON file
- Create LangChain documents
- Split into chunks
- Generate embeddings with OpenAI
- Create ChromaDB vector store

**Cell 8-11: Build RAG Chain**
- Initialize GPT-4 chat model
- Create retriever (fetches top 50 relevant chunks)
- Define system prompt
- Construct the RAG chain

**Cell 12: Interactive Chat**

Run this cell to start chatting:

```python
print("\n🤖 CoffeeBot ready. Type 'exit' to quit.\n")

while True:
    user_input = input("You: ").strip()
    
    if user_input.lower() in {"exit", "quit"}:
        print("CoffeeBot: Goodbye!")
        break
    
    response = rag_chain.invoke(user_input)
    print(f"CoffeeBot: {response}\n")
```

### Example Interactions

```
You: List all Ethiopian coffees
CoffeeBot: Here are all the Ethiopian coffees currently available:

1. Ethiopia Guji - Washed
   - Notes: bergamot, jasmine tea, stone fruit
   - Altitude: 1900-2100m
   - URL: https://www.dakcoffeeroasters.com/shop/coffee/ethiopia-guji

2. Ethiopia Yirgacheffe - Natural
   - Notes: blueberry, dark chocolate, wine-like
   - Altitude: 1800-2000m
   - URL: https://www.dakcoffeeroasters.com/shop/coffee/ethiopia-yirgacheffe
```

```
You: What coffees have chocolate notes?
CoffeeBot: Coffees with chocolate notes include:

1. Colombia Huila - Notes of milk chocolate, caramel, orange
2. Brazil Santos - Notes of dark chocolate, hazelnut, brown sugar
3. Ethiopia Yirgacheffe Natural - Notes of blueberry, dark chocolate...
```

```
You: Recommend something for espresso
CoffeeBot: For espresso, I recommend:

1. Espresso Blend - Specifically designed for espresso with balanced sweetness...
2. Brazil Santos - Works well for espresso with its chocolatey, nutty profile...
```

## 📁 Project Structure

```
coffee-rag-chatbot/
│
├── scraper/                          # Web scraping component
│   ├── coffee_scraper/
│   │   ├── spiders/
│   │   │   ├── dak_coffee.py        # Main spider (uses Zyte API auto-extraction)
│   │   │   └── manual-spider.py     # Alternative spider (manual XPath)
│   │   ├── settings.py              # Scrapy + Zyte API configuration
│   │   └── ...
│   └── scrapy.cfg
│
├── rag-pipeline/                     # RAG chatbot component
│   └── notebook/
│       └── coffeebot_RAG_Pipeline.ipynb  # Main notebook (embeddings + chat)
│
├── data/                             # Generated data (gitignored)
│   ├── coffee_data.json             # Scraped coffee data
│   └── vector_store/                # ChromaDB persistence
│
├── pyproject.toml                    # Python dependencies
└── README.md
```

## 🔧 Configuration Options

### Scraper Settings

In `scraper/coffee_scraper/settings.py`:

```python
# Rate limiting
CONCURRENT_REQUESTS_PER_DOMAIN = 1
DOWNLOAD_DELAY = 1

# Zyte API features
ZYTE_API_ENABLED = True
ZYTE_API_KEY = "YOUR_KEY"
```

### RAG Pipeline Settings

In the notebook:

```python
# Data paths
JSON_PATH = "../../data/coffee_data.json"
VECTOR_DB_DIRECTORY = "../../data/vector_store"

# Chunking strategy
chunk_size = 400
chunk_overlap = 0

# Retrieval settings
retriever = vector_store.as_retriever(search_kwargs={"k": 50})

# LLM model
chat_model = ChatOpenAI(
    model="gpt-4.1",
    temperature=0.3
)
```

## 💡 Key Features

### Zyte API Auto-Extraction

Instead of writing fragile CSS selectors:

```python
# ❌ Traditional approach - breaks when site changes
coffee_name = response.css('.product-title::text').get()
description = response.css('.product-desc p::text').getall()
price = response.css('.price span::text').get()
```

We use auto-extraction:

```python
# ✅ Zyte API approach - robust and LLM-ready
meta={
    "zyte_api": {
        "browserHtml": True,
        "pageContent": True,
        "pageContentOptions": {
            "extractFrom": "browserHtml"
        }
    }
}
```

Benefits:
- Handles JavaScript-heavy sites automatically
- No selector maintenance needed
- Returns structured, semantic content
- Perfect for feeding into LLMs

### Vector Search with Semantic Understanding

Traditional keyword search fails here:
```
Query: "coffees with fruity taste"
❌ No exact match for "fruity taste"
```

Vector search understands meaning:
```
Query: "coffees with fruity taste"
✅ Matches: "notes of strawberry", "citrus and berry", "tropical fruit flavors"
```

### Grounded Responses (No Hallucinations)

The system prompt explicitly prevents hallucinations:
```
"Use your knowledge to help user but don't invent any new information 
or add extra information which is not available in the context."
```

Result: The bot only recommends coffees that actually exist in the scraped data.

## 🔄 Keeping Data Fresh

To update the bot with latest products:

```bash
# Re-run the scraper
cd scraper
scrapy crawl dak_coffee -O ../data/coffee_data.json

# Re-run vector store creation cells in the notebook
# (Cells 1-7)
```

For production, schedule this with cron (Linux/Mac):
```bash
0 */6 * * * cd /path/to/project/scraper && scrapy crawl dak_coffee -O ../data/coffee_data.json
```

Or Windows Task Scheduler for automated updates.

## 🐛 Troubleshooting

### "No module named 'scrapy_zyte_api'"

```bash
uv pip install scrapy-zyte-api
```

### "ZYTE_API_KEY not set"

Make sure you've added your API key to `scraper/coffee_scraper/settings.py`:
```python
ZYTE_API_KEY = "your-actual-key-here"
```

### "OpenAI API key not found"

Set the environment variable before running the notebook:
```bash
export OPENAI_API_KEY="sk-..."
```

### Vector store errors

If you see ChromaDB errors, delete the vector store and recreate:
```bash
rm -rf data/vector_store/
```
Then re-run cells 1-7 in the notebook.

### Rate limiting errors

If Zyte API returns rate limit errors, increase the delay in `settings.py`:
```python
DOWNLOAD_DELAY = 3  # Increase from 1 to 3 seconds
```

## 🎓 Learning Resources

- [Scrapy Documentation](https://docs.scrapy.org/)
- [Zyte API Documentation](https://docs.zyte.com/zyte-api/get-started.html)
- [LangChain Documentation](https://python.langchain.com/docs/get_started/introduction)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [OpenAI API Documentation](https://platform.openai.com/docs/)

## 🚀 Extending This Project

Ideas for customization:

1. **Multi-source scraping**: Scrape from multiple coffee roasters
2. **Add filters**: Filter by price, roast level, bag size
3. **Image search**: Include product images in responses
4. **Preference learning**: Remember user preferences across sessions
5. **Comparison mode**: "Compare Ethiopia Guji vs. Colombia Huila"
6. **Price tracking**: Alert when coffees go on sale
7. **Brew recommendations**: Match coffees to brewing methods

The architecture is modular—scraping, storage, and generation are independent components you can swap or extend.

## 📝 Use Cases Beyond Coffee

This pattern works for:

- **E-commerce**: Product recommendation chatbots
- **Real estate**: Property search assistants
- **Restaurants**: Menu and location finders
- **Documentation**: Keep internal docs searchable
- **Market research**: Track competitor offerings
- **News aggregation**: Query latest articles by topic

Anywhere you need:
1. Fresh data from the web
2. Natural language queries
3. Accurate, grounded responses

## 📄 License

MIT License - feel free to use this project as a starting point for your own RAG applications.


**Happy scraping and chatting! ☕🤖**
