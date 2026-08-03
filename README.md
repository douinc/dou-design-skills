# Saylog Design Skills

Dou 제품의 디자인·UI/UX 이슈 관리·사용자 매뉴얼 제작에 사용하는 private agent skills 저장소입니다.

## 설치 전제조건

이 저장소는 private GitHub 저장소입니다. 설치하는 계정에 douinc/dou-design-skills 읽기 권한이 있어야 하며, GitHub SSH 키 또는 Git credential이 먼저 설정되어 있어야 합니다.

### 권장 설치 방법

SSH 인증을 사용하는 경우:

~~~bash
npx skills add git@github.com:douinc/dou-design-skills.git --skill <skill-name>
~~~

예:

~~~bash
npx skills add git@github.com:douinc/dou-design-skills.git --skill dou-product-design
~~~

### 저장소 shorthand

기존 npx skills 사용 규칙에 따라 다음 형식도 사용할 수 있습니다.

~~~bash
npx skills add douinc/dou-design-skills@<skill-name>
~~~

private 저장소를 clone할 수 있도록 인증되어 있지 않다면 shorthand가 실패할 수 있습니다. 그 경우 SSH URL 방식을 사용하세요.

dou-product-design에서 GitHub 이슈 연결 작업까지 하려면 두 skill을 함께 설치합니다.

~~~bash
npx skills add git@github.com:douinc/dou-design-skills.git --skill dou-product-design --skill saylog-uxui-issues
~~~

## Skill 목록

| Skill | 용도 |
| --- | --- |
| [dou-product-design](./skills/dou-product-design/) | Next.js + shadcn/ui 기반 Dou 제품 화면의 스펙·와이어프레임·직접 구현 워크플로우 |
| [saylog-uxui-issues](./skills/saylog-uxui-issues/) | Saylog 제품 UI/UX 이슈의 초안·등록, 하위 이슈 관계와 GitHub Project 상태 관리 |
| [saylog-manual-authoring](./skills/saylog-manual-authoring/) | Saylog 화면 스크린샷과 설명으로 A4 사용자 매뉴얼을 만들거나 수정하는 워크플로우 |

## Skill 간 의존성

### dou-product-design

- Dou 제품 저장소의 docs/design-harness.md와 docs/ia.md
- 프로젝트 설정의 product_design_workflow.design_system에 지정된 dou-design-system
- GitHub 이슈를 연결하는 작업에서는 saylog-uxui-issues 규칙과 GitHub 권한

### saylog-uxui-issues

제품 영역에 따라 다음 private 저장소를 확인하거나 이슈 등록 대상으로 사용합니다.

- douinc/saylog
- douinc/carevoice
- douinc/saylog-design
- douinc/saylog-console-design
- douinc/saylog-live

GitHub 이슈 생성·수정, 하위 이슈 연결, Project 상태 변경에는 해당 저장소와 Project에 필요한 권한이 있어야 합니다.

### saylog-manual-authoring

Saylog 매뉴얼 작업에는 다음 private 저장소가 필요합니다.

- douinc/carevoice의 docs/shared 컨텍스트 문서
- douinc/saylog-manuals의 매뉴얼 소스·산출물

또한 PDF 렌더링과 시각 검증을 위해 macOS의 Chrome과 Quartz 환경이 필요합니다.

## 외부 의존성 처리

npx skills add는 이 저장소의 SKILL.md와 포함된 참조 파일·스크립트만 설치합니다. 위에 적은 제품 저장소, 디자인 시스템, 매뉴얼 저장소를 자동으로 clone하거나 인증하지 않습니다.

skill을 설치한 뒤 제품 저장소의 지침에 따라 필요한 private 저장소를 직접 clone하거나 최신 상태로 동기화하세요. 외부 저장소의 접근 권한이나 인증이 없으면 skill 자체는 설치되어도 제품 컨텍스트를 읽어야 하는 작업은 완료할 수 없습니다.

## 디렉터리 구조

~~~text
dou-design-skills/
├── README.md
├── skills/
│   ├── dou-product-design/
│   ├── saylog-uxui-issues/
│   └── saylog-manual-authoring/
└── docs/
    └── superpowers/
        ├── plans/
        └── specs/
~~~

각 skill은 skills/<skill-name>/SKILL.md를 진입점으로 사용하며, 해당 디렉터리의 참조 문서·스크립트·asset은 skill과 함께 배포합니다.

## 기여

1. skills/<skill-name>/SKILL.md와 필요한 부속 파일을 수정하거나 새 skill 디렉터리를 추가합니다.
2. README의 Skill 목록과 의존성 설명을 변경사항에 맞게 갱신합니다.
3. git diff --check와 skill 설치 테스트를 실행합니다.
4. private 제품 저장소의 비밀값·토큰·개인정보를 skill 파일이나 문서에 커밋하지 않습니다.

## 라이선스

[MIT](./LICENSE)
