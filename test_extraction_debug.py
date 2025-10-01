import json
import sys
import asyncio
sys.path.append('.')
from scraper import XayconScraper

async def test_match_extraction():
    scraper = XayconScraper()
    print("Testing match extraction and data structure...")
    
    matches = await scraper.scrape_matches()
    
    if matches:
        print(f"\nFound {len(matches)} matches:")
        for i, match in enumerate(matches[:3], 1):  # Show first 3 matches
            print(f"\n--- Match {i} ---")
            print(f"ID: {match.get('id')}")
            print(f"Home Team: {match.get('home_team')}")
            print(f"Away Team: {match.get('away_team')}")
            print(f"Time: {match.get('time')}")
            print(f"Date: {match.get('date')}")
            print(f"Score: {match.get('score')}")
            print(f"Tournament: {match.get('tournament')}")
            print(f"Status: {match.get('status')}")
            print(f"Is Live: {match.get('is_live')}")
            print(f"Schedule: {match.get('schedule')}")
            print(f"Description: {match.get('description')}")
    else:
        print("No matches found")

if __name__ == "__main__":
    asyncio.run(test_match_extraction())