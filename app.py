import os
import asyncio
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from scraper import XayconScraper
import atexit

app = Flask(__name__)

# Khởi tạo scraper
scraper = XayconScraper()

# Khởi tạo scheduler
scheduler = BackgroundScheduler()


def update_data():
    """
    Hàm cập nhật dữ liệu chạy trong background
    """
    try:
        print("Updating match data...")
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(scraper.scrape_matches())
        loop.close()
        print("Match data updated successfully")
    except Exception as e:
        print(f"Error updating data: {e}")


@app.route('/')
def home():
    """
    Endpoint trang chủ
    """
    return jsonify({
        'message': 'Xaycon Live Match API',
        'endpoints': {
            '/api/matches': 'Lấy danh sách tất cả trận đấu',
            '/api/matches/live': 'Lấy danh sách trận đấu đang diễn ra',
            '/api/status': 'Kiểm tra trạng thái API'
        }
    })


@app.route('/api/matches')
def get_all_matches():
    """
    API endpoint trả về tất cả trận đấu với thông tin ngày thi đấu đầy đủ
    """
    try:
        data = scraper.get_cached_data()
        
        # Định dạng lại dữ liệu để hiển thị thông tin ngày thi đấu rõ ràng
        if 'matches' in data:
            formatted_matches = []
            for match in data['matches']:
                formatted_match = {
                    'id': match.get('id'),
                    'home_team': match.get('home_team'),
                    'away_team': match.get('away_team'),
                    'tournament': match.get('tournament'),
                    'match_time': match.get('time'),
                    'match_date': match.get('date'),
                    'schedule': match.get('schedule', f"{match.get('date', 'TBD')} {match.get('time', 'TBD')}"),
                    'score': match.get('score'),
                    'status': match.get('status'),
                    'is_live': match.get('is_live', False),
                    'description': match.get('description', f"{match.get('tournament', 'Unknown')} - {match.get('date', 'TBD')} {match.get('time', 'TBD')} - {match.get('status', 'Unknown')}")
                }
                formatted_matches.append(formatted_match)
            
            data['matches'] = formatted_matches
        
        return jsonify({
            'success': True,
            'data': data,
            'message': 'Dữ liệu trận đấu được lấy thành công'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Lỗi khi lấy dữ liệu trận đấu'
        }), 500


@app.route('/api/matches/live')
def get_live_matches():
    """
    API endpoint trả về các trận đấu đang diễn ra
    """
    try:
        data = scraper.get_cached_data()
        live_matches = [match for match in data['matches'] if match.get('is_live', False)]
        
        return jsonify({
            'success': True,
            'data': {
                'matches': live_matches,
                'last_updated': data['last_updated'],
                'total_live_matches': len(live_matches)
            },
            'message': 'Dữ liệu trận đấu live được lấy thành công'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Lỗi khi lấy dữ liệu trận đấu live'
        }), 500


@app.route('/api/status')
def get_status():
    """
    API endpoint kiểm tra trạng thái
    """
    try:
        data = scraper.get_cached_data()
        return jsonify({
            'success': True,
            'status': 'active',
            'last_updated': data['last_updated'],
            'total_matches': data['total_matches'],
            'message': 'API đang hoạt động bình thường'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'status': 'error',
            'error': str(e),
            'message': 'API gặp lỗi'
        }), 500


@app.route('/api/refresh')
def manual_refresh():
    """
    API endpoint để cập nhật dữ liệu thủ công
    """
    try:
        # Chạy update trong thread riêng
        import threading
        thread = threading.Thread(target=update_data)
        thread.start()
        
        return jsonify({
            'success': True,
            'message': 'Đã bắt đầu cập nhật dữ liệu thủ công'
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'message': 'Lỗi khi cập nhật dữ liệu thủ công'
        }), 500


def initialize_app():
    """
    Khởi tạo ứng dụng
    """
    print("Initializing application...")
    
    # Lấy dữ liệu ban đầu
    update_data()
    
    # Thiết lập scheduler để cập nhật mỗi phút
    scheduler.add_job(
        func=update_data,
        trigger=IntervalTrigger(minutes=1),
        id='update_matches',
        name='Update match data every minute',
        replace_existing=True
    )
    
    # Bắt đầu scheduler
    scheduler.start()
    print("Scheduler started - data will be updated every minute")
    
    # Đảm bảo scheduler dừng khi app tắt
    atexit.register(lambda: scheduler.shutdown())


if __name__ == '__main__':
    initialize_app()
    
    # Lấy port từ environment variable (cho Render.com)
    port = int(os.environ.get('PORT', 5000))
    
    # Chạy app
    app.run(
        host='0.0.0.0',
        port=port,
        debug=False,
        threaded=True
    )