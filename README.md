# Google Maps Scraper

A powerful automated web scraper that extracts detailed business information from Google Maps. This tool uses Selenium to simulate user interactions with Google Maps and collects structured data about businesses including contact information, ratings, and reviews.

## 📋 Overview

This project automates the process of gathering business intelligence from Google Maps by:

1. Searching for specific business types in designated locations
2. Navigating through search results using automated browser interactions
3. Extracting detailed business information from individual listings
4. Storing data in multiple formats (CSV and JSON)
5. Tracking progress to handle interrupted or failed scraping sessions

## 🎯 What It Does

The scraper performs the following workflow:

1. **Search Execution**: Launches a Chrome browser and navigates to Google Maps
2. **Query Processing**: Enters your search query (e.g., "solar installer Antwerp")
3. **Result Collection**: Scrolls through search results to load business listings
4. **Link Extraction**: Collects direct links to each business listing
5. **Data Extraction**: For each business, extracts:
   - Company Name
   - Phone Number
   - Address
   - Website URL (cleaned and normalized)
   - Rating
   - Review Count
   - Google Maps Link
6. **Data Storage**: Saves extracted data to CSV or JSON format
7. **Progress Tracking**: Maintains a progress log to resume from interruptions
8. **Duplicate Removal**: Automatically removes duplicate entries by company name

## 🔧 How It Works

### Architecture

``` code
main.py (Entry Point)
    ↓
    Uses multiprocessing to manage multiple queries
    ↓
Business_scraper() (Selenium-based scraper)
    ↓
    1. Opens Chrome browser
    2. Navigates to Google Maps
    3. Searches for businesses
    4. Scrolls to load more results
    5. Collects business links
    6. Extracts data from each listing
    ↓
Tracker (Progress Management)
    ↓
    Saves completed queries to progress.json
    ↓
Output Files (CSV or JSON)
```

### Key Components

#### `main.py`

- **Purpose**: Main entry point that orchestrates the scraping process
- **Functionality**:
  - Defines industries and cities to search
  - Creates query combinations (e.g., "solar installer Antwerp")
  - Uses multiprocessing to run scraper jobs
  - Loads progress from previous runs
  - Re-runs any failed or incomplete queries

#### `scraper.py`

- **Purpose**: Core Selenium-based web scraper
- **Functionality**:
  - `Business_scraper()`: Main scraping function
  - Uses Selenium WebDriver to control Chrome browser
  - Implements explicit waits for reliable element detection
  - Scrolls through results to load multiple business listings
  - Extracts data using XPath and CSS selectors
  - Handles errors gracefully with retry logic
  - Cleans and normalizes extracted data
  - Saves output to CSV/JSON format

#### `tracker.py`

- **Purpose**: Manages progress tracking and recovery
- **Key Functions**:
  - `save_progress()`: Stores completed queries to JSON
  - `load_progress()`: Retrieves completed queries
  - `mark_done()`: Marks a query as completed
  - Uses `progress.json` to enable resuming interrupted scraping

#### `retry_missing.py`

- **Purpose**: Utility for reprocessing incomplete records
- **Functionality**:
  - Identifies records with missing phone numbers
  - Creates a `missing_phone.csv` file for re-scraping
  - Supports both CSV and JSON input files

## 📦 Features

- ✅ **Multi-query Scraping**: Process multiple search terms and locations
- ✅ **Multiprocessing Support**: Parallelize scraping tasks
- ✅ **Progress Tracking**: Resume from interruptions with `progress.json`
- ✅ **Robust Data Extraction**: Uses explicit waits and retry logic
- ✅ **Human-like Behavior**: Random delays and human-like interactions
- ✅ **Duplicate Removal**: Automatically removes duplicate entries
- ✅ **Multiple Export Formats**: Save as CSV or JSON
- ✅ **Error Logging**: Logs errors to `logs/errors.txt`
- ✅ **Data Validation**: Cleans URLs and normalizes data
- ✅ **Flexible Configuration**: Easy to modify search parameters

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- Google Chrome browser installed
- ChromeDriver (auto-managed by selenium if available)

### Setup Steps

1. **Clone the repository**:

```bash
git clone https://github.com/bate-kamorou/google_maps_scraper.git
cd google_maps_scraper
```

2. **Create a virtual environment** (optional but recommended):

