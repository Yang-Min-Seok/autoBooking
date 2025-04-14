# 📅 자동 예약 매크로 시스템 (autoBooking) KOREAN(🇰🇷)

웹사이트 예약을 자동으로 수행하는 Python 기반 자동화 스크립트입니다.  
Selenium을 활용해 브라우저를 조작하고, `.env`로 개인정보를 관리하며, cron 또는 작업 스케줄러로 정기 실행이 가능합니다.

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
```

---

### 환경변수 설정

```bash
cp info.env.example info.env        # macOS / Linux
copy info.env.example info.env      # Windows
```

`info.env` 파일을 열어 아래 값을 입력해 주세요.

```env
TARGET_URL=https://example.com/reservation
NAME=홍길동
PHONE_NUMBER=01012345678
E_MAIL=test@example.com
```

---

## 🧪 실행 전 테스트 (브라우저 작동 확인)

> 실제 자동 예약을 수행하기 전, 브라우저가 정상 실행되는지 테스트해보세요.

### macOS / Linux / Git Bash

```bash
chmod +x test_run.sh
./test_run.sh
```

### Windows

```cmd
test_run.bat
```

---

## 🚀 자동 예약 실행

### macOS / Linux / Git Bash

```bash
chmod +x run.sh
./run.sh
```

### Windows

```cmd
run.bat
```

---

## 🕑 자동 실행 예약

### macOS (cron 사용) / Git Bash

```bash
crontab -e
```

아래 라인 추가 (매주 토요일 오전 7시 실행):

```cron
0 7 * * 6 /Users/yourname/autoBooking/run.sh >> /Users/yourname/autoBooking/cron.log 2>&1
```

### Windows (작업 스케줄러 사용)

1. 작업 스케줄러 열기  
2. 새 작업 생성  
3. 트리거: 매주 토요일 오전 7시  
4. 동작: `run.bat` 실행 경로 지정

---

## 📁 디렉토리 구조

```
autoBooking/
├── main.py                  # 예약 자동화 메인 실행 스크립트
├── run.sh                   # macOS/Linux 실행용
├── run.bat                  # Windows 실행용
├── test_run.sh              # 테스트 실행 (.sh)
├── test_run.bat             # 테스트 실행 (.bat)
│
├── step1_access_url.py      # STEP 1 - 예약 페이지 접속
├── step2_select_date.py     # STEP 2 - 날짜 선택 및 ○예약 클릭
├── step3_select_time.py     # STEP 3 - 시간 선택 (예: 9–11시)
├── step4_input_form.py      # STEP 4 - 이름, 전화번호, 이메일 입력
├── step5_confirm.py         # STEP 5 - 최종 예약 버튼 클릭
├── step6_wait.py            # STEP 6 - 최종 예약 대기 (5초)
├── utils.py                 # 공통 함수 모듈 (드라이버 설정 등)
│
├── info.env.example         # 환경변수 예시 템플릿
├── requirements.txt         # 패키지 목록
├── .gitignore               # Git 제외 설정
└── README.md                # 한국어 설명서
```

---

## 📌 버전 기록

| 날짜       | 버전   | 변경 내용                    |
|------------|--------|------------------------------|
| 2025-04-09 | 1.0.0  | 첫 배포 (모듈화 완료, 수정 없음) |
| 2025-04-13 | 1.0.1  | 속도 개선 |

---

## ✅ 라이선스 및 제작자

- Maintained by [kurooru]  
- License: kurooru