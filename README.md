# 新潟市スポーツ施設自動予約マクロ

新潟市のスポーツ施設の自動予約を実行するPythonマクロです。

## 機能

- 자동 예약 실행
- CSRF 토큰 자동 처리
- 세션 관리
- confirm 모드에서 send 모드로 자동 전환

## インストール

1. Python 3.7 이상이 설치되어 있는지 확인하세요.

2. 필요한 패키지를 설치하세요:
```bash
pip install -r requirements.txt
```

## 使用方法

### 기본 실행
```bash
python niigata_macro.py
```

### 예약 정보 수정
`niigata_macro.py` 파일의 `main()` 함수에서 예약 정보를 수정하세요:

```python
success = macro.make_reservation(
    course_time_id=250345,           # 코스 시간 ID
    facility_name='鳥屋野総合体育館',  # 시설명
    facility_id=420,                # 시설 ID
    date='2025年10月15日（水）',       # 예약 날짜
    equipment='バドミントン',         # 장비
    course_name='バドミントン 1',     # 코스명
    course_time_name='9-11時',       # 시간대
    name='apple',                    # 예약자명
    tel='0123456789',               # 전화번호
    email='jeongwonjun0718@gmail.com' # 이메일
)
```

## 작동 원리

1. **CSRF 토큰 획득**: 예약 페이지에 접근하여 CSRF 토큰을 획득
2. **Confirm 모드**: 예약 정보를 confirm 모드로 전송
3. **예약자 정보 페이지**: 예약자 정보 입력 페이지로 이동
4. **Send 모드**: 폼 데이터를 수집하여 send 모드로 예약 실행

## 파일 구조

```
.
├── niigata_macro.py      # 메인 매크로
├── advanced_macro.py     # 고급 기능 매크로 (선택사항)
├── config.json          # 설정 파일 (선택사항)
├── requirements.txt     # 필요한 패키지 목록
├── README.md           # 사용 설명서
└── reservation.log     # 실행 로그 (자동 생성)
```

## 注意事項

1. **Rate Limit**: 新潟市のサイトは分당 5회 요청 제한이 있습니다.
2. **CSRF 토큰**: 매 요청마다 새로운 CSRF 토큰이 필요합니다.
3. **세션 관리**: 세션 쿠키를 올바르게 관리해야 합니다.

## トラブルシューティング

### 일반적인 문제

1. **CSRF 토큰 오류**
   - 예약 페이지에 먼저 접근하여 토큰을 획득하세요.

2. **세션 만료**
   - 프로그램을 재시작하거나 세션을 갱신하세요.

3. **Rate Limit 초과**
   - 요청 간격을 늘리거나 재시도 간격을 조정하세요.

### 로그 확인

실행 로그는 `reservation.log` 파일에 저장됩니다. 문제 발생 시 이 파일을 확인하세요.

## 免責事項

이 도구는 교육 목적으로 제작되었습니다. 사용자는 해당 사이트의 이용약관을 준수할 책임이 있으며, 사용으로 인한 모든 결과에 대해 사용자가 책임집니다.
