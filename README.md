# IPO Scraper

A robust web scraper that collects and tracks Initial Public Offering (IPO) data from [Screener.in](https://www.screener.in). This tool automates the process of gathering IPO information, including listing dates, market capitalizations, price history, and performance metrics.

## Overview

The IPO Scraper is designed to:
- Extract comprehensive IPO data from Screener.in
- Track listing dates, IPO prices, current prices, and performance metrics
- Maintain a record of processed IPOs to avoid duplication
- Export collected data to Excel for easy analysis
- Implement error handling and retry mechanisms for reliable data collection

## Features

- **Automated Data Collection**: Scrapes IPO data from multiple pages automatically
- **Duplicate Prevention**: Maintains a record of processed IPOs to avoid duplication
- **Comprehensive Data**: Collects company name, listing date, market cap, IPO price, current price, and performance metrics
- **Persistent Storage**: Exports data to Excel for easy analysis and record-keeping
- **Error Handling**: Implements robust error handling and retry logic
- **Logging**: Provides detailed logging for monitoring and debugging

## Technologies Used

- **Python 3.7+**: Core programming language
- **Requests**: HTTP library for making web requests
- **BeautifulSoup4**: HTML parsing and navigation
- **Pandas**: Data manipulation and Excel export
- **Logging**: Standard library for application logging
- **Pathlib**: Object-oriented filesystem paths
- **JSON**: Data serialization for tracking processed IPOs

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/ipo-scraper.git
   cd ipo-scraper
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use: venv\Scripts\activate
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Basic Usage

Run the script to start scraping IPO data:

```bash
python ipo_scraper.py
```

### Output

The script generates:
- `ipo_data.xlsx`: Excel file containing all the scraped IPO data
- `processed_ipos.json`: JSON file tracking already processed IPOs to avoid duplication

### Example Output

The Excel file will contain the following columns:
- Company: Name of the company
- Company Link: URL to the company's page on Screener.in
- Listing Date: Date when the company was listed
- IPO MCap (Rs. Cr): Market capitalization at IPO
- IPO Price: Initial offering price
- Current Price: Current trading price
- Percent Change: Performance since IPO

## 🔍 How It Works

1. The scraper starts by loading previously processed IPOs from the JSON file.
2. It then navigates to the recent IPO page on Screener.in.
3. The scraper determines the total number of pages to process.
4. For each page, it extracts data from the IPO table, including:
   - Company name and link
   - Listing date
   - Market capitalization
   - IPO price
   - Current price
   - Performance metrics
5. New IPO data is appended to the Excel file.
6. The list of processed IPOs is updated to avoid duplication in future runs.

## Development Challenges

- **Handling Pagination**: Implementing a robust solution to navigate through multiple pages of IPO listings.
- **Preventing Duplication**: Creating a system to track already processed IPOs across multiple runs.
- **Error Handling**: Building resilient error handling and retry mechanisms to deal with potential network issues.
- **Rate Limiting**: Implementing reasonable delays between requests to respect the website's servers.

## Future Enhancements

- Add command-line arguments for customization (e.g., output file path, base URL)
- Implement email notifications for new IPO listings
- Add data visualization capabilities
- Expand to scrape additional financial metrics
- Implement parallel processing for faster scraping
- Add support for additional data sources


## Contact

For questions or feedback, please reach out to agrim.goyal@gmail.com.
