# Storix AGENTS Guide

## 목적

이 저장소의 AI 에이전트는 Storix MVP v1.0을 구현한다.

- Storix는 macOS 로컬 저장공간 분석 및 정리 도구다.
- 제공 인터페이스는 CLI + TUI다.
- 주 사용자층은 macOS 개발자와 power user다.
- 모든 구현은 "무엇이 용량을 많이 쓰는지", "무엇을 안전하게 지울 수 있는지", "얼마나 비울 수 있는지"를 빠르게 이해시키는 방향이어야 한다.

## 기준 문서

아래 문서를 항상 우선 참고한다.

- 제품 요구사항: `dev/storix_prd.md`
- 기술 설계: `dev/storix_tdd.md`

문서와 구현 요청이 충돌하거나 해석이 모호할 때는 아래 우선순위를 따른다.

1. 데이터 손실 방지와 안전한 기본값
2. CLI/TUI가 공통 서비스 계층을 재사용하는 구조
3. MVP 범위 유지
4. 확장보다 명확성, 자동 삭제보다 사용자 확인

## Repo Skills

이 저장소의 스킬은 두 위치에 존재한다. 에이전트에 따라 참조 경로가 다르다.

### Claude Code (`claude code` CLI)

- 스킬 위치: `.claude/skills/`
- `/스킬명` 으로 직접 호출하거나, 관련 작업 시 Claude가 자동으로 적용한다.

| 호출 | 용도 |
|------|------|
| `/storix-mvp-guardrails` | 기능 범위 판단, PRD/TDD 해석, 구조 결정, 리팩터링 방향 검토 |
| `/storix-clean-safety` | scan/doctor/clean, 위험도 분류, guard rule, 삭제 흐름, reclaimable size 계산 |
| `/storix-cli-tui-delivery` | Typer CLI, Rich 출력, Textual TUI, presenter, JSON/Markdown report 작업 |
| `/storix-test-patterns` | pytest, `tmp_path`, 스캐너/클리너/서비스 회귀 테스트, TUI 상태 테스트 작성 |

### Codex (`codex` CLI)

- 스킬 위치: `.codex/skills/`
- `codex` 실행 시 자동으로 탐색하며, 작업 유형에 맞는 스킬을 적용한다.

| 스킬명 | 용도 |
|--------|------|
| `storix-mvp-guardrails` | 기능 범위 판단, PRD/TDD 해석, 구조 결정, 리팩터링 방향 검토 |
| `storix-clean-safety` | scan/doctor/clean, 위험도 분류, guard rule, 삭제 흐름, reclaimable size 계산 |
| `storix-cli-tui-delivery` | Typer CLI, Rich 출력, Textual TUI, presenter, JSON/Markdown report 작업 |
| `storix-test-patterns` | pytest, `tmp_path`, 스캐너/클리너/서비스 회귀 테스트, TUI 상태 테스트 작성 |

### 조합 기준

여러 스킬이 동시에 필요한 경우 최소한의 조합만 사용한다.

- 구조 판단 + 구현: `storix-mvp-guardrails`
- 삭제/정리 로직 구현: `storix-clean-safety`
- 사용자 출력/화면 작업: `storix-cli-tui-delivery`
- 테스트 추가/수정: `storix-test-patterns`

## 제품 원칙

아래 원칙은 비타협 항목으로 취급한다.

- 먼저 보여주고, 그다음 지운다.
- 기본값은 항상 안전해야 한다.
- 위험한 항목은 자동으로 지우지 않는다.
- 삭제 전 예상 회수 용량을 보여준다.
- CLI와 TUI는 같은 비즈니스 로직을 공유한다.
- Storix는 단순 삭제 스크립트가 아니라 분석, 분류, 예측, 확인, 정리, 리포트 흐름을 제공해야 한다.

## MVP 범위

기본적으로 아래 범위 안에서 구현한다.

- 저장공간 개요 조회
- 카테고리별 스캔
- 정리 후보 탐지
- 위험도 분류: `safe`, `caution`, `dangerous`
- dry-run
- clean
- TUI
- JSON/Markdown 리포트

우선 지원해야 하는 카테고리:

- Xcode
- Android
- Flutter/Dart
- Node/Web
- Python
- VS Code
- General 사용자 폴더

우선 지원해야 하는 명령:

- `storix scan`
- `storix top`
- `storix doctor`
- `storix clean`
- `storix projects scan`
- `storix report`
- `storix tui`

명시적 요청이 없다면 아래는 기본 구현 범위에 넣지 않는다.

