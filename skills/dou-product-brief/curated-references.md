# Curated Design System References

Phase 3에서 사용하는 **도메인 × 화면 패턴** 룩업 테이블.
`awesome-design-systems` 400+ 항목에서 실무 자주 쓰일 것들을 선별한 **씨앗(seed)**이다. 실제 써보고 별로면 교체, 좋았던 건 추가한다.

---

## 1. 도메인별 추천

| 도메인 | 1순위 | 2순위 | 링크 / 특징 |
|--------|-------|-------|------------|
| 의료·헬스케어 | NHS Design System | IBM Carbon | nhs.uk/service-manual · 환자 안전·접근성 톤 |
| 의료 데이터 대시보드 | IBM Carbon | Salesforce Lightning | carbondesignsystem.com · 테이블·차트 밀도 |
| 핀테크·금융 | Goldman Sachs UI Toolkit | Monzo | design.gs.com · 수치·거래 표기 |
| 엔터프라이즈 SaaS | Atlassian | Shopify Polaris | atlassian.design · 폼·설정 밀도 |
| B2B 어드민 | Ant Design | Salesforce Lightning | ant.design · 테이블·필터·트리 |
| 컨슈머 앱 (iOS) | Apple HIG | Airbnb DLS | developer.apple.com/design · 시스템 네이티브감 |
| 컨슈머 앱 (Android) | Material 3 | Google Fit | m3.material.io · 동적 컬러 |
| 정부·공공 | GOV.UK | US Web Design System | design-system.service.gov.uk · 단순·명료 |
| 교육 | Khan Academy | Duolingo | · 단계 표시·동기부여 톤 |
| 커머스 | Shopify Polaris | Wayfair Homebase | polaris.shopify.com · 상품·재고 |
| 워치·웨어러블 | Apple HIG Watch | Wear OS | · 글랜스·단일 태스크 |
| 뉴스·콘텐츠 | BBC GEL | NYT Customs | bbc.co.uk/gel · 타이포·가독성 |

---

## 2. 화면 패턴별 추천

| 패턴 | 먼저 볼 디자인 시스템 | 참고 포인트 |
|------|--------------------|-------------|
| 리스트 / 테이블 | Shopify Polaris, IBM Carbon | 정렬·필터·빈 상태 |
| 상세 화면 | Material 3, Apple HIG | 히어로 영역·하단 액션 |
| 폼 / 입력 | GOV.UK, Atlassian | 검증·인라인 에러·헬프 텍스트 |
| 온보딩 / 튜토리얼 | Material 3 Onboarding, Duolingo | 단계 진행·skip 전략 |
| 모달 / 바텀시트 | Apple HIG Sheets, Material Dialog | 포커스 트랩·핸들 |
| 대시보드 / 차트 | IBM Carbon Charts, Salesforce | 데이터 시각화·필터 |
| 빈 / 에러 / 로딩 | Shopify Polaris Empty, Atlassian | 톤·재시도 CTA |
| 설정 | Apple HIG Settings, Material | 그룹핑·토글·보조 설명 |
| 검색 / 필터 | Airbnb, Booking | 자동완성·최근 검색 |
| 리뷰 / 피드백 | Airbnb, App Store | 별점·텍스트 조합 |
| 결제 / 체크아웃 | Shopify, Stripe | 단계·안전성 신호 |
| 알림 / 배지 | Slack, Discord | 읽음·우선순위 |
| 프로필 / 계정 | Instagram, LinkedIn | 아바타·bio·탭 |
| 채팅 / 메시지 | iMessage HIG, WhatsApp | 버블·상태 |
| 지도 / 위치 | Airbnb, Uber | 핀·클러스터 |
| 회원가입 / 인증 | Auth0, GOV.UK | 단계·에러·복구 경로 |
| 권한 / 역할 분기 | Atlassian, Salesforce | 비활성 표기·접근 거부 화면 |

---

## 3. Voice & Tone 참고 (문구 작성)

| 톤 | 참고 |
|----|------|
| 전문·임상 | NHS Design System Content, Mayo Clinic |
| 친근·가벼움 | Mailchimp Voice & Tone, Duolingo |
| 공식·정확 | GOV.UK Content Style, US Web |
| 간결·브랜드 | Shopify Voice, Atlassian Writing |

---

## 4. 컴포넌트 레벨 레퍼런스 (코드 있음 — 개발팀 공유용)

| 컴포넌트 목적 | 참고 라이브러리 |
|--------------|--------------|
| 접근성 우선 React 프리미티브 | Radix UI |
| 스타일 프리셋 React | shadcn/ui |
| Flutter 컴포넌트 | Material 3 for Flutter, Fluent UI |
| 디자인 토큰 관리 | Style Dictionary, Figma Variables |

---

## 5. 확장 규칙

새 항목 추가 시:

1. 해당 도메인 또는 패턴 행에 추가.
2. **한 줄 이내**로 특징 기재. 장황하게 쓰지 말 것 (스킬 문서 크기 유지).
3. 공개 URL 있으면 링크. 유료·가입 필요 사이트는 `(로그인 필요)` 표시.
4. 세 번 이상 참고했으면 테이블 상단으로 이동 (자주 쓰는 것 우선).

제거 규칙: 6개월간 한 번도 참고 안 한 항목은 제거.

---

## 6. 대형 레퍼런스 리스트 (검색용)

본 스킬 베이스가 된 종합 리스트: https://github.com/alexpate/awesome-design-systems
  
해당 리포에서 필터:

- **Components** 태그: 코드·사용 예시 제공
- **Voice & Tone** 태그: 문구 톤 가이드 제공
- **Designers Kit** 태그: Figma/Sketch 파일 공개
- **Source code** 태그: 오픈 소스

Phase 3에서 WebSearch로 보강할 때 이 리포를 `site:github.com/alexpate/awesome-design-systems <domain>` 형태로 검색하면 후보 찾기 쉬움.
