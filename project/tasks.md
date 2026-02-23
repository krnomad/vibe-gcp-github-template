# Tasks

작성일: 2026-02-24 (KST)

## 완료

- [x] FastAPI 앱 기본 엔드포인트 구현
- [x] Dockerfile 작성
- [x] Artifact Registry 저장소 생성 (`fastapi`)
- [x] Cloud Run 수동 배포 완료
- [x] `GET /` 실동작 확인
- [x] 에이전트 규칙 문서 추가 (`AGENTS.md`)
- [x] 시작/부트스트랩/WIF 문서 골격 추가
- [x] `README.md`에 10분 Quickstart 섹션 추가
- [x] GitHub 원격 `main` 동기화 완료
- [x] PR 기반 CI/auto-merge/deploy 워크플로우 분리
  - `ci-pr.yml`, `auto-merge.yml`, `deploy.yml` 업데이트
- [x] 2단계 운영 문서 갱신
  - `README.md`, `docs/00-start-here.md`, `docs/github-actions-wif.md`
- [x] 워크플로우 YAML 파싱/앱 스모크 검증
  - YAML load 성공, `GET /`/`GET /healthz` 200 확인
- [x] GitHub 저장소 설정 적용
  - `Allow auto-merge`, `Allow squash merging`, `delete branch on merge`
  - `main` branch protection(required check: `unit-test`, approvals: `0`)
- [x] PR 생성/머지 흐름 확인
  - PR #1에서 `unit-test` 성공 후 squash merge 완료
- [x] `deploy.yml` 트리거 보강 반영
  - `main push` + `workflow_run(ci-pr 성공)` 이벤트에서 배포 실행하도록 조정
- [x] GitHub Actions 배포 인증값 설정
  - `WIF_PROVIDER`, `WIF_SERVICE_ACCOUNT` secrets 등록 완료
  - `GCP_PROJECT_ID`, `GCP_REGION`, `ARTIFACT_REPOSITORY`, `CLOUD_RUN_SERVICE` variables 등록 완료
- [x] `deploy-cloud-run` end-to-end 검증
  - rerun run id `22314798677` 성공
  - Cloud Run 최신 리비전 `fastapi-backend-00003-mqm` 반영 확인

## 진행 중 / 다음 작업

- [ ] P1: `/healthz` 404 원인 분석 및 수정
  - 완료 기준: 원인/대응이 문서화되고 운영용 health path가 확정됨
- [ ] P1: Cloud Build `PERMISSION_DENIED` 원인 확정(권한/조직정책)
  - 완료 기준: 재현 로그 + 누락 권한/정책 식별 + 해결 절차 문서화
- [ ] P2: Cloud SQL + Secret Manager + `/db/healthz` 200 검증(3단계)
  - 완료 기준: 배포 변수/시크릿 연동 후 `/db/healthz`가 `200` 반환
- [ ] P2: `POST /items`, `GET /items/{id}` 실환경 검증
  - 완료 기준: 생성/조회 시나리오 1회 이상 성공 및 결과 기록
