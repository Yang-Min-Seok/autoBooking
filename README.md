# 니이가타 배드민턴 자동 예약 시스템

니이가타시 스포츠 시설 배드민턴 코트를 자동으로 예약하는 Python 프로그램입니다.

## 주요 기능

- 원하는 날짜(오늘 기준 7일 뒤)와 시간대의 배드민턴 코트 자동 예약
- 예약 가능한 코트 자동 검색 및 여러 코트 동시 예약 (COURT_NO 지정)
- FACILITY_NAME, FACILITY_ID 키워드 자동 매핑 지원 (예: HIGASHI, KITA 등)
- CSRF 토큰 자동 처리 및 예약 성공 여부 로깅
- 빠른 예약 처리 (1~2초 내)

## 설치 방법

### 1. Python 설치
Python 3.7 이상이 필요합니다.

### 2. 필요한 라이브러리 설치 (가상환경 권장)
권장: 프로젝트별 격리를 위해 `venv` 가상환경을 만들고 그 안에 라이브러리를 설치하세요.

```bash
# macOS / Linux
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Windows (PowerShell)
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

참고: 시스템(글로벌) 파이썬에 직접 설치하는 대신 가상환경을 사용하는 것을 권장합니다. `start_booking.sh`와 `start_booking.bat`는 기본적으로 `./venv` 내부의 파이썬을 사용하려 시도하며, 필요하면 환경변수 `VENV_PYTHON`으로 경로를 지정할 수 있습니다.

## 전체 환경 구축

아래는 전체 환경을 처음부터 구성하는 간단한 순서입니다.

1) 코드 클론/복사 및 작업 디렉터리로 이동

```bash
git clone <repo-url> /path/to/autoBooking
cd /path/to/autoBooking
```

2) Python 설치 및 의존성 설치

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

3) 설정 파일 생성 (브라우저 사용)

1) 프로젝트 루트에 있는 `USEME.html` 파일을 웹 브라우저로 엽니다 (파일 더블클릭 또는 브라우저에서 열기).

2) 폼을 작성한 뒤 "설정 저장" 버튼을 누르면 브라우저의 다운로드 폴더(예: `~/Downloads`)에 `my_data.json` 파일이 생성됩니다.

3) 생성된 `my_data.json` 파일을 프로젝트 폴더로 이동합니다. 예:

```bash
# macOS / Linux 예시 (경로는 실제 사용자 환경에 맞게 수정하세요)
mv ~/Downloads/my_data.json /path/to/autoBooking/my_data.json
# 또는 복사
cp ~/Downloads/my_data.json /path/to/autoBooking/my_data.json
```

참고: `USEME.html`을 열면 브라우저에서 직접 설정 파일을 만들 수 있으므로 별도의 샘플 복사 과정이 필요하지 않습니다.

4) 로그 디렉터리 확인

```bash
mkdir -p logs
```

## start_booking 실행 및 예약 방법

`start_booking.sh`은 예약을 시작하기 위한 스크립트입니다. 보통 cron에서 실행하도록 설정합니다. 스크립트는 내부적으로 07:00까지 대기하도록 구현되어 있으므로, 예약을 안정적으로 시작하려면 약간 앞서 실행되게 cron에 등록하세요.

1) 스크립트 권한 부여 및 수동 실행 테스트

```bash
chmod +x start_booking.sh
sh start_booking.sh
```

2) crontab에 등록 (예: 매주 토요일 06:59에 실행)

```bash
crontab -e

# 매주 토요일 06:59에 실행
# 주의: `main.py`는 자체적으로 `logs/reservation.log`에 로그를 남깁니다.
# 따라서 crontab에서 별도 로그 리다이렉션을 하지 않아도 됩니다.
59 6 * * 6 cd /Users/<your-username>/Desktop/autoBooking && sh start_booking.sh
```

3) 등록 확인

```bash
crontab -l
```

참고:
- crontab에서 실행 시 절대 경로를 사용하세요. 가상환경을 사용하는 경우 `cd` 후 `source venv/bin/activate`를 추가하거나 스크립트 내에 가상환경 활성화 로직을 넣어주세요.
- 스크립트를 07:00 전에 실행하면 `main.py`의 내부 대기 로직이 정확히 07:00에 예약 프로세스를 시작합니다.

## nightly_update 실행 및 예약 방법

자동 업데이트 스크립트인 `nightly_update.sh`는 매주 또는 매일 정기적으로 실행하도록 cron에 등록할 수 있습니다.

1) 스크립트 권한 부여 및 수동 실행 테스트

```bash
chmod +x nightly_update.sh
sh nightly_update.sh
```

2) crontab 예시 (매일 01:00에 실행)

```bash
crontab -e