- Trash 이동 옵션
- 중복 파일 탐지
- iCloud local occupancy 대응
- scheduler 연동
- rule customization UI
- Linux 지원
- GUI 앱 확장

## 기술 기준

- 언어: Python 3.11+
- CLI: `Typer`
- 콘솔 출력: `Rich`
- TUI: `Textual`
- 파일 시스템 처리: `pathlib`, `os`, `shutil`
- 시스템 명령 실행: `subprocess`
- 데이터 모델링: `dataclasses` 또는 `pydantic`
- 직렬화: `json`, `pyyaml`
- 테스트: `pytest`, `pytest-mock`, `tmp_path`
- 패키징: `pyproject.toml` 기반, `pipx` 설치 가능 구조 유지

## 아키텍처 규칙

Storix는 UI와 비즈니스 로직을 분리한다.

- CLI와 TUI는 동일한 서비스 계층을 재사용해야 한다.
- 스캔, 분석, 정리, 위험도 판정 로직은 UI에 의존하면 안 된다.
- 출력 형식 차이는 presenter 계층에서 처리한다.
- dangerous path 보호는 공통 guard rule에서 처리한다.
- 새 기능을 추가할 때는 먼저 서비스/도메인 모델에 넣고, 이후 CLI/TUI에 연결한다.

권장 구조는 `dev/storix_tdd.md`의 모듈 구성을 따른다.

- `models/`: 후보, 요약, 결과, 리포트 모델
- `services/`: scan, doctor, clean, project, report orchestration
- `scanners/`: 카테고리별 탐지
- `cleaners/`: 카테고리별 정리 로직
- `presenters/`: console/json/markdown/tui adapter
- `tui/`: 화면, 위젯, 상태 관리
- `utils/`: fs, shell, size, guard, logger, confirm
- `rules/targets.yaml`: known path 및 규칙 정의

로직을 CLI 파일이나 TUI 화면 클래스 안에 직접 쌓아두지 않는다.

## 스캔 규칙

- 기본 스캔은 known path 우선으로 동작해야 한다.
- 사용자는 10초에서 30초 안에 주요 결과를 볼 수 있어야 한다.
- 전체 재귀 탐색은 옵션화한다.
- 경로가 존재하지 않거나 접근이 제한되면 전체 실행을 실패시키지 말고 부분 결과를 반환한다.
- macOS 중심 경로를 우선 지원한다.
- 프로젝트 스캔은 프로젝트 타입 감지와 산출물 탐지를 함께 제공해야 한다.

## 위험도 정책

### `safe`

재생성 가능한 캐시/빌드 산출물이다.

예:

- Xcode `DerivedData`
- `build`
- `.dart_tool`
- VS Code cache
- `workspaceStorage`

처리 규칙:

- 빠른 정리 대상이다.
- 자동화 대상이 될 수 있다.
- 그래도 삭제 전 목록과 예상 회수 용량은 보여준다.

### `caution`

재생성 가능하지만 시간 비용이나 환경 재구성이 필요한 항목이다.

예:

- Xcode Archives
- Android `system-images`
- AVD
- pub cache
- Gradle cache
- CocoaPods cache
- `ios/Pods`

처리 규칙:

- 추가 확인이 필요하다.
- 왜 주의가 필요한지 설명해야 한다.
- dry-run 없이 바로 지우는 흐름을 기본값으로 두지 않는다.

### `dangerous`

사용자 데이터나 원본 파일이 섞일 수 있는 항목이다.

예:

- `Downloads`
- `Desktop`
- `Documents`
- `Movies`
- 프로젝트 루트
- 사용자 원본 파일

처리 규칙:

- 기본 삭제 대상에서 제외한다.
- 자동 삭제에 포함하지 않는다.
- 공통 guard rule로 보호한다.
- 명시적 opt-in이 없는 한 clean 후보로 취급하지 않는다.

## 삭제 안전 규칙

- 모든 clean 흐름은 dry-run을 지원해야 한다.
- 삭제 전 대상 목록, 경로, 위험도, 예상 회수 용량을 보여줘야 한다.
- 실제 삭제는 공통 guard 검증을 통과한 뒤에만 수행한다.
- raw shell 삭제를 바로 호출하지 말고 공통 cleaner/guard 경유 구조를 사용한다.
- 부분 실패는 허용하되, 성공/실패 항목을 요약해 리포트해야 한다.
- root 권한이나 시스템 전체 접근을 전제로 설계하지 않는다.

