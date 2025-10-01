import asyncio
import json
from datetime import datetime
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup


class XayconScraper:
    def __init__(self):
        self.url = "https://www.xaycon.live/"
        self.last_data = []
        self.last_updated = None

    async def scrape_matches(self):
        """
        Lấy HTML của website sau 5 giây và phân tích dữ liệu trận đấu
        """
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
                
                # Truy cập website
                await page.goto(self.url, wait_until='domcontentloaded')
                
                # Chờ 5 giây để trang load đủ thông tin
                await asyncio.sleep(5)
                
                # Lấy HTML content
                html_content = await page.content()
                
                await browser.close()
                
                # Phân tích HTML để lấy thông tin trận đấu
                matches = self.parse_matches(html_content)
                self.last_data = matches
                self.last_updated = datetime.now().isoformat()
                
                return matches
                
        except Exception as e:
            print(f"Error scraping matches: {e}")
            return self.last_data

    def parse_matches(self, html_content):
        """
        Phân tích HTML để lấy thông tin các trận đấu live
        """
        try:
            soup = BeautifulSoup(html_content, 'html.parser')
            matches = []
            seen_matches = set()  # Để tránh trùng lặp
            
            # Tìm các element chứa thông tin trận đấu theo cấu trúc thực tế
            match_elements = soup.find_all('div', class_=lambda x: x and 'bg-match-card' in x)
            
            print(f"Found {len(match_elements)} match elements")
            
            for element in match_elements:
                try:
                    match_info = self.extract_match_info_new(element)
                    if match_info and match_info['id'] not in seen_matches:
                        matches.append(match_info)
                        seen_matches.add(match_info['id'])
                        print(f"Parsed match: {match_info['home_team']} vs {match_info['away_team']} - {match_info['status']}")
                except Exception as e:
                    print(f"Error parsing match element: {e}")
                    continue
            
            return matches
            
        except Exception as e:
            print(f"Error parsing HTML: {e}")
            return []

    def extract_match_info_new(self, element):
        """
        Trích xuất thông tin từ element trận đấu theo cấu trúc mới của xaycon.live
        """
        try:
            import re
            
            # Lấy thời gian và ngày từ container chứa time/date
            time_element = element.find('div', class_=lambda x: x and 'text-primary' in x and 'font-bold' in x and 'items-center' in x and 'gap-x-4' in x)
            match_time = None
            match_date = None
            
            if time_element:
                time_text = time_element.get_text(strip=True)
                print(f"Found time/date text: '{time_text}'")
                
                # Sử dụng regex để tách time và date từ text như "20:4501/10"
                time_match = re.search(r'(\d{1,2}:\d{2})', time_text)
                date_match = re.search(r'(\d{1,2}/\d{1,2})', time_text)
                
                if time_match:
                    match_time = time_match.group(1)
                    print(f"Extracted time: {match_time}")
                if date_match:
                    match_date = date_match.group(1)
                    print(f"Extracted date: {match_date}")
            
            # Lấy tên giải đấu
            tournament_element = element.find('div', class_=lambda x: x and 'text-primary' in x and 'overflow-hidden' in x and 'truncate' in x)
            tournament = tournament_element.get_text(strip=True) if tournament_element else 'Unknown'
            
            # Lấy tên các đội từ img alt attributes
            team_images = element.find_all('img', alt=True)
            teams = []
            for img in team_images:
                alt_text = img.get('alt', '').strip()
                # Loại bỏ các alt không phải tên đội
                if alt_text and not any(skip in alt_text.lower() for skip in ['banner', 'live', 'xay-con', 'avatar']):
                    teams.append(alt_text)
            
            # Nếu không tìm được từ img, thử tìm trong text
            if len(teams) < 2:
                team_texts = []
                # Tìm text giữa các img elements
                for img in team_images[:2]:  # Chỉ lấy 2 img đầu (home và away team)
                    parent = img.parent
                    if parent:
                        team_text = parent.get_text(strip=True)
                        if team_text and team_text not in team_texts:
                            team_texts.append(team_text)
                
                if team_texts:
                    teams = team_texts
            
            # Kiểm tra trạng thái LIVE
            is_live = False
            status = 'Upcoming'
            
            # Tìm element chứa trạng thái LIVE với class text-status-red
            live_element = element.find('div', class_=lambda x: x and 'text-status-red' in x)
            if live_element:
                status_text = live_element.get_text(strip=True).upper()
                if 'LIVE' in status_text:
                    is_live = True
                    status = 'LIVE'
            
            # Tìm trạng thái khác
            if not is_live:
                status_elements = element.find_all('div', class_=lambda x: x and 'bg-white' in x)
                for status_elem in status_elements:
                    status_text = status_elem.get_text(strip=True)
                    if status_text and status_text not in ['VS']:
                        status = status_text
                        break
            
            # Tìm tỷ số thực (nếu có) - chỉ tìm trong các element không phải time/date
            score = None
            score_elements = element.find_all(string=lambda text: text and ':' in text and text.count(':') == 1)
            for score_text in score_elements:
                score_text = score_text.strip()
                if score_text and len(score_text) <= 10:  # Tỷ số thường ngắn
                    try:
                        parts = score_text.split(':')
                        if len(parts) == 2 and parts[0].isdigit() and parts[1].isdigit():
                            # Kiểm tra để tránh nhầm với thời gian (ví dụ: 20:45)
                            # Tỷ số thường có giá trị nhỏ (0-10), thời gian có giá trị lớn hơn
                            hour_part = int(parts[0])
                            minute_part = int(parts[1])
                            
                            # Nếu không phải định dạng thời gian (giờ:phút) thì mới coi là tỷ số
                            if not (0 <= hour_part <= 23 and 0 <= minute_part <= 59 and len(parts[0]) >= 2):
                                score = score_text
                                break
                    except:
                        continue
            
            # Tạo object match nếu có đủ thông tin
            if len(teams) >= 2:
                # Tạo unique ID để tránh trùng lặp
                match_id = f"{teams[0]}-{teams[1]}-{match_time}-{match_date}"
                
                match_info = {
                    'id': match_id,
                    'home_team': teams[0],
                    'away_team': teams[1],
                    'score': score,
                    'time': match_time,
                    'date': match_date,
                    'tournament': tournament,
                    'status': status,
                    'is_live': is_live,
                    'schedule': f"{match_date} {match_time}" if match_date and match_time else 'TBD',
                    'description': f"{tournament} - {match_date} {match_time} - {status}" if match_date and match_time else f"{tournament} - {status}"
                }
                
                return match_info
            
            return None
            
        except Exception as e:
            print(f"Error extracting match info: {e}")
            return None

    def extract_matches_by_text_pattern(self, soup):
        """
        Trích xuất matches bằng cách tìm patterns trong text
        """
        try:
            matches = []
            text_content = soup.get_text()
            lines = text_content.split('\n')
            
            for i, line in enumerate(lines):
                line = line.strip()
                # Tìm patterns giống như "Team A vs Team B" hoặc "Team A - Team B"
                if ' vs ' in line.lower() or ' - ' in line:
                    teams = line.replace(' vs ', ' - ').split(' - ')
                    if len(teams) == 2:
                        # Tìm score và time trong các dòng gần đó
                        context_lines = lines[max(0, i-2):min(len(lines), i+3)]
                        score = None
                        match_time = None
                        status = 'Unknown'
                        
                        for context_line in context_lines:
                            context_line = context_line.strip()
                            # Tìm score pattern (số:số hoặc số-số)
                            if ':' in context_line and context_line.count(':') == 1:
                                parts = context_line.split(':')
                                if len(parts) == 2 and parts[0].strip().isdigit() and parts[1].strip().isdigit():
                                    score = context_line
                            
                            # Tìm time pattern
                            if any(keyword in context_line.upper() for keyword in ['LIVE', 'MIN', "'"]):
                                match_time = context_line
                                if 'LIVE' in context_line.upper():
                                    status = 'LIVE'
                        
                        matches.append({
                            'home_team': teams[0].strip(),
                            'away_team': teams[1].strip(),
                            'score': score,
                            'time': match_time,
                            'status': status,
                            'is_live': status == 'LIVE'
                        })
            
            return matches
            
        except Exception as e:
            print(f"Error extracting matches by text pattern: {e}")
            return []

    def get_cached_data(self):
        """
        Trả về dữ liệu đã cache
        """
        return {
            'matches': self.last_data,
            'last_updated': self.last_updated,
            'total_matches': len(self.last_data)
        }