# GCP FastAPI 실습 계획

작성일: 2026-02-23

## 목표
- GCP를 사용해 FastAPI 백엔드를 단계적으로 배포/확장한다.
1. FastAPI를 Cloud Run에 수동 배포해 기본 동작 확인
2. GitHub `main` push 시 자동 배포(GitHub Actions + OIDC/WIF)
3. Cloud SQL(Postgres) 연동 및 Alembic 마이그레이션 적용

## 확정된 기술 선택
- 인증: GitHub OIDC + Workload Identity Federation(WIF)
- 인프라 설정 방식: gcloud CLI
- 리전: `asia-northeast3`
- 의존성/실행 관리: `uv`
- DB 스택: SQLAlchemy 2.x + asyncpg
- 마이그레이션: Alembic
- 실습 구성: 단일 `main` 브랜치에서 점진 확장

## 단계별 계획

### 1단계: FastAPI → Cloud Run 수동 배포
- FastAPI 앱 기본 엔드포인트 구성
  - `GET /`
  - `GET /healthz`
- Dockerfile 기반 컨테이너 이미지 빌드
- Artifact Registry 푸시 후 Cloud Run 수동 배포
- Cloud Run URL에서 200 응답 확인

### 2단계: GitHub Actions 자동 배포
- Workload Identity Pool/Provider 생성
- GitHub Actions 배포용 서비스 계정 구성 및 최소 권한 부여
- GitHub 저장소 Secrets/Variables 등록
- `.github/workflows/deploy.yml` 구성
  - 트리거: `main` 브랜치 push
  - 테스트 통과 후 이미지 빌드/푸시
  - Cloud Run 배포

### 3단계: Cloud SQL(Postgres) 연동
- Cloud SQL 인스턴스/DB/사용자 생성
- DB 비밀번호 Secret Manager 저장
- Cloud Run에 Cloud SQL 연결 설정
- 앱에 DB 세션/모델/CRUD 엔드포인트 추가
  - `GET /db/healthz`
  - `POST /items`
  - `GET /items/{id}`
- Alembic 초기 마이그레이션 적용

## 테스트 및 검증 기준
- 단위 테스트: health/root 엔드포인트
- 통합 검증: DB 연결/CRUD 동작
- 배포 검증: main push 후 Cloud Run 최신 리비전 반영
- 완료 기준:
  - main push만으로 자동 배포 수행
  - Cloud SQL read/write 엔드포인트 동작
  - Alembic 마이그레이션 이력 관리 가능

## 참고 문서
- 실습 안내: `README.md`
- GCP 설정 가이드: `docs/gcp-setup.md`
- 완료 기록: `docs/progress-completed.md`
