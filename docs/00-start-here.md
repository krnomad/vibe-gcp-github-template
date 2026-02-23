# 00-start-here

작성일: 2026-02-24 (KST)

이 문서는 이 저장소에서 작업할 때 가장 먼저 읽는 시작점이다.

## 목적

- GitHub + GitHub Actions + GCP 연동 템플릿을 재사용 가능하게 유지
- 신규 프로젝트에서도 동일한 방식으로 빠르게 부트스트랩
- 에이전트/사람 모두 같은 순서로 작업하도록 표준화

## 문서 읽기 순서

1. `docs/00-start-here.md` (현재 문서)
2. `docs/gcp-project-bootstrap.md` (신규 GCP 프로젝트 준비)
3. `docs/github-actions-wif.md` (GitHub OIDC/WIF 연동)
4. `docs/gcp-setup.md` (상세 명령/레퍼런스)

## 빠른 체크리스트

1. 목표와 범위 확정
   - 1단계: Cloud Run 수동 배포
   - 2단계: GitHub Actions 자동 배포
   - 3단계: Cloud SQL + Alembic
2. 환경 변수 템플릿 준비
   - `PROJECT_ID`, `REGION`, `SERVICE_NAME`, `REPO_NAME`
3. 현재 상태 확인
   - `project/progress.md`
   - `project/tasks.md`

## 필수 정책

- `gcloud` 명령 실행 전, 항상 `docs/gcp-project-bootstrap.md`의 변수 블록을 먼저 확인
- GitHub Actions 관련 변경 전, `docs/github-actions-wif.md`의 Secret/Variable 매핑을 먼저 확인
- 작업 후에는 `project/progress.md`와 `project/tasks.md`를 최신화

## 다음 문서

신규 프로젝트 초기화를 시작하려면 `docs/gcp-project-bootstrap.md`로 이동
