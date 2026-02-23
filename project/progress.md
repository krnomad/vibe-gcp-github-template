# Progress

작성일시: 2026-02-24 00:16:48 KST

## 현재 상태 요약

- Cloud Run 수동 배포 완료
- 서비스명: `fastapi-backend`
- 프로젝트/리전: `vibe-fastapi-dev` / `asia-northeast3`
- 최신 리비전: `fastapi-backend-00002-dvk`
- 트래픽: 최신 리비전 100%
- 서비스 URL: `https://fastapi-backend-gddhqf47hq-du.a.run.app`

## 검증 결과

- `GET /` -> `200`
  - 응답: `{"service":"fastapi-cloud-run-lab","environment":"prod"}`
- `GET /openapi.json` -> `200`
- `GET /healthz` -> `404` (Google 404 HTML 응답)
- `GET /db/healthz` -> `503`
  - 응답: `Database is not configured: Missing DB settings: DB_NAME, DB_USER, DB_PASSWORD`

## 배포 중 이슈/해결

- 이슈: Cloud Build(`gcloud builds submit`)에서 `PERMISSION_DENIED`
- 우회: 로컬 Docker 빌드 + Artifact Registry push + Cloud Run deploy
- 이슈: ARM 이미지 배포 시 컨테이너 기동 실패
- 해결: `docker buildx build --platform linux/amd64 --push`로 재배포
