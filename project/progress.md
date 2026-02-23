# Progress

작성일시: 2026-02-24 00:56:51 KST

## 현재 상태 요약

- Cloud Run 수동 배포 완료
  - 서비스명: `fastapi-backend`
  - 프로젝트/리전: `vibe-fastapi-dev` / `asia-northeast3`
  - 최신 리비전: `fastapi-backend-00002-dvk`
  - 트래픽: 최신 리비전 100%
  - 서비스 URL: `https://fastapi-backend-gddhqf47hq-du.a.run.app`
- 2단계 파이프라인 코드 반영 완료
  - PR 테스트: `.github/workflows/ci-pr.yml`
  - PR auto-merge: `.github/workflows/auto-merge.yml`
  - 머지 후 배포: `.github/workflows/deploy.yml` (`push` to `main`)

## 이번 세션 변경 사항

- 문서 업데이트
  - `README.md`: 2단계를 PR 기반(`ci -> auto-merge -> deploy`)으로 재정의
  - `docs/00-start-here.md`: PR 기본 운영 정책/required check 반영
  - `docs/github-actions-wif.md`: 저장소 설정/워크플로우 역할/검증 절차 추가
- 워크플로우 업데이트
  - `deploy.yml`에서 test job 제거(배포 전용)
  - `ci-pr.yml` 신규 추가(`pull_request`에서 `unit-test`)
  - `auto-merge.yml` 신규 추가(`pull_request_target`에서 squash auto-merge 예약)

## 검증 결과

- 워크플로우 YAML 파싱
  - `ci-pr.yml`, `auto-merge.yml`, `deploy.yml` 모두 `YAML.load_file` 통과
- 코드 스모크
  - `uv run python -m compileall app tests` 통과
  - TestClient 호출 결과
    - `GET /` -> `200`
    - `GET /healthz` -> `200`
- 배포 URL 기준 외부 확인(기존 상태 유지)
  - `GET /` -> `200`
  - `GET /openapi.json` -> `200`
  - `GET /healthz` -> `404` (Google 404 HTML)
  - `GET /db/healthz` -> `503` (`DB_NAME`, `DB_USER`, `DB_PASSWORD` 미설정)

## Git 상태

- 작업 브랜치: `feat/pr-auto-merge-deploy-pipeline`
- 기본 브랜치: `main`
- 원격: `origin` (`git@github.com:krnomad/vibe-gcp-github-template.git`)

## 배포 중 이슈/해결(누적)

- 이슈: Cloud Build(`gcloud builds submit`)에서 `PERMISSION_DENIED`
- 우회: 로컬 Docker 빌드 + Artifact Registry push + Cloud Run deploy
- 이슈: ARM 이미지 배포 시 컨테이너 기동 실패
- 해결: `docker buildx build --platform linux/amd64 --push`로 재배포

## 작업 중 실패 로그

- 로그: `zsh:1: command not found: main`
  - 상황: 백틱이 포함된 `rg` 패턴을 큰따옴표로 실행
  - 원인: zsh command substitution으로 `` `main` ``이 명령으로 해석됨
  - 해결: 작은따옴표/이스케이프 적용 후 재실행, 매치 없음 확인

## 다음 작업

1. GitHub 저장소에서 `Allow auto-merge`/`Allow squash merging` 및 `main` branch protection 적용
2. PR 생성 후 `ci-pr` 성공 -> auto-merge(squash) -> `deploy-cloud-run` 성공까지 E2E 검증
3. `/healthz` 404 원인 문서화/경로 조정 및 3단계(DB) 검증 진행
