# Storix TDD

## 1. 문서 정보

- 프로젝트명: Storix
- 문서 유형: Technical Design Document
- 대상 버전: MVP v1.0
- 플랫폼: macOS
- 인터페이스: CLI + TUI
- 작성 목적: Storix의 기술 구조, 모듈 설계, 데이터 흐름, TUI 구조, 배포 구조를 정의한다.

---

## 2. 기술 개요

Storix는 Python 기반 애플리케이션으로 구현한다.  
CLI는 `Typer`, 출력은 `Rich`, TUI는 `Textual`을 사용한다.

시스템은 다음 기능을 담당한다.

1. 파일 시스템 및 known path 스캔
2. 정리 후보 추출
3. 위험도 분류
4. reclaimable storage 계산
5. dry-run / interactive clean
6. TUI 렌더링 및 사용자 액션 처리
7. JSON/Markdown 리포트 생성
8. 배포 가능한 패키지 구조 제공

---

## 3. 기술 스택

### 언어
- Python 3.11+

### CLI
- Typer

### 콘솔 출력
- Rich

### TUI
- Textual

### 파일 시스템 처리
- pathlib
- os
- shutil

### 시스템 명령 실행
- subprocess

### 데이터 모델링
- dataclasses 또는 pydantic

### 직렬화
- json
- pyyaml

### 테스트
- pytest
- pytest-mock
- tempfile / tmp_path

### 패키징
- pyproject.toml
- setuptools 또는 hatchling
- pipx 설치 가능 구조

### 선택 배포
- PyInstaller
- Homebrew tap formula

---

## 4. 아키텍처 원칙

Storix는 UI와 비즈니스 로직을 분리한다.

### 원칙
- CLI와 TUI는 동일한 서비스 계층을 재사용한다.
- 스캔/분석/정리 로직은 UI에 독립적이어야 한다.
- presenter 계층만 CLI/TUI/JSON/Markdown에 따라 달라진다.
- dangerous path는 공통 guard rule로 보호한다.

---

## 5. 전체 구조

```text
storix/
├─ pyproject.toml
├─ README.md
├─ storix/
│  ├─ __init__.py
│  ├─ cli.py
│  ├─ main.py
│  ├─ constants.py
│  ├─ models/
│  │  ├─ enums.py
│  │  ├─ candidate.py
│  │  ├─ summary.py
│  │  ├─ clean_result.py
│  │  └─ report.py
│  ├─ services/
│  │  ├─ scan_service.py
│  │  ├─ doctor_service.py
│  │  ├─ clean_service.py
│  │  ├─ project_service.py
│  │  └─ report_service.py
│  ├─ scanners/
│  │  ├─ disk_scanner.py
│  │  ├─ xcode_scanner.py
│  │  ├─ android_scanner.py
│  │  ├─ flutter_scanner.py
│  │  ├─ node_scanner.py
│  │  ├─ python_scanner.py
│  │  ├─ vscode_scanner.py
│  │  ├─ project_scanner.py
│  │  └─ general_scanner.py
│  ├─ cleaners/
│  │  ├─ base.py
│  │  ├─ xcode_cleaner.py
│  │  ├─ android_cleaner.py
│  │  ├─ flutter_cleaner.py
│  │  ├─ node_cleaner.py
│  │  ├─ vscode_cleaner.py
│  │  └─ project_cleaner.py
│  ├─ tui/
│  │  ├─ app.py
│  │  ├─ screens/
│  │  │  ├─ main_screen.py
│  │  │  ├─ confirm_screen.py
│  │  │  └─ result_screen.py
│  │  ├─ widgets/
│  │  │  ├─ category_list.py
│  │  │  ├─ candidate_table.py
│  │  │  ├─ detail_panel.py
│  │  │  ├─ footer_bar.py
│  │  │  └─ summary_bar.py
│  │  └─ storix.tcss
│  ├─ presenters/
│  │  ├─ console_presenter.py
│  │  ├─ json_presenter.py
│  │  ├─ markdown_presenter.py
│  │  └─ tui_adapter.py
│  ├─ utils/
│  │  ├─ fs.py
│  │  ├─ shell.py
│  │  ├─ size.py
│  │  ├─ guard.py
│  │  ├─ logger.py
│  │  └─ confirm.py
│  └─ rules/
│     └─ targets.yaml
└─ tests/
   ├─ test_scan_service.py
   ├─ test_doctor_service.py
   ├─ test_clean_service.py
   ├─ test_project_scanner.py
   ├─ test_guard.py
   ├─ test_tui_state.py
   └─ fixtures/