# Saylog Design Skills Repository Migration

## Goal

분산된 `agent-skills` 저장소에서 Dou 제품에 직접 의존하는 세 skill을 별도 private 저장소인 `saylog-design-skills`로 이동하고, 두 저장소의 README가 실제 설치 경로와 의존성을 정확히 설명하도록 정리한다.

## Scope

새 저장소로 이동하는 skill은 다음 세 가지다.

- `dou-product-design/`
- `dou-uxui-issues/`
- `manual-authoring/`

각 디렉터리의 `SKILL.md`, 참조 문서, 가이드, assets, scripts, agent metadata를 함께 보존한다. 원본 저장소의 다른 skill은 유지한다.

## Repository layout

새 저장소는 다음 구조를 갖는다.

```text
saylog-design-skills/
├── README.md
├── docs/superpowers/specs/2026-08-03-saylog-design-skills-migration-design.md
└── skills/
    ├── dou-product-design/
    ├── dou-uxui-issues/
    └── manual-authoring/
```

원본 `agent-skills/README.md`에서는 이동된 세 skill의 목록 행과 설치 안내를 제거해 깨진 링크가 남지 않게 한다.

## Dependency model

- `dou-product-design`은 Dou 제품의 `dou-design-system`과 제품 저장소의 `docs/design-harness.md`, `docs/ia.md`를 작업 전제조건으로 사용한다.
- GitHub 이슈를 연결하는 경우 `dou-uxui-issues`의 규칙과 GitHub 접근 권한이 필요하다.
- `dou-uxui-issues`는 Saylog/Carevoice 관련 private GitHub 저장소와 제품 영역별 디자인 기준 저장소를 참조한다.
- `manual-authoring`은 Saylog 매뉴얼 작업 시 `douinc/carevoice`의 문서와 `douinc/saylog-manuals` 저장소를 참조한다.
- `npx skills add`는 새 저장소의 skill 파일을 설치할 뿐, 위 외부 private 저장소를 자동으로 설치하거나 인증하지 않는다. README에 이 권한 요구사항을 명시한다.

## README content

새 README는 다음을 포함한다.

1. 저장소 목적과 private 저장소 접근 조건
2. SSH 기반 설치 명령과 특정 skill 설치 예시
3. 세 skill의 역할 표
4. skill 간 의존성 및 외부 제품 저장소 권한 표
5. skill 디렉터리 구조와 기여 방법
6. MIT 라이선스 안내

## Verification

이동 후 다음을 확인한다.

- 새 저장소에 세 skill의 모든 파일이 존재한다.
- 원본 저장소에는 세 skill 디렉터리가 더 이상 존재하지 않는다.
- 원본 README에 이동된 skill을 가리키는 링크나 `douinc/agent-skills` 설치 명령이 남아 있지 않다.
- 새 README의 상대 링크가 실제 파일과 일치한다.
- 두 저장소의 Git 상태와 변경 목록이 의도한 이동·삭제·README 변경만 포함한다.
