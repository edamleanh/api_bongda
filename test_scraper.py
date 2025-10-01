"""
Test script để kiểm tra scraper hoạt động
"""
import asyncio
import sys
import os

# Thêm thư mục hiện tại vào Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scraper import XayconScraper


async def test_scraper():
    """
    Test function cho scraper
    """
    print("Testing Xaycon Scraper...")
    
    scraper = XayconScraper()
    
    print("Scraping match data...")
    matches = await scraper.scrape_matches()
    
    print(f"\nFound {len(matches)} matches:")
    for i, match in enumerate(matches, 1):
        print(f"\n{i}. {match['home_team']} vs {match['away_team']}")
        print(f"   Score: {match['score']}")
        print(f"   Time: {match['time']}")
        print(f"   Status: {match['status']}")
        print(f"   Is Live: {match['is_live']}")
    
    # Test cached data
    cached_data = scraper.get_cached_data()
    print(f"\nCached data - Total matches: {cached_data['total_matches']}")
    print(f"Last updated: {cached_data['last_updated']}")


if __name__ == "__main__":
    # Chạy test
    asyncio.run(test_scraper())