# 매일 01:00에 실행: 디렉터리 이동 후 스크립트 실행
# `nightly_update.sh` 출력이 필요하면 파일로 리다이렉트하시되,
# 예약 로그는 `main.py`가 담당하므로 기본적으로는 리다이렉트 불필요합니다.
0 1 * * * cd /Users/<your-username>/Desktop/autoBooking && sh nightly_update.sh
```

3) 등록 확인

```bash
crontab -l
```

---

### 실행 결과 확인

콘솔 및 `logs/reservation.log` 또는 `logs/nightly_update.log`에서 결과를 확인하세요. 문제가 있을 경우 로그의 에러 메시지를 기준으로 디버깅합니다.

## 프로그램 구조

```
├── main.py                    # 메인 실행 파일
├── modules/
│   ├── get_date_id.py            # 날짜 ID 조회 모듈
│   ├── get_reservation_ids.py    # 예약 가능한 코트 조회 모듈
│   └── niigata_macro.py          # 예약 실행 모듈
├── USEME.html                    # 브라우저에서 my_data.json을 생성하는 폼
├── start_booking.sh              # 예약 실행 스크립트 (cron 용)
├── nightly_update.sh             # 자동 업데이트 스크립트 (cron 또는 수동 실행)
├── requirements.txt              # 필요한 라이브러리 목록
├── README.md                     # 사용 설명서
└── reservation.log               # 실행 로그 (자동 생성)
```

## 작동 원리

1. **날짜 ID 조회**: 예약하려는 날짜(오늘+5일)의 고유 ID를 웹사이트에서 조회
2. **코트 검색**: 해당 날짜와 시간대에 예약 가능한 코트 검색
3. **CSRF 토큰 획득**: 예약 페이지에서 보안 토큰 획득
4. **예약 확인/실행**: 예약 정보를 전송하여 예약 완료

## 예약 가능 시간대

- 9-11시
- 11-13시
- 13-15시
- 15-17시
- 17-19시
- 19-21시

## 주의사항

⚠️ **중요한 제한사항**

1. **Rate Limit**: 웹사이트는 분당 약 5회 요청 제한이 있습니다. 너무 자주 실행하면 429 에러가 발생할 수 있습니다.
2. **예약 가능 기간**: 웹사이트의 예약 가능 기간 정책을 따릅니다.
3. **중복 예약 방지**: 이미 예약된 코트는 자동으로 예약할 수 없습니다.
4. **코트 선택**: 여러 코트가 비어있을 경우 COURT_NO만큼 순서대로 예약합니다.

## 문제 해결

### 예약 가능한 코트가 없다고 나올 때
- 해당 시간대의 모든 코트가 이미 예약된 상태입니다.
- 다른 시간대를 선택하거나 다른 날짜를 시도해보세요.

### 429 에러가 발생할 때
- 너무 많은 요청을 보낸 경우입니다.
- 30초~1분 정도 기다린 후 다시 시도하세요.

### CSRF 토큰 오류
- 웹사이트 세션이 만료된 경우입니다.
- 프로그램을 다시 실행하면 자동으로 해결됩니다.

### ValueError: too many values to unpack
- `get_reservation_ids.py` 파일이 업데이트되지 않은 경우입니다.
- 최신 버전의 파일로 교체해주세요.

## 로그 확인

`reservation.log` 파일에서 다음 정보를 확인할 수 있습니다:
- 날짜 ID 조회 결과
- 예약 가능한 코트 목록 (코트 번호 포함)
- 선택된 코트 정보
- CSRF 토큰 획득 여부
- 예약 요청 응답 코드
- 예약 성공/실패 여부
- 총 소요 시간

**로그 예시:**
```
2025-10-12 01:42:02,844 - INFO - 예약 가능한 코트들: ['バドミントン 1 (ID: 250514)', 'バドミントン 2 (ID: 250521)']
2025-10-12 01:42:02,844 - INFO - 선택된 코트: バドミントン 1 (ID: 250514)
2025-10-12 01:42:02,844 - INFO - 예약 완료 - 코트: バドミントン 1
2025-10-12 01:42:02,845 - INFO - === 예약이 성공적으로 완료되었습니다! ===
2025-10-12 01:42:02,845 - INFO - 예약된 코트: バドミントン 1
2025-10-12 01:42:02,845 - INFO - 총 소요 시간: 1.56초
```

## 성공 예시

```
[성공] 예약이 성공적으로 완료되었습니다!
예약 코트: バドミントン 1
소요시간: 1.56초
```

## 📌 버전 기록

| 날짜 | 버전 | 변경 내용 |
|---|---:|---|
| 2025-04-09 | 1.0.0 | 첫 배포 (Selenium 기반) |
| 2025-04-13 | 1.0.1 | Selenium 기반 속도 개선 |
| 2025-04-14 | 2.0.0 | Playwright 버전 도입 및 속도 개선 |
| 2025-04-19 | 2.0.1 | 코트, 시간 지정 기능 추가, 매직넘버 변수화 |
| 2025-04-23 | 2.1.1 | 체육관 지정 기능 추가(카메다), 예약 실패 반응 속도 단축 |
| 2025-05-10 | 2.2.0 | 체육관 옵션 추가(토야노) |
| 2025-06-02 | 2.2.1 | 에러 대응, 안정성 형상 |
| 2025-06-28 | 3.0.0 | 다중 코트 대응(3코트까지), 속도 개선 |
| 2025-07-26 | 3.1.0 | 체육관 옵션 추가(西, 北), 날짜 버그 개선 |
| 2025-07-27 | 3.2.0 | nightly update 기능 추가 |
| 2025-10-12 | 4.0.0 | api기반 속도 개선 |
| 2025-10-12 | 4.1.0 | 자동화 툴 제공 (start_booking, nightly_update) |
| 2025-10-18 | 4.2.0 | 예약 안정성 강화 (1분전 시작, 남은 시간 계산방식으로 변경), 월말시점 월초 예약 대응 |
| 2025-11-09 | 4.3.0 | json파일 생성 브라우저 제공 |
| 2025-12-07 | 4.4.0 | 3코트 동시 예약 대응 (테스트용) |

## ✅ 라이선스 및 제작자

- Maintained by [kurooru]
- License: kurooru

## 📔 개발 일지

[개발 일지 (Notion)](https://www.notion.so/NEMMY-DARRY-MENDY-208b163aeba780e09715c8992b99829a?source=copy_link)