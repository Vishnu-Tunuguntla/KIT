import json
import pprint
from langchain_community.document_loaders import BraveSearchLoader
from langchain_openai import ChatOpenAI
from langchain.chains import create_extraction_chain
from langchain_text_splitters import RecursiveCharacterTextSplitter
import requests
from bs4 import BeautifulSoup

# Set the Brave Search API key and initialize the ChatOpenAI language model
api_key = "BSAx-Fuzc3WKsXGCTwflO4SkRbf6AwU"
llm = ChatOpenAI(temperature=0, model="gpt-4")

# Set OPENAI_API_KEY environment variable for langchain to use OpenAI API

# Define the schema for the nutrition information extraction
schema = {
    "properties": {
        "product_name": {"type": "string"},
        "serving_size": {"type": "string"},
        "calories": {"type": "integer"},
        "total_fat": {"type": "object", "properties": {"amount": {"type": "number"}, "unit": {"type": "string"}}},
        "protein": {"type": "object", "properties": {"amount": {"type": "number"}, "unit": {"type": "string"}}},
        "carbohydrates": {"type": "object", "properties": {"amount": {"type": "number"}, "unit": {"type": "string"}}},
        "sugar": {"type": "object", "properties": {"amount": {"type": "number"}, "unit": {"type": "string"}}},
        "sodium": {"type": "object", "properties": {"amount": {"type": "number"}, "unit": {"type": "string"}}},
    },
    "required": ["product_name", "serving_size", "calories"],
}

# Function to extract information from content based on the provided schema
def extract(content: str, schema: dict):
    return create_extraction_chain(schema=schema, llm=llm).invoke(content)

# Function to scrape a webpage using BeautifulSoup and extract content
def scrape_with_beautifulsoup(url, schema, max_lines=10):
    # Send a GET request to the URL
    response = requests.get(url)

    # Create a BeautifulSoup object to parse the HTML content
    soup = BeautifulSoup(response.content, 'html.parser')

    # Extract the <body> tag from the parsed HTML
    body_content = soup.body.get_text(strip=True)

    print(f"Extracting content from {url}")

    # Split the content into chunks of 1000 tokens
    splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=1000, chunk_overlap=0
    )
    splits = splitter.split_text(body_content)

    # Check if splits is empty
    if not splits:
        print(f"No content found for {url}")
        return None

    # Extract information from the first split using the extract function and the provided schema
    extracted_content = extract(schema=schema, content=splits[0])

    # Check if the extracted content has too many lines
    if len(str(extracted_content).split("\n")) > max_lines:
        print(f"Extracted content has too many lines for {url}")
        return None

    # Remove the "input" field from the extracted content
    nutrition_info = extracted_content.get("text", [])
    if nutrition_info:
        return nutrition_info[0]
    else:
        return None

# Function to perform a search using Brave Search and scrape the top search results
def search_and_scrape(query, schema, num_results=8):
    # Load search results using BraveSearchLoader
    loader = BraveSearchLoader(
        query=query,
        api_key=api_key,
        search_kwargs={
            "count": num_results,
        }
    )
    search_results = loader.load()

    extracted_contents = []

    count = 0

    excluded_sources = ["none"]

    # Iterate over each search result
    for result in search_results:
        illegal_source = False
        # Extract the URL from the search result metadata
        url = result.metadata["link"]

        # Check if the URL contains any excluded sources
        for source in excluded_sources:
            if source in url:
                print(f"Excluding {source} from search results.")
                illegal_source = True
                break
        if illegal_source:
            continue

        # Scrape the webpage and extract content using scrape_with_beautifulsoup function
        try:
            extracted_content = scrape_with_beautifulsoup(url, schema)
        except Exception as e:
            print(f"An error occurred while scraping {url}: {e}")
            extracted_content = None

        # Check if extracted_content is not None before appending
        if extracted_content is not None:
            extracted_contents.append(extracted_content)
        if count >= 3:
            if extracted_contents:
                break

        count+=1

    # Check if extracted_contents is empty
    if not extracted_contents:
        print("No content extracted from the search results.")
        return None

    # Find the largest content based on the length of the extracted content
    largest_content = max(extracted_contents, key=lambda x: len(str(x)))

    return largest_content

# Function to create a JSON file with the extracted content
def create_json_file(product_name, extracted_content, output_file):
    # Create a dictionary with the schema properties
    json_data = {
        "product_name": product_name,
        "serving_size": extracted_content.get("serving_size", ""),
        "calories": extracted_content.get("calories", 0),
        "total_fat": f'{extracted_content.get("total_fat", {"amount": 0}).get("amount", 0)} {extracted_content.get("total_fat", {"unit": ""}).get("unit", "")}',
        "protein": f'{extracted_content.get("protein", {"amount": 0}).get("amount", 0)} {extracted_content.get("protein", {"unit": ""}).get("unit", "")}',
        "carbohydrates": f'{extracted_content.get("carbohydrates", {"amount": 0}).get("amount", 0)} {extracted_content.get("carbohydrates", {"unit": ""}).get("unit", "")}',
        "sugar": f'{extracted_content.get("sugar", {"amount": 0}).get("amount", 0)} {extracted_content.get("sugar", {"unit": ""}).get("unit", "")}',
        "sodium": f'{extracted_content.get("sodium", {"amount": 0}).get("amount", 0)} {extracted_content.get("sodium", {"unit": ""}).get("unit", "")}'
    }
    return json_data

def execute_search(brand_and_food_item):
    query = brand_and_food_item + " nutrition information"
    # Perform the search and scrape the top search results
    try:
        extracted_contents = search_and_scrape(query, schema)
    except Exception as e:
        print(f"An error occurred: {e}")
        extracted_contents = None

    # Create a JSON file with the extracted content
    if extracted_contents:
        json_data = create_json_file(brand_and_food_item, extracted_contents, "nutrition_info.json")
        return json_data
    else:
        print("No content extracted to create the JSON file.")
        return None

# Set the search query
# item = "Betty Crocker Original Bisquick Pancake & Baking Mix"

# print(execute_search(item))