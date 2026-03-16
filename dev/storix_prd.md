# Storix PRD

## 1. 문서 정보

- 제품명: Storix
- 제품 유형: macOS 로컬 저장공간 분석 및 정리 도구
- 제공 형태: CLI + TUI
- 대상 버전: MVP v1.0
- 작성 목적: macOS 개발자 및 파워유저가 로컬 저장공간 사용 현황을 쉽게 분석하고, 안전하게 정리할 수 있도록 하는 도구의 제품 요구사항 정의

---

## 2. 제품 개요

Storix는 macOS 환경에서 동작하는 저장공간 분석/정리 도구이다.  
기존의 단순 shell script 방식과 달리, 사용자가 현재 어떤 폴더와 캐시가 얼마나 많은 용량을 차지하고 있는지 파악할 수 있도록 돕고, 삭제 가능한 대상을 위험도에 따라 분류하여 안전하게 저장공간을 확보할 수 있도록 지원한다.

Storix는 두 가지 인터페이스를 제공한다.

1. **CLI**
   - 스크립트 친화적
   - 빠른 조회, 자동화, 배치 정리에 적합
   - 예: `storix scan`, `storix doctor`, `storix clean all-safe`

2. **TUI**
   - 터미널 내부 인터랙티브 화면
   - 시각적으로 목록을 보고 선택/정리하기에 적합
   - 예: `storix tui`

Storix는 단순 삭제 툴이 아니라, 다음 흐름을 제공한다.

1. 스캔
2. 분석
3. 위험도 분류
4. 예상 회수 용량 제시
5. 사용자 선택 및 확인
6. 정리 실행
7. 결과 리포트 제공

---

## 3. 문제 정의

### 3.1 현재 문제

macOS 개발 환경에서는 다음 데이터가 빠르게 누적된다.

- Xcode DerivedData, Archives, DeviceSupport, Simulator 데이터
- Android AVD, SDK system-images, Gradle cache
- Flutter/Dart pub cache, `.dart_tool`, `build`
- Node cache, `.next`, `dist`, `coverage`
- CocoaPods cache, `Pods`
- VS Code cache/workspaceStorage
- Downloads 내 설치 파일, 압축 파일, 대용량 아티팩트

하지만 현재 사용자는 다음 문제를 겪는다.

- 어떤 폴더가 진짜 큰지 한눈에 보기 어렵다.
- 지워도 되는 것과 위험한 것을 구분하기 어렵다.
- 단순 `rm -rf` 스크립트는 위험하다.
- 삭제 전 얼마나 비워질지 모른다.
- 프로젝트별 산출물 누적을 놓치기 쉽다.
- 반복적으로 쓰기 좋은 정리 도구가 없다.

### 3.2 해결하고자 하는 핵심 문제

Storix는 사용자가 다음 질문에 답할 수 있게 해야 한다.

- 지금 내 저장공간은 어디서 많이 쓰고 있는가
- 무엇을 지워도 안전한가
- 무엇은 조심해서 지워야 하는가
- 얼마나 비울 수 있는가
- 어떻게 반복적으로 관리할 수 있는가

---

## 4. 제품 목표

### 4.1 핵심 목표

- macOS 로컬 저장공간 사용처를 빠르게 가시화한다.
- 개발 환경 중심의 정리 가능한 항목을 자동 탐지한다.
- 삭제 전 예상 회수 용량을 보여준다.
- 위험도를 분류해 신뢰 가능한 정리를 제공한다.
- CLI와 TUI 모두 지원하여 자동화와 수동 확인 작업을 모두 만족시킨다.
- 배포가 쉬운 형태로 제공하여 설치 장벽을 낮춘다.

### 4.2 성공 기준