## CLI 기준

- CLI는 스크립트 친화적이어야 한다.
- 사람이 읽기 쉬운 출력과 기계가 읽기 쉬운 출력 모두 지원한다.
- `--json`, `--markdown`, `--dry-run`, `--yes`, `--interactive` 같은 옵션은 일관되게 동작해야 한다.
- `doctor`는 카테고리별 reclaimable storage와 risk level 합계를 잘 보여줘야 한다.
- `clean all-safe --yes` 같은 자동화 시나리오를 해치지 않아야 한다.

## TUI 기준

TUI는 아래 UX를 충족해야 한다.

- 좌측: 카테고리 목록
- 중앙: 후보 목록
- 우측: 상세 설명
- 하단: 상태, 키바인드, 총 선택 용량

핵심 동작:

- 카테고리 탐색
- 항목 선택/해제
- 상세 패널 표시
- dry-run
- clean 실행
- 상태 피드백

핵심 원칙:

- 삭제 전에 항상 확인 흐름이 있어야 한다.
- 위험도는 시각적으로 명확히 구분되어야 한다.
- 선택된 항목의 총 확보 예상 용량이 즉시 보여야 한다.
- dry-run과 실제 clean은 명확히 구분되어야 한다.

예상 키바인드도 최대한 유지한다.

- `↑/↓`
- `←/→`
- `space`
- `a`
- `d`
- `c`
- `r`
- `f`
- `q`

## 출력과 리포트 기준

- 사용자에게는 경로, 크기, 위험도, 탐지 이유, 재생성 가능 여부, 주의사항을 가능한 한 함께 보여준다.
- 리포트는 JSON과 Markdown을 지원한다.
- 출력은 읽기 쉬워야 하며, 위험도 표현은 일관돼야 한다.

## 테스트 규칙

행동이 바뀌면 테스트도 같이 바꾼다.

- `pytest`를 기본으로 사용한다.
- 서비스 계층 테스트를 우선 작성한다.
- 파괴적 동작은 `tmp_path` 기반의 안전한 fixture로 검증한다.
- 다음 영역은 특히 테스트를 놓치지 않는다.
  - risk 분류
  - guard rule
  - dry-run
  - partial failure
  - project scan
  - TUI 상태 변화
- 경로 미존재, 접근 제한, 삭제 실패 상황도 검증한다.

## 성능과 사용성 기준

- 기본 스캔은 빠르게 주요 결과를 반환해야 한다.
- known path 기반 탐지를 우선한다.
- 전체 재귀 탐색은 opt-in이어야 한다.
- 출력은 사람이 빠르게 판단할 수 있어야 한다.
- 사용자는 3분 내에 주요 용량 사용처와 정리 후보를 이해할 수 있어야 한다.

## 배포 기준

- `pipx install storix`가 가능한 패키지 구조를 우선한다.
- PyPI 배포 친화적인 구조를 유지한다.
- Homebrew tap과 standalone binary는 확장 배포 경로로 고려하되, 기본 구현을 복잡하게 만들지 않는다.

## AI 작업 금지사항

아래 행동은 기본적으로 하지 않는다.

- dangerous 항목을 기본 삭제 경로에 포함하기
- guard를 우회하는 삭제 로직 작성
- dry-run 없는 clean 흐름 만들기
- CLI와 TUI에 중복 비즈니스 로직 복사하기
- macOS 전용 도구를 Linux 중심 구조로 바꾸기
- 차기 버전 범위를 MVP에 무단 포함하기
- 사용자가 이해할 수 없는 형태로 결과를 숨기기

## 작업 전 체크

작업을 시작하기 전에 아래 질문에 답할 수 있어야 한다.

- 이 변경이 Storix의 핵심 질문 다섯 가지에 도움이 되는가
- 이 변경이 macOS 개발자/파워유저의 정리 흐름을 더 안전하게 만드는가
- 이 변경이 공통 서비스 계층을 유지하는가
- 이 변경이 risk 정책과 guard 규칙을 지키는가
- 이 변경이 MVP 범위를 넘지 않는가

## 작업 완료 체크리스트

- 삭제 전 미리보기 또는 dry-run이 가능하다.
- 예상 회수 용량이 계산된다.
- 위험도 정책이 일관되게 적용된다.
- CLI와 TUI가 같은 핵심 로직을 사용한다.
- JSON/Markdown 출력이 깨지지 않는다.
- 테스트가 추가 또는 갱신된다.
- 기본값이 안전하다.
