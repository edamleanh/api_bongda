# 🚀 Hướng dẫn Deploy API lên Render.com

## Tổng quan
API này scrape dữ liệu trận đấu từ xaycon.live và cung cấp REST endpoints với thông tin ngày thi đấu đầy đủ.

## 📋 Bước 1: Chuẩn bị Repository GitHub

### 1.1 Tạo Repository mới
1. Truy cập [GitHub](https://github.com) và đăng nhập
2. Click **"New repository"**
3. Đặt tên: `xaycon-api` (hoặc tên bạn muốn)
4. Chọn **Public** (để Render.com free tier có thể access)
5. Click **"Create repository"**

### 1.2 Upload code lên GitHub
```bash
# Mở terminal tại thư mục project
cd "c:\Users\edaml\OneDrive\Desktop\New folder\New folder (3)"

# Khởi tạo git repository
git init

# Thêm remote origin (thay YOUR_USERNAME bằng GitHub username của bạn)
git remote add origin https://github.com/YOUR_USERNAME/xaycon-api.git

# Add tất cả files
git add .

# Commit
git commit -m "Initial commit: Xaycon Live Match API"

# Push lên GitHub
git push -u origin main
```

## 🌐 Bước 2: Deploy trên Render.com

### 2.1 Tạo tài khoản Render.com
1. Truy cập [Render.com](https://render.com)
2. Click **"Get Started for Free"**
3. Đăng ký bằng GitHub account (recommended)

### 2.2 Tạo Web Service
1. Trong Dashboard, click **"New +"**
2. Chọn **"Web Service"**
3. Click **"Connect a repository"**
4. Chọn repository `xaycon-api` vừa tạo
5. Click **"Connect"**

### 2.3 Cấu hình Deploy Settings

**Basic Settings:**
- **Name**: `xaycon-api` (hoặc tên khác)
- **Region**: `Oregon (US West)` (gần nhất với VN)
- **Branch**: `main`
- **Root Directory**: để trống
- **Environment**: `Python 3`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python app.py`

**Advanced Settings:**
- **Auto-Deploy**: `Yes` (tự động deploy khi có code mới)

## ⚙️ Bước 3: Environment Variables (Tùy chọn)

Không cần thiết lập environment variables cho API này vì:
- Không sử dụng API keys
- Không có database connections
- Tất cả cấu hình đã hard-coded trong code

## 🚀 Bước 4: Deploy và Kiểm tra

### 4.1 Bắt đầu Deploy
1. Kiểm tra lại tất cả settings
2. Click **"Create Web Service"**
3. Render.com sẽ bắt đầu build và deploy

### 4.2 Theo dõi Deploy Process
- Deploy log sẽ hiển thị real-time
- Thời gian deploy: ~3-5 phút
- Khi thành công, sẽ có URL như: `https://xaycon-api.onrender.com`

### 4.3 Test API sau khi deploy
```bash
# Test homepage
curl https://your-app-name.onrender.com/

# Test matches endpoint
curl https://your-app-name.onrender.com/api/matches

# Test live matches
curl https://your-app-name.onrender.com/api/matches/live

# Test status
curl https://your-app-name.onrender.com/api/status
```

## 📊 Bước 5: Monitoring và Maintenance

### 5.1 Render.com Dashboard
- **Logs**: Xem logs realtime
- **Metrics**: CPU, Memory usage
- **Events**: Deploy history

### 5.2 API Endpoints
Sau khi deploy thành công, các endpoints sẽ available tại:

- **GET** `https://your-app.onrender.com/` - Homepage & API info
- **GET** `https://your-app.onrender.com/api/matches` - Tất cả trận đấu
- **GET** `https://your-app.onrender.com/api/matches/live` - Trận đấu LIVE
- **GET** `https://your-app.onrender.com/api/status` - API status
- **POST** `https://your-app.onrender.com/api/refresh` - Force refresh data

### 5.3 Auto-refresh Data
- API tự động cập nhật dữ liệu mỗi phút
- Scrape dữ liệu từ xaycon.live với Playwright
- Cache data để tăng performance

## 🔧 Troubleshooting

### Lỗi thường gặp:

**1. Build failed - Dependencies error**
```
Giải pháp: Kiểm tra requirements.txt có đầy đủ dependencies
```

**2. App failed to start**
```
Giải pháp: Kiểm tra Start Command: python app.py
Kiểm tra app.py có lỗi syntax không
```

**3. Playwright browser error**
```
Giải pháp: Đã include playwright-install command trong requirements.txt
```

**4. Memory limit exceeded**
```
Giải pháp: Render.com free tier có 512MB RAM
Optimize scraper để giảm memory usage
```

### Debug Commands:
```bash
# Check logs
curl https://your-app.onrender.com/api/status

# Manual refresh
curl -X POST https://your-app.onrender.com/api/refresh

# Test specific endpoint
curl https://your-app.onrender.com/api/matches | jq '.data.matches[0]'
```

## 💡 Tips cho Production

1. **Domain tùy chỉnh**: Upgrade plan để có custom domain
2. **HTTPS**: Render.com tự động cung cấp SSL certificate
3. **Scaling**: Auto-scale khi traffic tăng (paid plans)
4. **Monitoring**: Setup uptime monitoring với tools như UptimeRobot
5. **Error handling**: API đã có comprehensive error handling

## 🎯 Kết quả mong đợi

Sau khi deploy thành công:
- ✅ API chạy 24/7 trên cloud
- ✅ Auto-refresh data mỗi phút
- ✅ Scrape được thông tin ngày thi đấu chính xác
- ✅ REST API endpoints hoạt động ổn định
- ✅ Miễn phí với Render.com free tier

---

**Chúc bạn deploy thành công! 🚀**

Nếu gặp vấn đề gì, hãy check logs trong Render.com dashboard hoặc test locally trước.
git commit -m "Initial commit - Xaycon Live API"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

## Bước 3: Deploy trên Render.com

### 3.1 Tạo tài khoản Render.com

1. Truy cập [render.com](https://render.com)
2. Đăng ký tài khoản miễn phí bằng GitHub

### 3.2 Tạo Web Service

1. Nhấn **"New"** > **"Web Service"**
2. Chọn **"Build and deploy from a Git repository"**
3. Connect với GitHub repository của bạn
4. Chọn repository vừa tạo

### 3.3 Cấu hình Deploy

Điền thông tin như sau:

**Basic Settings:**
- **Name**: `xaycon-api` (hoặc tên bạn muốn)
- **Language**: `Python 3`
- **Branch**: `main`
- **Root Directory**: để trống

**Build & Deploy:**
- **Build Command**: 
  ```bash
  pip install -r requirements.txt && playwright install chromium
  ```
- **Start Command**: 
  ```bash
  python app.py
  ```

**Advanced Settings:**
- **Auto-Deploy**: Yes (để tự động deploy khi có commit mới)

### 3.4 Environment Variables (Tùy chọn)

Không cần thiết lập environment variables đặc biệt cho project này.

### 3.5 Deploy

1. Nhấn **"Create Web Service"**
2. Chờ deploy hoàn tất (khoảng 5-10 phút)
3. Render sẽ cung cấp URL public cho API của bạn

## Bước 4: Test API

Sau khi deploy thành công, API sẽ có URL dạng:
`https://your-service-name.onrender.com`

### Test các endpoints:

1. **Trang chủ:**
   ```
   GET https://your-service-name.onrender.com/
   ```

2. **Tất cả trận đấu:**
   ```
   GET https://your-service-name.onrender.com/api/matches
   ```

3. **Trận đấu Live:**
   ```
   GET https://your-service-name.onrender.com/api/matches/live
   ```

4. **Trạng thái API:**
   ```
   GET https://your-service-name.onrender.com/api/status
   ```

5. **Refresh thủ công:**
   ```
   GET https://your-service-name.onrender.com/api/refresh
   ```

## Bước 5: Lưu ý quan trọng

### 5.1 Về gói miễn phí Render.com

- **Sleep**: Service sẽ sleep sau 15 phút không có request
- **Thời gian**: 750 giờ/tháng (khoảng 24 ngày)
- **Băng thông**: 100GB/tháng
- **Wake-up**: Mất 30-60 giây để wake up từ sleep

### 5.2 Để tránh sleep

Có thể setup ping service để keep-alive:

1. Sử dụng [UptimeRobot](https://uptimerobot.com) miễn phí
2. Monitor URL: `https://your-service-name.onrender.com/api/status`
3. Interval: 14 phút (tránh sleep)

### 5.3 Monitoring

- Xem logs trong Render Dashboard
- API tự động cập nhật data mỗi phút
- Có thể monitor qua `/api/status` endpoint

## Troubleshooting

### Lỗi Playwright

Nếu gặp lỗi với Playwright:
```
Error: Failed to launch chromium
```

**Giải pháp**: Thêm args trong `scraper.py`:
```python
args=[
    '--no-sandbox',
    '--disable-setuid-sandbox',
    '--disable-dev-shm-usage',
    '--disable-accelerated-2d-canvas',
    '--no-first-run',
    '--no-zygote',
    '--disable-gpu'
]
```

### Lỗi Build

Nếu build fail:
1. Kiểm tra `requirements.txt` có đúng format không
2. Đảm bảo Python version trong `runtime.txt` được hỗ trợ
3. Xem build logs trong Render Dashboard

### Lỗi Memory

Nếu app crash do memory:
1. Optimize scraper (giảm số lượng browser instances)
2. Thêm delay giữa các requests
3. Clear cache định kỳ

## Kết quả

Sau khi deploy thành công, bạn sẽ có:

✅ API REST hoàn chỉnh cho xaycon.live  
✅ Tự động cập nhật data mỗi phút  
✅ Endpoints cho tất cả trận đấu và trận live  
✅ Chạy 24/7 trên cloud miễn phí  
✅ Có thể integrate vào website/app khác  

**URL API mẫu:** `https://xaycon-api.onrender.com`