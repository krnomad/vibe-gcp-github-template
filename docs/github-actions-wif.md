# GitHub Actions + WIF (OIDC)

작성일: 2026-02-24 (KST)

GitHub Actions에서 장기 키 없이 GCP에 배포하기 위한 OIDC/WIF 가이드.

## 0) 전제

- `docs/gcp-project-bootstrap.md` 완료
- GitHub 저장소 생성 완료
- 배포 대상 브랜치: `main`
- 개발 흐름: 기능 브랜치 -> PR -> auto-merge(squash) -> `main`

## 1) 변수 정의

```bash
export PROJECT_ID="YOUR_PROJECT_ID"
export PROJECT_NUMBER="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')"

export GH_OWNER="YOUR_GITHUB_OWNER"
export GH_REPO="YOUR_GITHUB_REPO"

export WIF_POOL="github-pool"
export WIF_PROVIDER="github-provider"
export DEPLOY_SA="github-deployer"
export DEPLOY_SA_EMAIL="${DEPLOY_SA}@${PROJECT_ID}.iam.gserviceaccount.com"
```

## 2) WIF Pool/Provider 생성

```bash
gcloud iam workload-identity-pools create "$WIF_POOL" \
  --location="global" \
  --display-name="GitHub Pool" \
  --project "$PROJECT_ID"

gcloud iam workload-identity-pools providers create-oidc "$WIF_PROVIDER" \
  --location="global" \
  --workload-identity-pool="$WIF_POOL" \
  --display-name="GitHub Provider" \
  --issuer-uri="https://token.actions.githubusercontent.com" \
  --attribute-mapping="google.subject=assertion.sub,attribute.repository=assertion.repository,attribute.ref=assertion.ref" \
  --attribute-condition="assertion.repository=='${GH_OWNER}/${GH_REPO}'" \
  --project "$PROJECT_ID"
```

## 3) GitHub OIDC 주체에 SA 권한 부여

```bash
export WIF_POOL_NAME="projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WIF_POOL}"

gcloud iam service-accounts add-iam-policy-binding "$DEPLOY_SA_EMAIL" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WIF_POOL_NAME}/attribute.repository/${GH_OWNER}/${GH_REPO}" \
  --project "$PROJECT_ID"
```

## 4) GitHub 설정값 매핑

Secrets:

- `WIF_PROVIDER`: provider full resource name
- `WIF_SERVICE_ACCOUNT`: deploy service account email

Variables:

- `GCP_PROJECT_ID`
- `GCP_REGION`
- `ARTIFACT_REPOSITORY`
- `CLOUD_RUN_SERVICE`
- `CLOUD_RUN_RUNTIME_SA`

DB 연동 시 추가 Variables:

- `INSTANCE_CONNECTION_NAME`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD_SECRET`

## 5) provider resource name 조회

```bash
gcloud iam workload-identity-pools providers describe "$WIF_PROVIDER" \
  --workload-identity-pool="$WIF_POOL" \
  --location="global" \
  --project "$PROJECT_ID" \
  --format="value(name)"
```

## 6) GitHub 저장소 설정

1. `Settings > General`
   - `Allow auto-merge` 활성화
   - `Allow squash merging` 활성화
2. `Settings > Branches > Branch protection rules (main)`
   - `Require a pull request before merging` 활성화
   - `Require status checks to pass before merging` 활성화
   - Required checks: `unit-test`
   - 승인 리뷰 수: 0 (리뷰 없이 체크만)
   - `main` 직접 push 차단(권장)

## 7) 워크플로우 구성

- `ci-pr.yml`
  - 트리거: `pull_request` to `main`
  - 역할: 테스트(`unit-test`) 수행
- `auto-merge.yml`
  - 트리거: `pull_request_target` (`opened`, `reopened`, `synchronize`, `ready_for_review`)
  - 역할: 같은 저장소 브랜치 PR에 auto-merge(squash) 예약
- `deploy.yml`
  - 트리거: `push` to `main` 또는 `pull_request_target(closed)` with merged
  - 역할: OIDC 인증 후 이미지 빌드/푸시 및 Cloud Run 배포

## 8) 동작 검증

1. 기능 브랜치에서 커밋 후 PR 생성(`base: main`)
2. `ci-pr` 워크플로우의 `unit-test` 성공 확인
3. PR이 auto-merge로 squash 머지되는지 확인
4. 머지 직후 `deploy-cloud-run` 워크플로우 성공 확인
5. Cloud Run 최신 리비전 반영 확인

## 9) 트러블슈팅 메모

- `PERMISSION_DENIED`: SA 역할/바인딩 누락 여부 확인
- `unauthorized` on auth step: `WIF_PROVIDER` 값이 full resource name인지 확인
- 배포 실패: 이미지 아키텍처(`linux/amd64`) 및 런타임 env 확인
- auto-merge 미동작: 저장소 `Allow auto-merge`와 branch protection required check 이름 확인
