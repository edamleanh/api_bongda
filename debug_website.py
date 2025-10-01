"""
Debug script để kiểm tra HTML content từ xaycon.live
"""
import asyncio
import sys
import os
from playwright.async_api import async_playwright

async def debug_website():
    """
    Debug function để xem HTML content thực tế
    """
    print("Debugging xaycon.live website...")
    
    url = "https://www.xaycon.live/"
    
    try:
        async with async_playwright() as p:
            # Khởi tạo browser
            browser = await p.chromium.launch(
                headless=True,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-accelerated-2d-canvas',
                    '--no-first-run',
                    '--no-zygote',
                    '--disable-gpu'
                ]
            )
            
            context = await browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            )
            
            page = await context.new_page()
            
            print(f"Loading {url}...")
            await page.goto(url, wait_until='domcontentloaded')
            
            print("Waiting 5 seconds for content to load...")
            await asyncio.sleep(5)
            
            # Lấy HTML content
            html_content = await page.content()
            
            await browser.close()
            
            print(f"\nHTML Content Length: {len(html_content)} characters")
            print("\n" + "="*50)
            print("FIRST 2000 CHARACTERS:")
            print("="*50)
            print(html_content[:2000])
            print("\n" + "="*50)
            
            # Tìm text chứa keywords liên quan đến bóng đá
            keywords = ['vs', 'live', 'match', 'team', 'score', 'goal', 'minute', 'time']
            print(f"SEARCHING FOR KEYWORDS: {', '.join(keywords)}")
            print("="*50)
            
            lines = html_content.split('\n')
            found_lines = []
            
            for i, line in enumerate(lines):
                line_lower = line.lower().strip()
                if any(keyword in line_lower for keyword in keywords):
                    found_lines.append((i, line.strip()))
            
            if found_lines:
                print(f"Found {len(found_lines)} lines with keywords:")
                for line_num, line in found_lines[:20]:  # Show first 20 matches
                    print(f"Line {line_num}: {line}")
            else:
                print("No lines found with football-related keywords")
            
            # Tìm các elements có class hoặc id liên quan
            print("\n" + "="*50)
            print("SEARCHING FOR RELEVANT CSS CLASSES/IDS:")
            print("="*50)
            
            import re
            class_pattern = r'class=["\']([^"\']*)["\']'
            id_pattern = r'id=["\']([^"\']*)["\']'
            
            classes = re.findall(class_pattern, html_content)
            ids = re.findall(id_pattern, html_content)
            
            relevant_classes = [cls for cls in classes if any(keyword in cls.lower() for keyword in ['match', 'game', 'live', 'team', 'score', 'fixture'])]
            relevant_ids = [id_val for id_val in ids if any(keyword in id_val.lower() for keyword in ['match', 'game', 'live', 'team', 'score', 'fixture'])]
            
            if relevant_classes:
                print(f"Relevant classes found: {set(relevant_classes)}")
            if relevant_ids:
                print(f"Relevant IDs found: {set(relevant_ids)}")
            
            if not relevant_classes and not relevant_ids:
                print("No relevant CSS classes or IDs found")
                
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(debug_website())