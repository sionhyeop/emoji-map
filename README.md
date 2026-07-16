# 🗺️ EmojiMap — 한눈에 보는 이모지 지도

광고 없이, 한 페이지에서 모든 이모지를 탐색·검색·복사할 수 있는 정적 사이트입니다.

## 특징
- **한 페이지 지도**: Unicode 17.0 기준 1,914개 이모지(+스킨톤 변형 1,900개)를 섹션 이동 없이 스크롤/카테고리 내비로 탐색
- **한국어·영어 검색**: CLDR 공식 키워드 주석 기반 (`하트`, `party`, `고양이`, `ㅎㅎ` 등)
- **무드 추천 컬렉션**: 축하 · 사랑 · 감사/사과 · 웃김 · 위로 · 응원 · 업무 · 먹방 · 여행 · 피곤 · 취미 · 계절 — 상황별 큐레이션
- **클릭 한 번 복사** + 최근 사용 / ⭐ 즐겨찾기 (localStorage)
- **스킨톤 전역 선택**: 지도 전체가 선택한 톤으로 표시
- **상세 패널**: 한/영 이름, 유니코드 버전, 스킨톤 변형, 비슷한 이모지 추천
- **이모지 조합 바구니**: 여러 개 모아 한 번에 복사 (예: 🎉🥳🎂)
- **다크 모드**, `/` 키로 검색 포커스, 🎲 랜덤 이모지

## 데이터
- [Unicode emoji-test.txt](https://unicode.org/Public/emoji/latest/emoji-test.txt) (v17.0)
- [CLDR annotations](https://github.com/unicode-org/cldr-json) (en/ko 이름·검색 키워드)

`python3 build_data.py` 로 `docs/emoji-data.js` 재생성.

## 배포
GitHub Pages — `docs/` 디렉터리 서빙. 순수 정적(HTML+JS 2파일), 빌드 불필요.
