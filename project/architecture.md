# Architecture

작성일: 2026-02-24 (KST)

## 현재 아키텍처 (1단계 기준)

- Client
  - 브라우저/`curl`
- Backend
  - FastAPI (`app.main`, `app.api.routes`)
  - 컨테이너: `Dockerfile`
  - 런타임: Cloud Run (`fastapi-backend`)
- Registry/Build
  - Artifact Registry: `asia-northeast3-docker.pkg.dev/vibe-fastapi-dev/fastapi`
  - 이미지: 수동 Docker 빌드 후 push
- Database
  - 코드 레벨 구현 완료(SQLAlchemy + Alembic)
  - 1단계 배포에서는 미연동

## 요청 흐름

1. 클라이언트 요청
2. Cloud Run 서비스 수신
3. FastAPI 라우터 처리
4. 응답 반환(JSON)
