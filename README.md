# Google Maps Scraper

This is a simple Google Maps scraper that allows you to extract information about businesses in a specific area. The scraper retrieves the name, address, phone number, website, rating, and reviews of businesses listed on Google Maps.

## Features

- Extract business information from Google Maps
- Save the extracted data in a structured format into a CSV file

## Usage

1. Clone the repository:

```bash
    git clone https://github.com/bate-kamorou/simple_google_maps_scraper.git
    cd simple_google_maps_scraper
```

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. Run the scraper:

```bash
    python scraper.py <query>  <output> 
```

## Parameters

- `query`: The search query for finding businesses (e.g., "solar installer Amsterdam").
- `output`: The name of the CSV file to save the extracted data (e.g., "businesses_leads.csv").

## Output

The scraper will create a CSV file named `businesses_leads.csv` containing the extracted information about the businesses. The CSV file will have the following columns:

- Name
- Address
- Phone Number
- Website
- Rating
- Reviews