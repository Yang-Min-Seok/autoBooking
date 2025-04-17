# 📅 자동 예약 매크로 시스템 (autoBooking) KOREAN(🇰🇷)

웹사이트 예약을 자동으로 수행하는 Python 기반 자동화 스크립트입니다.  
Playwright를 활용해 브라우저를 조작하고, `.env`로 개인정보를 관리하며, cron 또는 작업 스케줄러로 정기 실행이 가능합니다.

---

## 📦 설치 방법

### ✅ 클론 경로 주의

> ❌ 한글 경로 및 클라우드 폴더 (예: `OneDrive`, `iCloud`, `문서`)에서 실행 시 실패 가능  
> ✅ 영문 이름의 로컬 경로 추천: `C:\Projects`, `~/Projects` 등

```bash
git clone https://github.com/Yang-Min-Seok/autoBooking
cd autoBooking
```

---

### 가상환경 생성 및 실행

#### macOS / Linux / Git Bash

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```cmd
python -m venv venv
venv\Scripts\activate
```

---

### 패키지 설치

```bash
pip install -r requirements.txt
playwright install
```

---

### 환경변수 설정

```bash
cp info.env.example info.env        # macOS / Linux
copy info.env.example info.env      # Windows
```

`info.env` 파일을 열어 아래 값을 입력해 주세요:

```env
NAME=홍길동
PHONE_NUMBER=01012345678
E_MAIL=test@example.com
```

---

## 🧪 실행 전 테스트

> Playwright 브라우저가 정상 작동하는지 먼저 확인하세요.

```bash
python3 auto_booking.py
```

---

## 🚀 자동 예약 실행

### macOS / Linux / Git Bash

```bash
chmod +x start_booking.sh
./start_booking.sh
```

### Windows

```cmd
start_booking.bat
```

---

## 🕑 자동 실행 예약

### macOS (cron 사용)

```bash
crontab -e
```

아래 라인 추가 (매주 토요일 오전 7시 실행):

```cron
0 7 * * 6 /Users/yourname/autoBooking/start_booking.sh >> /Users/yourname/autoBooking/cron.log 2>&1
```

### Windows (작업 스케줄러 사용)

1. **작업 스케줄러** 실행  
2. **기본 작업 만들기** 클릭  
3. **트리거**: 매주 토요일 오전 7시 설정  
4. **동작**: `start_booking.bat` 경로 지정 (예: `C:\\Users\\사용자이름\\autoBooking\\start_booking.bat`)  
5. 완료 후, 스크립트가 매주 자동으로 실행됩니다 

---

## 📁 디렉토리 구조

```
autoBooking/
├── auto_booking.py                # 예약 전체 실행 메인 파일
├── start_booking.sh               # macOS/Linux 실행용 스크립트
├── start_booking.bat              # Windows 실행용 스크립트
│
├── steps/                         # STEP별 모듈화된 기능
│   ├── access_page.py             # STEP 1 - 예약 페이지 접속
│   ├── select_date.py             # STEP 2 - 날짜 탐색 및 ○예약 클릭
│   ├── select_time.py             # STEP 3 - 시간 선택 (예: 9–11시)
│   ├── fill_form.py               # STEP 4 - 이름, 전화번호, 이메일 입력
│   └── confirm_final.py           # STEP 5 - 최종 예약 버튼 클릭
│
├── info.env.example               # 환경변수 템플릿
├── requirements.txt               # 의존 패키지 목록
├── .gitignore                     # Git 제외 설정
└── README.md                      # 설명서 (Korean)
```

---

## 📌 버전 기록

| 날짜       | 버전   | 변경 내용                               |
|------------|--------|------------------------------------------|
| 2025-04-09 | 1.0.0  | 첫 배포 (Selenium 기반)                  |
| 2025-04-13 | 1.0.1  | Selenium 기반 속도 개선 |
| 2025-04-14 | 2.0.0  | Playwright 버전 도입 및 속도 개선 |

---

## ✅ 라이선스 및 제작자

- Maintained by [kurooru]  
- License: kurooru