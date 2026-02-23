# Progress

작성일시: 2026-02-24 01:06:27 KST

## 현재 상태 요약

- Cloud Run 수동 배포 완료
  - 서비스명: `fastapi-backend`
  - 프로젝트/리전: `vibe-fastapi-dev` / `asia-northeast3`
  - 최신 리비전: `fastapi-backend-00002-dvk`
  - 서비스 URL: `https://fastapi-backend-gddhqf47hq-du.a.run.app`
- 2단계(PR CI -> auto-merge -> merge 후 배포) 파이프라인 코드가 `main`에 반영됨
  - 머지 커밋: `040141fa87d47ff82925ee390737c7ba43ccb6c4`
  - PR: `https://github.com/krnomad/vibe-gcp-github-template/pull/1`
- GitHub 저장소 설정 적용 완료
  - `allow_auto_merge=true`
  - `allow_squash_merge=true`
  - `delete_branch_on_merge=true`
  - `main` branch protection: required check `unit-test`, required approvals `0`

## 이번 세션 변경 사항

- 워크플로우 분리/배포
  - `ci-pr.yml`: `pull_request` 테스트
  - `auto-merge.yml`: `pull_request_target`에서 auto-merge 예약
  - `deploy.yml`: `push` to `main` 배포 전용
- 문서 동기화
  - `README.md`
  - `docs/00-start-here.md`
  - `docs/github-actions-wif.md`
  - 프로젝트 추적 문서(`project/*.md`)
- PR 생성/머지
  - 브랜치 push 후 PR #1 생성
  - `gh pr merge --auto --squash --delete-branch`로 auto-merge 예약
  - 체크 통과 후 `main`에 squash 머지 확인

## 검증 결과

- 로컬 검증
  - 워크플로우 YAML 파싱(`YAML.load_file`) 통과
  - `uv run python -m compileall app tests` 통과
  - TestClient: `GET /`/`GET /healthz` -> `200`
- GitHub 검증
  - `ci-pr` 워크플로우(`unit-test`) 성공
  - PR #1 `MERGED` 확인
  - `deploy-cloud-run` 실행됨(run id: `22314120424`)
  - 배포는 인증 단계 실패(아래 실패 로그 참고)

## 배포 중 이슈/해결(누적)

- 이슈: Cloud Build(`gcloud builds submit`)에서 `PERMISSION_DENIED`
- 우회: 로컬 Docker 빌드 + Artifact Registry push + Cloud Run deploy
- 이슈: ARM 이미지 배포 시 컨테이너 기동 실패
- 해결: `docker buildx build --platform linux/amd64 --push`로 재배포

## 작업 중 실패 로그

- 로그: `zsh:1: command not found: main`
  - 상황: 백틱이 포함된 `rg` 패턴을 큰따옴표로 실행
  - 원인: zsh command substitution으로 `` `main` ``이 명령으로 해석됨
  - 해결: 작은따옴표/이스케이프 적용 후 재실행
- 로그: `zsh:1: no matches found: required_status_checks.contexts[]=ci-pr / unit-test`
  - 상황: `gh api` 인자에 `[]`/공백이 포함된 값을 무인용으로 전달
  - 원인: zsh glob 확장
  - 해결: JSON payload(`--input`) 방식으로 branch protection 적용
- 로그: `google-github-actions/auth failed ... must specify exactly one of workload_identity_provider or credentials_json`
  - 상황: `deploy-cloud-run` run id `22314120424`의 `Authenticate to Google Cloud` 단계 실패
  - 원인: GitHub Secrets `WIF_PROVIDER`, `WIF_SERVICE_ACCOUNT` 미설정(또는 주입 실패)
  - 해결: 저장소 Secrets 등록 후 `deploy-cloud-run` 재실행 필요
- 로그: `zsh:1: command not found: unit-test`
  - 상황: `gh pr create` 본문 문자열에 백틱(`unit-test`)을 큰따옴표로 전달
  - 원인: zsh command substitution
  - 해결: 본문 문자열의 백틱 이스케이프 또는 single-quote 사용 필요

## 다음 작업

1. GitHub Secrets 설정
   - `WIF_PROVIDER` (provider full resource name)
   - `WIF_SERVICE_ACCOUNT` (deploy SA email)
2. `deploy-cloud-run` 재실행 또는 신규 커밋 push로 재검증
3. `/healthz` 404 원인 문서화/경로 조정
4. Cloud SQL + Secret Manager 연동 후 `/db/healthz` 200 검증