- 사용자가 3분 내에 주요 용량 사용처를 파악할 수 있다.
- `doctor` 혹은 `tui` 진입 후 정리 가능한 항목을 쉽게 선택할 수 있다.
- `safe` 항목만 정리해도 유의미한 공간 확보가 가능하다.
- 잘못된 삭제 사고 가능성을 최소화한다.
- macOS 개발자 환경에서 반복적으로 사용할 수 있는 실용적 도구가 된다.

---

## 5. 타겟 사용자

### 5.1 1차 타겟

- macOS 개발자
- Flutter/iOS/Android/Web 개발자
- Xcode/Android Studio/VS Code 사용 빈도가 높은 사용자
- 디스크 용량 부족 문제를 자주 겪는 사용자

### 5.2 2차 타겟

- 일반 macOS power user
- 다운로드 폴더와 설치 파일이 자주 쌓이는 사용자
- CLI/TUI 사용에 익숙한 사용자

---

## 6. 핵심 가치 제안

Storix는 다음 가치를 제공한다.

- 저장공간 사용처를 보여준다.
- 지워도 되는 것과 조심해야 하는 것을 구분해준다.
- 얼마나 확보될지 예측해준다.
- 자동화 가능한 CLI를 제공한다.
- 사람이 보기 쉬운 TUI를 제공한다.
- 개발자 캐시/산출물 정리에 특화된 경험을 제공한다.

---

## 7. 핵심 사용 시나리오

### 시나리오 A. 저장공간 부족 경고를 본 개발자

사용자는 macOS 저장공간 부족 경고를 보고 `storix doctor`를 실행한다.  
Storix는 Xcode Archives, Android system-images, Gradle cache, pub cache 등 정리 후보를 표시한다.  
사용자는 안전한 항목만 먼저 지운 뒤, 필요한 경우 `caution` 항목까지 검토한다.

### 시나리오 B. TUI에서 눈으로 보고 선택 정리

사용자는 `storix tui`를 실행한다.  
좌측 카테고리 목록, 중앙 정리 후보 목록, 우측 상세 설명을 보며 항목을 체크한다.  
Dry-run으로 예상 확보 용량을 확인하고, 이후 clean을 실행한다.

### 시나리오 C. 프로젝트 산출물 누적 정리

사용자는 여러 Flutter/Node 프로젝트를 운영한다.  
`storix projects scan ~/Dev ~/Workspace`로 프로젝트별 산출물을 스캔한다.  
오래된 `build`, `.dart_tool`, `.next`, `dist`, `ios/Pods` 등을 골라 정리한다.

### 시나리오 D. 자동화/스크립트용 사용

사용자는 cron, zsh alias, 셸 스크립트 등에서 `storix clean all-safe --yes`를 주기적으로 실행한다.  
사람이 직접 들어가지 않아도 비교적 안전한 정리만 자동으로 처리할 수 있다.

---

## 8. 제품 범위

### 8.1 MVP 범위

#### A. 저장공간 개요 조회
- 전체 디스크 용량
- 사용량
- 여유 공간
- 주요 경로별 사용량 요약

#### B. 카테고리별 스캔
- Xcode
- Android
- Flutter/Dart
- Node/Web
- Python
- VS Code
- General 사용자 폴더

#### C. 정리 후보 탐지
예시:
- Xcode DerivedData
- Xcode Archives
- iOS DeviceSupport
- Simulator device data
- Android AVD
- Android SDK system-images
- Gradle cache
- pub cache
- CocoaPods cache
- npm/yarn/pnpm cache
- VS Code cache
- 프로젝트별 build output

#### D. 위험도 분류
- safe
- caution
- dangerous

#### E. Dry-run
- 삭제 예정 항목 미리 보기
- 예상 회수 용량 계산

#### F. Clean
- 카테고리별 정리
- safe-only 정리
- interactive 정리

#### G. TUI
- 목록 조회
- 카테고리 전환
- 후보 선택
- 상세 패널 확인
- dry-run
- clean 실행

#### H. 리포트
- JSON 출력
- Markdown 출력

### 8.2 차기 버전 범위

