# GCP 설정 가이드 (asia-northeast3)

아래 순서대로 실행하면 이 저장소의 GitHub Actions 배포 구성이 동작합니다.

## 0. 기본 변수

```bash
export PROJECT_ID="YOUR_PROJECT_ID"
export PROJECT_NUMBER="$(gcloud projects describe "$PROJECT_ID" --format='value(projectNumber)')"
export REGION="asia-northeast3"

export SERVICE_NAME="fastapi-backend"
export REPO_NAME="fastapi"
export SQL_INSTANCE="fastapi-db"
export SQL_DB="app"
export SQL_USER="app"

export DEPLOY_SA="github-deployer"
export RUNTIME_SA="cloud-run-runtime"

export GH_OWNER="YOUR_GITHUB_OWNER"
export GH_REPO="YOUR_GITHUB_REPO"

export WIF_POOL="github-pool"
export WIF_PROVIDER="github-provider"
```

## 1. API 활성화

```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  sqladmin.googleapis.com \
  secretmanager.googleapis.com \
  iamcredentials.googleapis.com \
  --project "$PROJECT_ID"
```

## 2. Artifact Registry 생성

```bash
gcloud artifacts repositories create "$REPO_NAME" \
  --repository-format=docker \
  --location="$REGION" \
  --description="FastAPI images" \
  --project "$PROJECT_ID"
```

## 3. 서비스 계정 생성

```bash
gcloud iam service-accounts create "$DEPLOY_SA" --project "$PROJECT_ID"
gcloud iam service-accounts create "$RUNTIME_SA" --project "$PROJECT_ID"

export DEPLOY_SA_EMAIL="${DEPLOY_SA}@${PROJECT_ID}.iam.gserviceaccount.com"
export RUNTIME_SA_EMAIL="${RUNTIME_SA}@${PROJECT_ID}.iam.gserviceaccount.com"
```

## 4. 배포용 권한 부여 (OIDC로 사용할 SA)

```bash
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${DEPLOY_SA_EMAIL}" \
  --role="roles/run.admin"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${DEPLOY_SA_EMAIL}" \
  --role="roles/artifactregistry.writer"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${DEPLOY_SA_EMAIL}" \
  --role="roles/iam.serviceAccountUser"
```

## 5. Cloud Run 런타임 SA 권한

```bash
gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${RUNTIME_SA_EMAIL}" \
  --role="roles/cloudsql.client"

gcloud projects add-iam-policy-binding "$PROJECT_ID" \
  --member="serviceAccount:${RUNTIME_SA_EMAIL}" \
  --role="roles/secretmanager.secretAccessor"
```

## 6. Cloud SQL(Postgres) 생성

```bash
gcloud sql instances create "$SQL_INSTANCE" \
  --database-version=POSTGRES_16 \
  --region="$REGION" \
  --cpu=1 --memory=3840MiB \
  --project "$PROJECT_ID"

gcloud sql databases create "$SQL_DB" \
  --instance="$SQL_INSTANCE" \
  --project "$PROJECT_ID"

gcloud sql users create "$SQL_USER" \
  --instance="$SQL_INSTANCE" \
  --password="CHANGE_ME_STRONG_PASSWORD" \
  --project "$PROJECT_ID"

export INSTANCE_CONNECTION_NAME="$(gcloud sql instances describe "$SQL_INSTANCE" --project "$PROJECT_ID" --format='value(connectionName)')"
```

## 7. DB 비밀번호 Secret Manager 저장

```bash
echo -n "CHANGE_ME_STRONG_PASSWORD" | gcloud secrets create db-password \
  --data-file=- \
  --replication-policy="automatic" \
  --project "$PROJECT_ID"
```

이미 존재하면 새 버전 추가:

```bash
echo -n "CHANGE_ME_STRONG_PASSWORD" | gcloud secrets versions add db-password \
  --data-file=- \
  --project "$PROJECT_ID"
```

## 8. Workload Identity Federation (GitHub OIDC)

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

GitHub OIDC 주체에 서비스 계정 토큰 생성 권한 부여:

```bash
export WIF_POOL_NAME="projects/${PROJECT_NUMBER}/locations/global/workloadIdentityPools/${WIF_POOL}"

gcloud iam service-accounts add-iam-policy-binding "$DEPLOY_SA_EMAIL" \
  --role="roles/iam.workloadIdentityUser" \
  --member="principalSet://iam.googleapis.com/${WIF_POOL_NAME}/attribute.repository/${GH_OWNER}/${GH_REPO}" \
  --project "$PROJECT_ID"
```

Provider 전체 리소스명 확인:

```bash
gcloud iam workload-identity-pools providers describe "$WIF_PROVIDER" \
  --workload-identity-pool="$WIF_POOL" \
  --location="global" \
  --project "$PROJECT_ID" \
  --format="value(name)"
```

## 9. GitHub 저장소 설정값

### GitHub Secrets
- `WIF_PROVIDER`: 위 명령으로 얻은 provider resource name
- `WIF_SERVICE_ACCOUNT`: `${DEPLOY_SA_EMAIL}`

### GitHub Variables
- `GCP_PROJECT_ID`: `${PROJECT_ID}`
- `GCP_REGION`: `${REGION}`
- `ARTIFACT_REPOSITORY`: `${REPO_NAME}`
- `CLOUD_RUN_SERVICE`: `${SERVICE_NAME}`
- `CLOUD_RUN_RUNTIME_SA`: `${RUNTIME_SA_EMAIL}`
- `INSTANCE_CONNECTION_NAME`: `${INSTANCE_CONNECTION_NAME}`
- `DB_NAME`: `${SQL_DB}`
- `DB_USER`: `${SQL_USER}`
- `DB_PASSWORD_SECRET`: `db-password`

## 10. 배포 후 점검

```bash
SERVICE_URL="$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --project "$PROJECT_ID" --format='value(status.url)')"

echo "$SERVICE_URL"
curl "$SERVICE_URL/healthz"
curl "$SERVICE_URL/db/healthz"
```
