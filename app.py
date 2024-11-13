from firecrawl import FirecrawlApp
from pydantic import BaseModel
from typing import List
from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import json
import os
import requests

load_dotenv()

# Initialize the Firecrawl application with API key
app = FirecrawlApp(api_key=os.getenv('FIRECRAWL_API_KEY'))

# Define URL to scrape
url = "https://www.llv.li/en/national-administration/government-chancellery-unit/consultations/ongoing-consultations"

# Attempt to scrape the page content (without pageOptions)
try:
    page_content = app.scrape_url(url=url)
except requests.exceptions.HTTPError as e:
    print(f"Error during scraping: {e}")
    exit()

# Initialize OpenAI client
client = OpenAI()

# Define output fields
fields = ["Document", "deadline", "Responsibility"]

system_prompt = (
    "You are a helpful assistant. You receive a scraped webpage, and you extract the items and return them in valid JSON. "
    "Return a list with all fields. For 'Document' and 'Responsibility' include the URL as well."
)

user_prompt = f"""
  The extracted webpage: {page_content}
  The fields you return: {fields}
"""

# Extract data using OpenAI
try:
    completion = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        temperature=0,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    # Decode JSON data
    data = json.loads(completion.choices[0].message.content)
except Exception as e:
    print(f"Error with OpenAI completion: {e}")
    exit()

# Process and store the extracted items
items = []
keys = list(data.keys())
number_of_keys = len(keys)

if number_of_keys == 1:
    data = data[keys[0]]

for single_item in data:
    items.append(single_item)

# Save to Excel and CSV
df = pd.DataFrame(items)
df.to_excel("law.xlsx", index=False)
df.to_csv("law.csv", index=False)
