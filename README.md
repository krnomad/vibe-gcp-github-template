# FastAPI + Cloud Run + GitHub Actions + Cloud SQL(Postgres) 실습

이 저장소는 아래 3단계를 한 번에 실습할 수 있도록 구성되어 있습니다.

1. FastAPI를 Cloud Run에 수동 배포
2. `main` 브랜치 push 시 GitHub Actions로 자동 배포
3. Cloud SQL(Postgres) 연동 + Alembic 마이그레이션

## Start Here (템플릿 운용 문서)

아래 문서 순서대로 확인한 뒤 작업을 진행하세요.

1. `docs/00-start-here.md`
2. `docs/gcp-project-bootstrap.md`
3. `docs/github-actions-wif.md`
4. `docs/gcp-setup.md`

에이전트 실행 규칙은 `AGENTS.md`에 정리되어 있습니다.

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

## 3) GitHub Actions 자동 배포 (2단계)

`.github/workflows/deploy.yml`는 `main` push 시 테스트 후 배포합니다.

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
