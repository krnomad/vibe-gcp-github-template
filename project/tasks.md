# Tasks

작성일: 2026-02-24 (KST)

## 완료

- [x] FastAPI 앱 기본 엔드포인트 구현
- [x] Dockerfile 작성
- [x] Artifact Registry 저장소 생성 (`fastapi`)
- [x] Cloud Run 수동 배포 완료
- [x] `GET /` 실동작 확인

## 진행 중 / 다음 작업

- [ ] `/healthz` 404 원인 분석 및 수정
- [ ] Cloud Build `PERMISSION_DENIED` 원인 확정(권한/조직정책)
- [ ] GitHub Actions 자동 배포(2단계) end-to-end 검증
- [ ] Cloud SQL + Secret Manager + `/db/healthz` 200 검증(3단계)
- [ ] `POST /items`, `GET /items/{id}` 실환경 검증
