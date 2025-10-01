import re
from bs4 import BeautifulSoup

# Sample HTML from actual website
html_content = '''
<div class="flex w-full flex-col bg-match-card border-bd-match gap-y-4 border-[1px] rounded-[16px] p-3 justify-between cursor-pointer">
    <div class="flex w-full flex-col gap-y-4">
        <div class="flex flex-row w-full justify-between items-center">
            <div class="flex flex-row text-primary font-bold h-4 items-center gap-x-4 text-xs sm:text-base">
                20:45
                <div class="flex h-full w-[1px] bg-[#1111111A]"></div>
                01/10
            </div>
            <div class="block text-primary font-bold text-xs sm:text-[14px] overflow-hidden truncate whitespace-nowrap" style="max-width: 18ch;">
                AFC Champions League 2
            </div>
        </div>
        <div class="flex flex-row w-full items-center gap-x-2">
            <div class="flex flex-col flex-1 items-center justify-center text-primary text-sm sm:text-base text-center gap-y-2 px-2">
                <img alt="FC Istiklol Dushanbe" loading="lazy" width="32" height="32" src="/image1.webp">
                FC Istiklol Dushanbe
            </div>
            <div class="flex flex-row h-[36px] px-2 gap-x-2 items-center justify-center border-status-red border-[1px] rounded-[8px]">
                <div class="flex w-[6px] h-[6px] rounded-full bg-status-red"></div>
                <div class="font-bold text-xs sm:text-base text-status-red">LIVE</div>
            </div>
            <div class="flex flex-col flex-1 items-center justify-center text-primary text-sm sm:text-base text-center gap-y-2 px-2">
                <img alt="FC Goa" loading="lazy" width="32" height="32" src="/image2.webp">
                FC Goa
            </div>
        </div>
    </div>
</div>

<div class="flex w-full flex-col bg-match-card border-bd-match gap-y-4 border-[1px] rounded-[16px] p-3 justify-between cursor-pointer">
    <div class="flex w-full flex-col gap-y-4">
        <div class="flex flex-row w-full justify-between items-center">
            <div class="flex flex-row text-primary font-bold h-4 items-center gap-x-4 text-xs sm:text-base">
                23:00
                <div class="flex h-full w-[1px] bg-[#1111111A]"></div>
                01/10
            </div>
            <div class="block text-primary font-bold text-xs sm:text-[14px] overflow-hidden truncate whitespace-nowrap" style="max-width: 18ch;">
                AFC Champions League 2
            </div>
        </div>
        <div class="flex flex-row w-full items-center gap-x-2">
            <div class="flex flex-col flex-1 items-center justify-center text-primary text-sm sm:text-base text-center gap-y-2 px-2">
                <img alt="Al Wihdat Amman" loading="lazy" width="32" height="32" src="/image3.png">
                Al Wihdat Amman
            </div>
            <div class="flex flex-row h-[36px] px-2 gap-x-2 items-center justify-center border-[#1111111A] border-[1px] rounded-[8px]">
                <div class="font-bold text-xs sm:text-base text-placeholder">VS</div>
            </div>
            <div class="flex flex-col flex-1 items-center justify-center text-primary text-sm sm:text-base text-center gap-y-2 px-2">
                <img alt="Al-Wasl" loading="lazy" width="32" height="32" src="/image4.png">
                Al-Wasl
            </div>
        </div>
    </div>
</div>
'''

def analyze_match_structure():
    print("ANALYZING MATCH CARD STRUCTURE")
    print("=" * 50)
    
    soup = BeautifulSoup(html_content, 'html.parser')
    match_cards = soup.find_all('div', class_='bg-match-card')
    
    for i, card in enumerate(match_cards, 1):
        print(f"\n--- MATCH CARD {i} ---")
        
        # Find time and date
        time_date_container = card.find('div', class_=re.compile(r'flex.*text-primary.*font-bold.*items-center.*gap-x-4'))
        if time_date_container:
            text_content = time_date_container.get_text(strip=True)
            print(f"Time/Date Container Text: '{text_content}'")
            
            # Extract time and date using regex
            time_match = re.search(r'(\d{1,2}:\d{2})', text_content)
            date_match = re.search(r'(\d{1,2}/\d{1,2})', text_content)
            
            if time_match:
                print(f"Match Time: {time_match.group(1)}")
            if date_match:
                print(f"Match Date: {date_match.group(1)}")
        
        # Find competition
        competition_div = card.find('div', class_=re.compile(r'block.*text-primary.*font-bold.*overflow-hidden'))
        if competition_div:
            competition = competition_div.get_text(strip=True)
            print(f"Competition: {competition}")
        
        # Find teams
        team_containers = card.find_all('div', class_=re.compile(r'flex.*flex-col.*flex-1.*items-center.*justify-center'))
        teams = []
        for team_container in team_containers:
            img = team_container.find('img')
            if img and img.get('alt'):
                team_name = img.get('alt')
                teams.append(team_name)
                print(f"Team: {team_name}")
        
        # Find match status
        status_container = card.find('div', class_=re.compile(r'font-bold.*text-status-red'))
        if status_container:
            status = status_container.get_text(strip=True)
            print(f"Status: {status} (LIVE MATCH)")
        else:
            vs_container = card.find('div', class_=re.compile(r'font-bold.*text-placeholder'))
            if vs_container:
                status = vs_container.get_text(strip=True)
                print(f"Status: {status} (Upcoming match)")

if __name__ == "__main__":
    analyze_match_structure()