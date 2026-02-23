# 진행 완료 기록

작성일: 2026-02-23

## 1. 프로젝트 초기 구성 완료
- `pyproject.toml` 작성 (`uv` 기반 의존성 정의)
- `.gitignore`, `.dockerignore`, `.env.example` 추가
- 기본 디렉터리 구조 생성
  - `app/`, `app/api/`, `app/db/`, `app/schemas/`
  - `alembic/`, `alembic/versions/`
  - `tests/`, `.github/workflows/`, `docs/`

## 2. FastAPI 백엔드 코드 구현 완료
- 앱 엔트리포인트 구성: `app/main.py`
- API 엔드포인트 구현: `app/api/routes.py`
  - `GET /`
  - `GET /healthz`
  - `GET /db/healthz`
  - `POST /items`
  - `GET /items/{item_id}`
- 설정 로직 구현: `app/config.py`
  - 로컬 TCP / Cloud Run Cloud SQL socket 연결 URL 분기
- DB 세션 구성: `app/db/session.py`
- SQLAlchemy 모델 구현: `app/db/models.py` (`items` 테이블)
- Pydantic 스키마 구현: `app/schemas/item.py`

## 3. 마이그레이션 구성 완료
- Alembic 설정 파일 작성: `alembic.ini`, `alembic/env.py`, `alembic/script.py.mako`
- 초기 마이그레이션 추가: `alembic/versions/20260223_0001_create_items_table.py`

## 4. 배포 구성 완료
- Cloud Run용 컨테이너 파일 작성: `Dockerfile`
- GitHub Actions 배포 워크플로우 작성: `.github/workflows/deploy.yml`
  - 트리거: `main` 브랜치 push
  - 단계: 테스트 → OIDC 인증 → 이미지 빌드/푸시 → Cloud Run 배포
  - DB 미연동(2단계) / DB 연동(3단계) 조건 분기 반영

## 5. 문서화 완료
- 실습 개요 및 실행 절차 정리: `README.md`
- GCP 리소스/IAM/WIF/Cloud SQL 설정 절차 정리: `docs/gcp-setup.md`

## 6. 검증 완료 항목
- Python 문법 컴파일 확인 완료
  - `app/`, `alembic/`, `tests/` 대상 `compileall` 통과
- GitHub Actions 워크플로우 YAML 파싱 확인 완료
