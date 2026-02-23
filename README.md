# FastAPI + Cloud Run + GitHub Actions + Cloud SQL(Postgres) 실습

이 저장소는 아래 3단계를 한 번에 실습할 수 있도록 구성되어 있습니다.

1. FastAPI를 Cloud Run에 수동 배포
2. PR 테스트 통과 후 자동 머지 + `main` 머지 시 자동 배포
3. Cloud SQL(Postgres) 연동 + Alembic 마이그레이션

## Start Here (템플릿 운용 문서)

아래 문서 순서대로 확인한 뒤 작업을 진행하세요.

1. `docs/00-start-here.md`
2. `docs/gcp-project-bootstrap.md`
3. `docs/github-actions-wif.md`
4. `docs/gcp-setup.md`

에이전트 실행 규칙은 `AGENTS.md`에 정리되어 있습니다.

## 10분 Quickstart (신규 프로젝트 기준)

아래 순서대로 실행하면 템플릿 초기 세팅과 1단계 배포까지 빠르게 진행할 수 있습니다.

1. 저장소 클론 + 기본 도구 확인
```bash
git clone https://github.com/krnomad/vibe-gcp-github-template.git
cd vibe-gcp-github-template
gcloud --version
uv --version
```

2. 변수 설정
```bash
export PROJECT_ID="YOUR_PROJECT_ID"
export REGION="asia-northeast3"
export SERVICE_NAME="fastapi-backend"
export REPO_NAME="fastapi"
```

3. GCP 부트스트랩 실행 (`docs/gcp-project-bootstrap.md` 기준)
```bash
gcloud config set project "$PROJECT_ID"
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  iamcredentials.googleapis.com \
  secretmanager.googleapis.com \
  --project "$PROJECT_ID"

gcloud artifacts repositories create "$REPO_NAME" \
  --repository-format=docker \
  --location="$REGION" \
  --description="Template images" \
  --project "$PROJECT_ID"
```

4. Cloud Run 수동 배포 (1단계)
```bash
IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:manual-$(date +%Y%m%d%H%M%S)"

# 기본 경로 (Cloud Build)
gcloud builds submit --project "$PROJECT_ID" --tag "$IMAGE_URI" .

# Cloud Build 권한 제한 시 대체
# docker buildx build --platform linux/amd64 -t "$IMAGE_URI" --push .

gcloud run deploy "$SERVICE_NAME" \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --platform managed \
  --image "$IMAGE_URI" \
  --allow-unauthenticated \
  --set-env-vars APP_ENV=prod
```

5. 배포 확인
```bash
SERVICE_URL="$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --project "$PROJECT_ID" --format='value(status.url)')"
echo "$SERVICE_URL"
curl "$SERVICE_URL/"
curl "$SERVICE_URL/openapi.json"
```

다음 단계:

1. GitHub Actions + WIF 연동: `docs/github-actions-wif.md`
2. 상세 명령 레퍼런스: `docs/gcp-setup.md`

## 1) 로컬 실행

사전 요구사항:
- Python 3.11+
- `uv`

```bash
uv sync --dev
uv run uvicorn app.main:app --reload
```

확인:
- `GET http://127.0.0.1:8000/healthz`
- `GET http://127.0.0.1:8000/`

## 2) Cloud Run 수동 배포 (1단계)

먼저 GCP 리소스는 `docs/gcp-setup.md`를 따라 준비합니다.

```bash
export PROJECT_ID="YOUR_PROJECT_ID"
export REGION="asia-northeast3"
export SERVICE_NAME="fastapi-backend"
export REPO_NAME="fastapi"

IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:manual-$(date +%Y%m%d%H%M%S)"

gcloud builds submit --project "${PROJECT_ID}" --tag "${IMAGE_URI}" .

gcloud run deploy "${SERVICE_NAME}" \
  --project "${PROJECT_ID}" \
  --region "${REGION}" \
  --platform managed \
  --image "${IMAGE_URI}" \
  --allow-unauthenticated
```

## 3) GitHub Actions 자동화 (2단계)

2단계는 아래 3개 워크플로우로 동작합니다.

- `.github/workflows/ci-pr.yml`
  - `pull_request` 이벤트에서 테스트 수행
- `.github/workflows/auto-merge.yml`
  - 같은 저장소 브랜치 PR에 대해 auto-merge(squash) 활성화
- `.github/workflows/deploy.yml`
  - `main` push 또는 `ci-pr` 성공(`workflow_run`) 후 merge 완료 PR 기준 Cloud Run 배포

GitHub 저장소에서 아래 설정을 먼저 적용하세요.

1. `Settings > General`
   - `Allow auto-merge` 활성화
   - `Allow squash merging` 활성화
2. `Settings > Branches > Branch protection rules (main)`
   - `Require a pull request before merging` 활성화
   - `Require status checks to pass before merging` 활성화
   - Required checks: `unit-test`
   - Approvals: 0 (리뷰 없이 체크만)
   - 직접 `main` push 차단(권장)

GitHub 저장소에 아래 값을 등록하세요.

필수 Secrets:
- `WIF_PROVIDER`
- `WIF_SERVICE_ACCOUNT`

필수 Variables:
- `GCP_PROJECT_ID`
- `GCP_REGION` (`asia-northeast3`)
- `ARTIFACT_REPOSITORY`
- `CLOUD_RUN_SERVICE`
- `CLOUD_RUN_RUNTIME_SA`

3단계(DB 연동)부터 필요한 Variables:
- `INSTANCE_CONNECTION_NAME` (`project:region:instance`)
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD_SECRET` (Secret Manager secret name)

동작 검증 순서:

1. 기능 브랜치 생성 후 PR 생성
2. `ci-pr` 워크플로우에서 `unit-test` 성공 확인
3. PR이 auto-merge로 squash 머지되는지 확인
4. 머지 직후 `deploy-cloud-run` 워크플로우 실행/성공 확인

## 4) Cloud SQL(Postgres) 연결 + 마이그레이션 (3단계)

환경 변수는 `.env.example` 참고 후 `.env`를 만듭니다.

```bash
cp .env.example .env
```

Alembic 적용:

```bash
uv run alembic upgrade head
```

DB 연결 확인:
- `GET /db/healthz`
- `POST /items`
- `GET /items/{id}`

## API 엔드포인트

- `GET /`
- `GET /healthz`
- `GET /db/healthz`
- `POST /items`
- `GET /items/{item_id}`

## 참고

GCP 리소스 생성, IAM/WIF, Cloud SQL 연결 절차는 `docs/gcp-setup.md`에 정리되어 있습니다.
