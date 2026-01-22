# coffee-rag-chatbot

## Usage

1. Clone the repo and setup python environment using uv
```
uv sync
```

2. Run the Scraper to get fresh data, first add ZYTE_API_KEY = "XXXX" in settings.py
```
cd scraper
scrapy crawl dak_coffee -O ../data/coffee_data.json
```
Note : Add ZYTE_API_KEY

3. Setup RAG pipeline
```
cd rag-pipeline
```
Note : Add OPENAI_API_KEY to environment or within notebook

4. Execute the notebook for Inferencing: 
```
/notebook/coffeebot_RAG_Pipeline.ipynb
```