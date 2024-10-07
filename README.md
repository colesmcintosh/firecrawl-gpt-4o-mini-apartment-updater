# Firecrawl GPT-4o-Mini Apartment Updater

Firecrawl GPT-4o-Mini Apartment Updater is an automated tool that scrapes apartment listings, analyzes them based on user preferences, and sends email notifications with the best matches.

## Features

- Web scraping of apartment listings from specified websites
- Data analysis using OpenAI's GPT-4o-mini to find the best apartment matches
- Email notifications with apartment recommendations

## Requirements

- Python 3.12
- FirecrawlApp API key
- OpenAI API key
- Gmail account for sending emails

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/colesmcintosh/firecrawl-gpt-4o-mini-apartment-updater.git
   cd firecrawl-gpt-4o-mini-apartment-updater
   ```

2. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

3. Set up your environment variables in a `.env` file:
   ```
   FIRECRAWL_API_KEY=your_firecrawl_api_key
   OPENAI_API_KEY=your_openai_api_key
   GMAIL_EMAIL=your_gmail_email
   GMAIL_PASSWORD=your_gmail_app_password
   RECIPIENT1_EMAIL=recipient1@example.com
   RECIPIENT2_EMAIL=recipient2@example.com
   WEBSITE_URL=your_website_url
   WEBSITE_DETAIL_URL=your_website_detail_url
   SPECIFICATIONS=your_specifications
   ```

## Usage

Run the main script to start the apartment finding process:

```
python main.py
```