- Trash 이동 옵션
- 중복 파일 탐지
- 대용량 오래된 설치 파일 추천 정리
- iCloud local occupancy 대응
- scheduler 연동
- rule customization
- Linux 지원
- GUI 앱 확장

---

## 9. 인터페이스 전략

### 9.1 CLI 역할

CLI는 다음 사용자에게 적합하다.

- 빠르게 결과만 보고 싶은 사용자
- 셸 스크립트와 함께 쓰고 싶은 사용자
- 배치 정리를 하고 싶은 사용자
- 로그/JSON 결과가 필요한 사용자

주요 명령:
- `storix scan`
- `storix top`
- `storix doctor`
- `storix clean`
- `storix projects scan`
- `storix report`

### 9.2 TUI 역할

TUI는 다음 사용자에게 적합하다.

- 항목을 눈으로 보며 골라 지우고 싶은 사용자
- 위험도와 상세 설명을 함께 보고 싶은 사용자
- CLI 옵션보다 인터랙티브 조작이 편한 사용자

주요 진입:
- `storix tui`

---

## 10. TUI UX 요구사항

### 10.1 화면 구성

#### 좌측 패널
- 카테고리 목록
- 예: All, Xcode, Android, Flutter, Node, VS Code, General

#### 중앙 패널
- 정리 후보 목록
- 항목명
- 경로
- 용량
- 위험도
- 선택 여부

#### 우측 패널
- 상세 설명
- 탐지 이유
- 재생성 가능 여부
- 주의사항
- 예상 회수 용량

#### 하단 영역
- 상태 표시
- 키바인드 안내
- 총 선택 용량

### 10.2 키바인드 초안

- `↑/↓`: 항목 이동
- `←/→`: 카테고리 이동 또는 패널 이동
- `space`: 선택/해제
- `a`: 전체 선택
- `d`: dry-run
- `c`: clean 실행
- `r`: rescan
- `f`: risk filter
- `q`: 종료

### 10.3 TUI 핵심 원칙

- 삭제 전에 항상 확인 흐름이 있어야 한다.
- 위험도는 시각적으로 명확히 구분되어야 한다.
- 선택된 항목의 총 확보 예상 용량이 즉시 보여야 한다.
- dry-run과 실제 clean이 구분되어야 한다.

---

## 11. 기능 요구사항

### 11.1 Scan

사용자는 로컬 저장공간 사용량과 주요 정리 후보를 스캔할 수 있어야 한다.

지원 명령 예시:
- `storix scan`
- `storix scan --json`
- `storix scan --path ~/Library --depth 2`

기대 결과:
- 디스크 요약
- 주요 경로별 용량
- 큰 후보 목록

### 11.2 Doctor

사용자는 정리 가능한 항목을 카테고리별로 집계해서 볼 수 있어야 한다.

지원 명령 예시:
- `storix doctor`
- `storix doctor --json`
- `storix doctor --markdown`

기대 결과:
- 카테고리별 reclaimable storage
- safe/caution/dangerous 합계
- 우선 정리 추천 대상

### 11.3 Clean

사용자는 정리 가능한 항목을 삭제할 수 있어야 한다.

지원 명령 예시:
- `storix clean all-safe --dry-run`
- `storix clean xcode`
- `storix clean android --yes`
- `storix clean --interactive`

기대 결과:
- 삭제 대상 목록
- 예상 회수 용량
- 삭제 후 결과 요약

### 11.4 Projects Scan

사용자는 특정 프로젝트 루트 아래의 산출물을 탐지할 수 있어야 한다.

지원 명령 예시:
- `storix projects scan ~/Dev ~/Workspace`

기대 결과:
- 프로젝트 타입 자동 감지
- 산출물 후보 목록
- 프로젝트별 reclaimable storage

### 11.5 TUI

사용자는 터미널 내부에서 인터랙티브하게 후보를 탐색하고 정리할 수 있어야 한다.

