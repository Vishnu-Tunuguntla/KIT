import pprint
from langchain_community.document_loaders import BraveSearchLoader
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import AsyncChromiumLoader
from langchain_community.document_transformers import BeautifulSoupTransformer

# Set the Brave Search API key and initialize the ChatOpenAI language model
api_key = "BSAx-Fuzc3WKsXGCTwflO4SkRbf6AwU"
llm = ChatOpenAI(temperature=0, model="gpt-4")

#Set OPEN_AI_API_KEY environment variable for langchain to use OpenAI API

# Define the schema for the nutrition information extraction
schema = {
    "properties": {
        "product_name": {"type": "string"},
        "serving_size": {"type": "string"},
        "calories": {"type": "integer"},
        "total_fat": {"type": "object", "properties": {"amount": {"type": "number"}, "unit": {"type": "string"}}},
        "protein": {"type": "object", "properties": {"amount": {"type": "number"}, "unit": {"type": "string"}}},
        "carbohydrates": {"type": "object", "properties": {"amount": {"type": "number"}, "unit": {"type": "string"}}},
    },
    "required": ["product_name", "serving_size", "calories"],
}

# Function to extract information from content based on the provided schema
def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).run(content)

# Function to scrape a webpage using Playwright and extract content
def scrape_with_playwright(url, schema):
    # Load the webpage using AsyncChromiumLoader
    loader = AsyncChromiumLoader([url])
    doc = loader.load()[0]
    
    # Transform the loaded document using BeautifulSoupTransformer to extract the <body> tag
    bs_transformer = BeautifulSoupTransformer()
    doc_transformed = bs_transformer.transform_documents([doc], tags_to_extract=["body"])[0]
    
    print(f"Extracting content from {url}")
    
    # Split the transformed document into chunks of 1000 tokens
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_documents([doc_transformed])
    
    # Extract information from the first split using the extract function and the provided schema
    extracted_content = extract(schema=schema, content=splits[0].page_content)
    
    # Print the extracted content
    #pprint.pprint(extracted_content)
    
    return extracted_content

# Function to perform a search using Brave Search and scrape the top search results
def search_and_scrape(query, schema, num_results=3):
    # Load search results using BraveSearchLoader
    loader = BraveSearchLoader(
        query=query,
        api_key=api_key,
        search_kwargs={"count": num_results}
    )
    search_results = loader.load()
    
    extracted_contents = []
    
    # Iterate over each search result
    for result in search_results:
        # Extract the URL from the search result metadata
        url = result.metadata["link"]
        
        # Scrape the webpage and extract content using scrape_with_playwright function
        extracted_content = scrape_with_playwright(url, schema)
        extracted_contents.append(extracted_content)
    
    # Find the largest content based on the length of the extracted content
    largest_content = max(extracted_contents, key=lambda x: len(str(x)))
    return largest_content
    
    #return extracted_contents

# Set the search query
query = "Barebells Salty Peanut Protein Bar Nutrition Information"

# Perform the search and scrape the top search results
extracted_contents = search_and_scrape(query, schema)
pprint.pprint(extracted_contents)