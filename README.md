# Xaycon Live Match API

API miễn phí để lấy thông tin các trận đấu từ website xaycon.live với tự động cập nhật mỗi phút.

## Tính năng

- 🔄 Tự động lấy dữ liệu từ xaycon.live mỗi 1 phút
- ⏱️ Chờ 5 giây để website load đầy đủ thông tin
- 🏆 API RESTful trả về thông tin các trận đấu
- 🎯 Lọc riêng các trận đấu đang diễn ra (Live)
- 🚀 Deploy miễn phí trên Render.com

## API Endpoints

### `GET /`
Trang chủ với thông tin về các endpoints có sẵn.

### `GET /api/matches`
Lấy danh sách tất cả các trận đấu.

**Response:**
```json
{
  "success": true,
  "data": {
    "matches": [
      {
        "home_team": "Team A",
        "away_team": "Team B",
        "score": "2:1",
        "time": "75'",
        "status": "LIVE",
        "is_live": true
      }
    ],
    "last_updated": "2024-01-01T12:00:00.000000",
    "total_matches": 10
  },
  "message": "Dữ liệu trận đấu được lấy thành công"
}
```

### `GET /api/matches/live`
Lấy danh sách các trận đấu đang diễn ra.

### `GET /api/status`
Kiểm tra trạng thái API và thời gian cập nhật cuối cùng.

### `GET /api/refresh`
Cập nhật dữ liệu thủ công (không cần chờ chu kỳ 1 phút).

## Cài đặt và chạy local

### 1. Clone repository
```bash
git clone <repository-url>
cd xaycon-api
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Cài đặt Playwright browsers
```bash
playwright install chromium
```

### 4. Chạy ứng dụng
```bash
python app.py
```

API sẽ chạy tại `http://localhost:5000`

## Deploy lên Render.com

### 1. Tạo tài khoản Render.com
Truy cập [render.com](https://render.com) và đăng ký tài khoản miễn phí.

### 2. Tạo Web Service mới
- Chọn "New" → "Web Service"
- Kết nối với GitHub repository của bạn
- Chọn repository chứa code này

### 3. Cấu hình Deploy
```
Name: xaycon-api (hoặc tên bạn muốn)
Environment: Python 3
Build Command: pip install -r requirements.txt && playwright install chromium
Start Command: python app.py
```

### 4. Environment Variables (nếu cần)
Không cần thiết lập environment variables đặc biệt cho project này.

### 5. Deploy
Nhấn "Create Web Service" và chờ deploy hoàn tất.

## Cấu trúc Project

```
xaycon-api/
├── app.py              # Flask API chính
├── scraper.py          # Module scraping website
├── requirements.txt    # Python dependencies
├── Procfile           # Cấu hình cho Render.com
└── README.md          # Tài liệu này
```

## Lưu ý quan trọng

### Về việc scraping
- Website xaycon.live được truy cập mỗi phút một lần
- Mỗi lần truy cập chờ 5 giây để trang load đầy đủ
- Sử dụng Playwright với Chromium headless
- Có xử lý lỗi và fallback data

### Về Render.com
- Gói miễn phí có giới hạn:
  - Sleep sau 15 phút không có request
  - 750 giờ/tháng
  - Có thể chậm khi wake up từ sleep
- Để tránh sleep, có thể setup health check ping định kỳ

### Về hiệu suất
- Dữ liệu được cache trong memory
- API trả về data từ cache, không scrape real-time
- Background job cập nhật data mỗi phút

## Troubleshooting

### Lỗi Playwright
Nếu gặp lỗi với Playwright trên Render.com:
```bash
# Thêm vào requirements.txt
playwright==1.40.0

# Hoặc sử dụng requests + time.sleep thay vì Playwright
```

### Lỗi timeout
Website có thể chậm hoặc block request. Code đã có xử lý timeout và retry.

### Lỗi parsing
Cấu trúc HTML của website có thể thay đổi. Cần cập nhật logic parsing trong `scraper.py`.

## Phát triển thêm

### Thêm database
Có thể thêm SQLite hoặc PostgreSQL để lưu lịch sử trận đấu:
```python
# Thêm vào requirements.txt
sqlalchemy
```

### Thêm logging
```python
import logging
logging.basicConfig(level=logging.INFO)
```

### Thêm caching nâng cao
```python
# Sử dụng Redis cho caching
import redis
```

## License
MIT License - Sử dụng tự do cho mục đích cá nhân và thương mại.