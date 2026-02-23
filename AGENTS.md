# AGENTS.md

이 저장소에서 작업하는 에이전트는 아래 규칙을 반드시 따른다.

## 1) 필수 선행 읽기

`gcloud`, 배포, IAM, GitHub Actions 관련 명령을 실행하기 전에 아래 문서를 순서대로 먼저 읽는다.

1. `docs/00-start-here.md`
2. `docs/gcp-project-bootstrap.md`
3. `docs/github-actions-wif.md`

참고: 기존 상세 가이드는 `docs/gcp-setup.md`를 사용한다.

## 2) 실행 규칙

1. 신규 GCP 프로젝트를 다룰 때는 `docs/gcp-project-bootstrap.md`의 변수 블록부터 채운다.
2. GitHub Actions OIDC/WIF 설정은 `docs/github-actions-wif.md` 절차를 우선 적용한다.
3. 문서에 없는 명령을 실행했다면, 작업 종료 전 관련 문서에 반영한다.
4. 실패 로그가 발생하면 원인/해결을 `project/progress.md`에 기록한다.

## 3) 문서 우선 원칙

코드 변경보다 먼저 문서 정합성을 확인한다.

1. 문서 절차와 실제 명령이 다르면 문서를 먼저 수정
2. 이후 코드/워크플로우 수정
3. 마지막에 검증 결과를 `project/tasks.md`, `project/progress.md`에 업데이트