지원 명령 예시:
- `storix tui`

기대 결과:
- 카테고리 탐색
- 항목 선택
- dry-run
- clean
- 상태 피드백

---

## 12. 위험도 정책

### safe
재생성 가능한 캐시/빌드 산출물

예:
- DerivedData
- build
- `.dart_tool`
- VS Code cache
- workspaceStorage

### caution
재생성 가능하지만 비용이 있거나 주의가 필요한 항목

예:
- Xcode Archives
- Android system-images
- AVD
- pub cache
- Gradle cache
- CocoaPods cache
- `ios/Pods`

### dangerous
사용자 데이터가 섞이거나 중요한 작업물이 포함될 가능성이 높은 항목

예:
- Downloads
- Desktop
- Documents
- Movies
- 프로젝트 루트
- 사용자 원본 파일

정책:
- dangerous는 기본 삭제 제외
- caution은 별도 확인 필요
- safe는 빠른 정리 대상
- TUI/CLI 모두 동일 정책 사용

---

## 13. 비기능 요구사항

### 성능
- 기본 스캔은 10~30초 내 주요 결과 제공
- known path 우선 스캔
- 전체 재귀 탐색은 옵션화

### 안정성
- dry-run 필수 지원
- 삭제 실패가 전체 흐름을 망치지 않도록 부분 실패 허용
- guard path 보호 필수

### 사용성
- 사람이 읽기 쉬운 출력
- 컬러/아이콘 기반 위험도 표현
- 명령어 일관성 유지

### 확장성
- 카테고리 추가가 쉬워야 함
- ruleset 확장이 가능해야 함
- TUI/CLI가 동일한 서비스 계층을 재사용해야 함

---

## 14. 배포 전략 요구사항

Storix는 설치 장벽을 낮추기 위해 다중 배포 전략을 지원한다.

### 14.1 1차 배포 방식: PyPI + pipx
- 개발자 친화적
- 설치와 업데이트가 단순
- CLI 앱으로 배포하기 적합

설치 예시:
- `pipx install storix`

### 14.2 2차 배포 방식: Homebrew Tap
- macOS 사용자 경험 개선
- brew 기반 설치 가능

설치 예시:
- `brew tap <org>/storix`
- `brew install storix`

### 14.3 선택 배포 방식: standalone binary
- Python 없는 환경도 지원
- 배포 파일만 실행 가능
- PyInstaller 기반 고려

---

## 15. 성공 지표

### 정량
- doctor 실행 후 clean 전환율
- safe-only clean 실행 빈도
- 1회 실행당 평균 회수 용량
- clean 실패율
- TUI 사용 비율

### 정성
- “무엇을 지워야 할지 이해하기 쉬운가”
- “안심하고 쓸 수 있는가”
- “기존 스크립트보다 신뢰감이 높은가”

---

## 16. 제약사항

- macOS 시스템 보호 영역은 완전한 접근이 불가하다.
- 일부 sandbox 앱 데이터는 접근 제한이 있다.
- root 권한 없는 상태에서는 시스템 전체 완전 분석이 불가능하다.
- iCloud/Time Machine/시스템 내부 special storage는 정확한 해석이 제한될 수 있다.

---

## 17. MVP 완료 정의

다음이 가능하면 MVP 완료로 본다.

- CLI scan/doctor/clean 동작
- TUI 진입 및 카테고리/목록/상세/선택/clean 동작
- 주요 개발자 캐시 자동 탐지
- risk 분류 적용
- dry-run 지원
- JSON/Markdown report 지원
- pipx 설치 가능한 패키징 완료

---

## 18. 제품 원칙

- 먼저 보여주고, 그다음 지운다.
- 기본값은 안전해야 한다.
- 위험한 것은 자동으로 지우지 않는다.
- CLI와 TUI는 같은 로직을 공유한다.
- 개발자에게 신뢰 가능한 로컬 도구가 된다.