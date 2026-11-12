# 채팀장 SNS 예약발행

블로그 글 → 인스타 카드뉴스 + 쓰레드 글로 변환해서 예약 시간에 자동 발행합니다.

- `posts/<글이름>/post.json` : 발행 시각(`publish_at`), 인스타 캡션·이미지, 쓰레드 글 목록
- `posts/<글이름>/card_XX.jpg` : 카드뉴스 이미지 (1080×1350)
- `posts/<글이름>/published.json` : 발행 기록 (자동 생성, 중복 발행 방지)
- `tools/render.py` : 카드뉴스 디자인 템플릿
- `.github/workflows/publish.yml` : 30분마다 예약 확인 후 발행

## 필요한 설정 (Settings → Secrets and variables → Actions)
- Secrets: `IG_TOKEN` (인스타 시스템 사용자 토큰), `THREADS_TOKEN` (쓰레드 토큰, 선택)
- Variables: `IG_USER_ID` = 17841459229578016

## 수동 점검
Actions → SNS 예약발행 → Run workflow (점검만 하기 체크 시 실제 발행 안 함)
