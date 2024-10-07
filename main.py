from firecrawl.firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from typing import List
from dotenv import load_dotenv
import os
import json
from openai import OpenAI
from loguru import logger
from pydantic import BaseModel
import Email  # Import our updated Email module

load_dotenv()
logger.info("Environment variables loaded.")

app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))
logger.info("FirecrawlApp initialized with API key.")

class ApartmentSchema(BaseModel):
    detail_number: str
    # Add other relevant fields based on apartment details

class ApartmentDetails(BaseModel):
    detail_number: str
    name: str
    price: float
    bedrooms: int
    bathrooms: int
    size_sqft: int
    availability: str
    floorplan_link: str  # New field for the floorplan link
    # Add other relevant fields based on apartment details

class TopApartmentsSchema(BaseModel):
    top_apartments: List[ApartmentDetails] = Field(..., max_items=5, description="Top 5 available apartments")

# Update the scrape URL to fetch latest apartments
data = app.scrape_url(os.getenv('WEBSITE_URL'), {
    'formats': ['extract'],
    'extract': {
        'schema': TopApartmentsSchema.model_json_schema()
    }
})
logger.info("Data scraped from URL.")

# Add floorplan links to the scraped data
for apartment in data['extract']['top_apartments']:
    apartment['floorplan_link'] = f"{os.getenv('WEBSITE_DETAIL_URL')}{apartment['detail_number']}"

# Pass details to OpenAI's GPT-4 for reasoning
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
logger.info("OpenAI client initialized.")

specifications = os.getenv('SPECIFICATIONS')

class ApartmentReportEmail(BaseModel):
    subject: str
    body: str

# Update the OpenAI call to include floorplan links in the analysis
response = openai.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system",
            "content": "You are an assistant that analyzes apartment details and provides a summary. Your response should be structured with a subject and a body. Include the floorplan links in your analysis."
        },
        {
            "role": "user",
            "content": f"Analyze the following apartment details and select the best options based on the following specifications. Include the floorplan links in your analysis:\nApartment details:\n{json.dumps(data['extract']['top_apartments'])}\nSpecifications: {specifications}"
        }
    ],
    response_format=ApartmentReportEmail,
)
logger.info("Received response from OpenAI.")

# Extract the structured output
result = response.choices[0].message.parsed

subject = result.subject
message_body = result.body

logger.success(f"Email subject: {subject}")
logger.success(f"Email body: {message_body}")

# Send emails using our updated Email module
try:
    recipient_emails = [os.getenv('RECIPIENT1_EMAIL'), os.getenv('RECIPIENT2_EMAIL')]
    Email.send_emails_sync(recipient_emails, subject, message_body)
    logger.info("Emails sent successfully.")
    print("Emails sent successfully.")
except Exception as e:
    logger.error(f"Failed to send emails: {str(e)}")
    print(f"Failed to send emails: {str(e)}")

logger.info("Script execution completed.")