```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

3. **Install dependencies**:

```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Usage

1. **Configure Search Parameters** in `main.py`:

```python
industries = [
    "solar installer",
    "roofing contractor",
    "construction company"
]

cities = [
    "Amsterdam",
    "Rotterdam",
    "Antwerp"
]
```

2. **Run the Scraper**:

```bash
python main.py
```

### Direct Scraper Usage

```bash
python scraper.py "solar installer Amsterdam" csv
```

### Retry Missing Data

```bash
python retry_missing.py output/solar_installer_Amsterdam.csv
```

## 📊 Output Format

### CSV Output

The scraper creates CSV files in the `output/` directory with the following columns:

| Column | Description |
|--------|-------------|
| company_name | Business name |
| phone | Contact phone number |
| address | Business address |
| rating | Google Maps rating (1-5 stars) |
| review | Number of reviews |
| website | Business website URL |
| google_maps_link | Direct link to Google Maps listing |

### JSON Output

Same data structure as CSV, formatted as JSON array of objects.

### Example CSV Row

``` code
company_name,phone,address,rating,review,website,google_maps_link
Solar Plus Amsterdam,+31 20 123 4567,123 Main St Amsterdam,4.8,156,https://solarplus.nl,https://www.google.com/maps/place/Solar+Plus...
```

## 📁 Project Structure

``` code
google-maps-scraper/
├── main.py                    # Entry point and query orchestration
├── scraper.py                 # Core Selenium scraper logic
├── tracker.py                 # Progress tracking utilities
├── retry_missing.py           # Utility for reprocessing records
├── requirements.txt           # Python dependencies
├── progress.json              # Tracks completed queries
├── README.md                  # This file
│
├── logs/
│   └── errors.txt             # Error log file
│
└── output/                    # Generated output files
    ├── solar_installer_Antwerp.csv
    ├── roofing_contractor_Antwerp.csv
    └── ...
```

## 🔧 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| selenium | 4.41.0 | Browser automation |
| pandas | 3.0.1 | Data manipulation and export |
| python-dateutil | 2.9.0 | Date handling |
| certifi | 2026.2.25 | SSL certificates |
| pycparser | 3.0 | C parser |

## ⚙️ Configuration Options

### In `main.py`

- **`industries`**: List of business types to search for
- **`cities`**: List of locations to search in
- **`Pool(n)`**: Number of parallel processes (currently set to 1 for stability)

### In `scraper.py`

- **`output_format`**: Choose "csv" or "json" for output
- **Retry logic**: `retries=3` parameter in `save_loading_and_extraction()`
- **Timeout values**: Adjustable in `WebDriverWait()` calls

## 🛡️ Error Handling

The scraper includes multiple error handling mechanisms:

1. **Explicit Waits**: Uses WebDriverWait instead of hardcoded sleep times
2. **Retry Logic**: Retries failed element extraction up to 3 times
3. **Try-Catch Blocks**: Gracefully handles missing elements
4. **Random Delays**: Varies sleep times to simulate human behavior
5. **Progress Tracking**: Saves progress to resume after failures
6. **Error Logging**: Stores errors in `logs/errors.txt`

## 💡 Tips & Best Practices

1. **Start Small**: Test with one industry-city combination before bulk scraping
2. **Monitor Progress**: Check `progress.json` to track completion
3. **Adjust Delays**: Increase sleep times if getting rate-limited
4. **Chrome Compatibility**: Ensure Chrome version matches ChromeDriver
5. **Network Stability**: Run on stable connection for reliable scraping
6. **Data Validation**: Review output for accuracy before processing

## ⚠️ Legal Notice

- Use this scraper responsibly and in compliance with Google Maps' Terms of Service
- Respect robots.txt and website policies
- Do not overload servers with excessive requests
- Consider the website's scraping policies

## 🐛 Troubleshooting

### Chrome/ChromeDriver Issues

```bash
# Update Selenium
pip install --upgrade selenium
```

### Missing Elements

- Increase wait times in scraper.py
- Check XPath selectors (Google Maps UI may change)

### Memory Issues

- Reduce number of processes in `Pool()`
- Process queries in smaller batches

### Rate Limiting

- Increase random delay values
- Add longer sleep times between requests

## 📝 License

This project is open source and available under the MIT License.