# GCP Project Bootstrap

작성일: 2026-02-24 (KST)

신규 GCP 프로젝트를 이 템플릿에 맞게 빠르게 준비하기 위한 가이드.

## 0) 변수 정의

아래 값을 먼저 채운다.

```bash
export PROJECT_ID="YOUR_PROJECT_ID"
export REGION="asia-northeast3"
export SERVICE_NAME="fastapi-backend"
export REPO_NAME="fastapi"

export DEPLOY_SA="github-deployer"
export RUNTIME_SA="cloud-run-runtime"
```

선택(신규 프로젝트 생성 시):

```bash
export BILLING_ACCOUNT_ID="YOUR_BILLING_ACCOUNT_ID"
```

## 1) 프로젝트 생성/선택

이미 프로젝트가 있으면 `gcloud config set project`만 실행한다.

```bash
# 신규 생성 (선택)
gcloud projects create "$PROJECT_ID"

# Billing 연결 (선택)
gcloud billing projects link "$PROJECT_ID" \
  --billing-account "$BILLING_ACCOUNT_ID"

# 현재 작업 프로젝트 지정
gcloud config set project "$PROJECT_ID"
```

## 2) 기본 API 활성화

```bash
gcloud services enable \
  run.googleapis.com \
  artifactregistry.googleapis.com \
  cloudbuild.googleapis.com \
  iamcredentials.googleapis.com \
  secretmanager.googleapis.com \
  --project "$PROJECT_ID"
```

## 3) Artifact Registry 준비

```bash
gcloud artifacts repositories create "$REPO_NAME" \
  --repository-format=docker \
  --location="$REGION" \
  --description="Template images" \
  --project "$PROJECT_ID"
```

이미 있으면 아래로 확인:

```bash
gcloud artifacts repositories describe "$REPO_NAME" \
  --location="$REGION" \
  --project "$PROJECT_ID"
```

## 4) 서비스 계정 생성

```bash
gcloud iam service-accounts create "$DEPLOY_SA" --project "$PROJECT_ID"
gcloud iam service-accounts create "$RUNTIME_SA" --project "$PROJECT_ID"

export DEPLOY_SA_EMAIL="${DEPLOY_SA}@${PROJECT_ID}.iam.gserviceaccount.com"
export RUNTIME_SA_EMAIL="${RUNTIME_SA}@${PROJECT_ID}.iam.gserviceaccount.com"
```

## 5) 권한 최소 부여(초기값)

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

## 6) 수동 배포 검증(1단계)

```bash
IMAGE_URI="${REGION}-docker.pkg.dev/${PROJECT_ID}/${REPO_NAME}/${SERVICE_NAME}:manual-$(date +%Y%m%d%H%M%S)"

# 방법 A: Cloud Build
gcloud builds submit --project "$PROJECT_ID" --tag "$IMAGE_URI" .

# 방법 B: 로컬 Docker (Cloud Build 제한 시)
# docker buildx build --platform linux/amd64 -t "$IMAGE_URI" --push .

gcloud run deploy "$SERVICE_NAME" \
  --project "$PROJECT_ID" \
  --region "$REGION" \
  --platform managed \
  --image "$IMAGE_URI" \
  --allow-unauthenticated \
  --set-env-vars APP_ENV=prod
```

## 7) 검증

```bash
SERVICE_URL="$(gcloud run services describe "$SERVICE_NAME" \
  --region "$REGION" --project "$PROJECT_ID" --format='value(status.url)')"

echo "$SERVICE_URL"
curl "$SERVICE_URL/"
curl "$SERVICE_URL/openapi.json"
```

## 8) 다음 단계

GitHub 자동 배포 연동은 `docs/github-actions-wif.md` 참고.
