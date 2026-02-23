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

## 진행 중 / 다음 작업

- [ ] `deploy-cloud-run` 인증 실패 원인 수정 후 end-to-end 성공 검증
  - run id `22314120424`: `WIF_PROVIDER`/`WIF_SERVICE_ACCOUNT` 미설정으로 auth 단계 실패
- [ ] `/healthz` 404 원인 분석 및 수정
- [ ] Cloud Build `PERMISSION_DENIED` 원인 확정(권한/조직정책)
- [ ] Cloud SQL + Secret Manager + `/db/healthz` 200 검증(3단계)
- [ ] `POST /items`, `GET /items/{id}` 실환경 검증
