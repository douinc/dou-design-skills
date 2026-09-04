# product-config 예시

프로젝트 루트의 `CLAUDE.md`에 아래 블록을 추가하면 `product-design-workflow` 스킬이 자동으로 읽는다.

---

## 최소 구성

```yaml
product_design_workflow:
  product_name: <프로덕트명>
  domain_guide: <도메인 가이드 파일 경로 (프로젝트 루트 기준 상대경로)>
  planning_docs_location: <기획문서 저장 폴더 (프로젝트 루트 기준 상대경로)>
  ux_writing_skill: <UX 라이팅 스킬명>  # 선택 — 프로젝트별 UX 라이팅 가이드
  design_skills:
    mobile: <모바일 디자인 스킬명>
    # watch, web 은 있는 것만
```

---

## 예시 1 — 새록

```yaml
product_design_workflow:
  product_name: 새록
  domain_guide: docs/domain/domain-guide.md
  planning_docs_location: docs/planning/
  design_skills:
    mobile: saylog-mobile-design
    watch: saylog-watch-design
```

## 예시 2 — 단일 플랫폼 서비스

```yaml
product_design_workflow:
  product_name: FooApp
  domain_guide: docs/foo-domain.md
  planning_docs_location: docs/specs/
  design_skills:
    web: fooapp-web-design
```

---

## 필드 설명

| 필드 | 필수 | 설명 |
|------|------|------|
| `product_name` | ✅ | 리포트·문서 헤더 표기용 |
| `domain_guide` | ✅ | Phase 1·1.5에서 읽는 정책/규칙 문서. 스킬은 read-only로만 접근 |
| `planning_docs_location` | ✅ | Phase 1 기획문서가 저장될 폴더. 없으면 자동 생성 요청 |
| `ux_writing_skill` | ❌ | Phase 2 화면 상담 시 적용할 UX 라이팅 스킬명. 미설정 시 라이팅 검수 없이 진행 |
| `design_skills.<platform>` | ≥1 | 플랫폼별 핸드오프 대상 스킬명. `mobile/watch/web` 중 해당 프로덕트에 있는 것만 |

---

## 작동 방식

1. 스킬이 cwd부터 상위로 올라가며 `CLAUDE.md`를 탐색.
2. 파일 안에서 `product_design_workflow:` 블록을 찾음.
3. 값 로드 후 사용자에게 1줄로 요약 보고.
4. 여러 CLAUDE.md가 발견되면 **가장 가까운(cwd에 가까운) 것** 우선.

설정이 없는 프로젝트에서 스킬을 호출하면 대화로 값을 수집한 뒤 이 블록을 프로젝트 루트 `CLAUDE.md`에 append한다.
