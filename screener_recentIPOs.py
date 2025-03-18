import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import logging
from pathlib import Path
import json
from datetime import datetime

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)

class IPOScraper:
    def __init__(self, base_url: str = "https://www.screener.in"):
        """
        Initialize the IPO scraper with base URL and settings.
        
        Args:
            base_url: The base URL for screener.in
        """
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        # Store processed IPOs in a set for quick lookup
        self.processed_ipos = self._load_processed_ipos()
        self.output_file = "ipo_data.xlsx"
        self.processed_file = "processed_ipos.json"
        
    def _load_processed_ipos(self) -> set:
        """
        Load previously processed IPOs from JSON file.
        
        Returns:
            Set of processed IPO identifiers
        """
        try:
            if Path(self.processed_file).exists():
                with open(self.processed_file, 'r') as f:
                    return set(json.load(f))
        except Exception as e:
            logger.error(f"Error loading processed IPOs: {str(e)}")
        return set()

    def _save_processed_ipos(self):
        """Save processed IPOs to JSON file."""
        try:
            with open(self.processed_file, 'w') as f:
                json.dump(list(self.processed_ipos), f)
        except Exception as e:
            logger.error(f"Error saving processed IPOs: {str(e)}")

    def _extract_pagination_info(self, soup: BeautifulSoup) -> int:
        """
        Extract total number of pages from pagination div.
        
        Args:
            soup: BeautifulSoup object of the page
            
        Returns:
            Total number of pages
        """
        pagination = soup.find('div', class_='pagination')
        if not pagination:
            return 1
            
        # Find all page links
        page_links = pagination.find_all('a')
        max_page = 1
        
        for link in page_links:
            # Extract page number from href
            if 'page=' in link.get('href', ''):
                try:
                    page_num = int(link['href'].split('page=')[1])
                    max_page = max(max_page, page_num)
                except ValueError:
                    continue
                    
        return max_page

    def _extract_ipo_data(self, row) -> dict:
        """
        Extract IPO information from a table row.
        
        Args:
            row: BeautifulSoup table row object
            
        Returns:
            Dictionary containing IPO data
        """
        cells = row.find_all('td')
        if not cells:
            return None
            
        # Extract company name and link
        name_cell = cells[0].find('a')
        if not name_cell:
            return None
            
        company_name = name_cell.text.strip()
        company_link = name_cell['href']
        
        # Create unique identifier for IPO
        ipo_id = f"{company_name}_{cells[1].text.strip()}"
        
        # Extract other data
        ipo_data = {
            'Company': company_name,
            'Company Link': f"{self.base_url}{company_link}",
            'Listing Date': cells[1].text.strip(),
            'IPO MCap (Rs. Cr)': cells[2].text.strip(),
            'IPO Price': cells[3].text.replace('₹', '').strip(),
            'Current Price': cells[4].text.replace('₹', '').strip(),
            'Percent Change': cells[5].text.strip().replace('⇣', '-').replace('⇡', '+')
        }
        
        return ipo_id, ipo_data

    def _make_request(self, url: str) -> requests.Response:
        """
        Make an HTTP request with error handling and retry logic.
        
        Args:
            url: URL to request
            
        Returns:
            Response object or None if failed
        """
        max_retries = 3
        
        for attempt in range(max_retries):
            try:
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                return response
            except requests.RequestException as e:
                logger.error(f"Error fetching {url}: {str(e)}")
                
            if attempt < max_retries - 1:
                delay = (2 ** attempt) + (time.random() * 0.1)
                time.sleep(delay)
            
        return None

    def scrape_ipo_data(self):
        """Scrape IPO data from all pages and save to Excel."""
        all_ipo_data = []
        url = f"{self.base_url}/ipo/recent/"
        
        # Get initial page
        response = self._make_request(url)
        if not response:
            logger.error("Failed to fetch initial page")
            return
            
        soup = BeautifulSoup(response.text, 'html.parser')
        total_pages = self._extract_pagination_info(soup)
        
        logger.info(f"Found {total_pages} pages to process")
        
        # Process all pages
        for page in range(1, total_pages + 1):
            page_url = f"{url}?page={page}"
            response = self._make_request(page_url)
            
            if not response:
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            table = soup.find('table', class_='data-table')
            
            if not table:
                continue
                
            # Process each row
            for row in table.find('tbody').find_all('tr'):
                ipo_id, ipo_data = self._extract_ipo_data(row)
                
                if ipo_id in self.processed_ipos:
                    logger.info(f"IPO {ipo_data['Company']} already processed, skipping...")
                    continue
                    
                all_ipo_data.append(ipo_data)
                self.processed_ipos.add(ipo_id)
                
            logger.info(f"Processed page {page}/{total_pages}")
            time.sleep(2)  # Be nice to the server
            
        # Save data if we found new IPOs
        if all_ipo_data:
            # Load existing data if file exists
            if Path(self.output_file).exists():
                existing_df = pd.read_excel(self.output_file)
                new_df = pd.DataFrame(all_ipo_data)
                final_df = pd.concat([existing_df, new_df], ignore_index=True)
            else:
                final_df = pd.DataFrame(all_ipo_data)
                
            final_df.to_excel(self.output_file, index=False)
            self._save_processed_ipos()
            logger.info(f"Added {len(all_ipo_data)} new IPOs to {self.output_file}")
        else:
            logger.info("No new IPOs found")

def main():
    """Main function to run the IPO scraper."""
    scraper = IPOScraper()
    scraper.scrape_ipo_data()

if __name__ == "__main__":
    main()