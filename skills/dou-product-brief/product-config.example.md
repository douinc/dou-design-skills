# design_config 예시

프로젝트 루트의 `CLAUDE.md`에 `design_config:` 블록을 두면 이 스킬이 Phase 0에서 자동으로 읽는다.
블록이 없으면 대화로 값을 물어본 뒤 같은 위치에 append한다.

---

## 최소 구성 — 이 스킬이 쓰는 값

```yaml
design_config:
  product_name: <제품명>
  domain_guide: <DCX GitHub URL 또는 로컬 파일 경로>
  planning_docs_location: <기획 산출물 루트>
  ux_writing_skill: <UX 라이팅 스킬명>
```

---

## 예시 1 — 새록 (실제 사용 중)

화면 작업(`dou-product-design`)까지 한 리포에서 이어가는 구성이다. 아래 절반은 그 스킬이 읽는다.

```yaml
design_config:
  product_name: 새록 (Saylog)
  domain_guide: https://github.com/douinc/dcx/tree/main/01-products/saylog
  planning_docs_location: docs/planning/   # 기획서(plan.md·IA·브리프). 화면 문서는 docs/screens/
  stack: Next.js + Bun + React + TypeScript + @dou/ui
  components: "@dou/ui (import해서 사용. shadcn 재설치/재구현 금지)"
  design_system: docs/design-system/   # DESIGN.md(규칙) · components.md · tokens.json
  icons: "@tabler/icons-react (Icon* 형식, outline / 활성 filled)"
  ux_writing_skill: saylog-ux-writing-korean
  local: "bun run dev → http://localhost:3100"
```

## 예시 2 — 도메인 문서가 아직 없는 신규 제품

DCX에 제품 폴더가 없는 것은 0부터 시작하는 제품에선 정상이다. `domain_guide`를 비워두고
시작하면 Phase 1에서 도메인 가이드를 함께 만든다(§3.1).

```yaml
design_config:
  product_name: FooApp
  domain_guide:            # 아직 없음 — Phase 1에서 생성
  planning_docs_location: docs/planning/
  ux_writing_skill: ux-writing-korean
```

---

## 필드 설명

| 필드 | 필수 | 설명 |
|------|------|------|
| `product_name` | ✅ | 문서 머리말·보고 표기용 |
| `domain_guide` | ✅ | Phase 1에서 읽는 제품 정책·도메인 문서. 읽기 전용으로만 접근한다. 신규 제품이면 비워둘 수 있다 |
| `planning_docs_location` | ✅ | `plan.md`·`ia.md`·브리프가 저장될 폴더. 없으면 생성을 요청한다 |
| `ux_writing_skill` | ✅ | 문구를 쓰거나 고칠 때 먼저 invoke할 스킬명 |

`stack` · `components` · `design_system` · `icons` · `local`은 이 스킬이 쓰지 않는다.
화면을 만드는 `dou-product-design`이 읽는 값이라, 같은 리포에서 화면까지 이어간다면 함께 적어둔다.

### domain_guide 값 형식

- **DCX GitHub URL (권장)**: `https://github.com/douinc/dcx/tree/main/01-products/<제품명>`
  — 팀 전체가 공유하는 공식 기준이라 로컬 파일보다 우선한다.
- **로컬 파일 경로**: `domain/<파일명>.md` — DCX에 문서가 없을 때만.

---

## 작동 방식

1. cwd부터 상위로 올라가며 `CLAUDE.md`를 탐색한다.
2. 파일 안에서 `design_config:` 블록을 찾는다.
3. 값을 읽고 한 줄로 요약 보고한 뒤 Phase 1 진행 여부를 확인한다.
4. `CLAUDE.md`가 여러 개면 **cwd에 가장 가까운 것**이 이긴다.
