# Decisions

작성일: 2026-02-24 (KST)

## 결정 사항

1. 리전은 `asia-northeast3` 고정
2. 1단계 배포는 DB 연결 없이 `APP_ENV=prod`만 설정
3. Cloud Build 권한 이슈 구간에서는 로컬 Docker 경로 사용
4. Cloud Run 호환성 위해 이미지 플랫폼은 `linux/amd64` 사용
5. 2단계부터 GitHub Actions + OIDC/WIF 기반 배포 유지
6. 2단계 워크플로우는 PR CI(`ci-pr`) + auto-merge + `main` push 배포(`deploy`)로 분리
7. auto-merge 전략은 `squash` 고정, 리뷰 승인 수는 0(체크 기반 게이트)
8. `main` 브랜치 required check 이름은 `unit-test`로 고정

## 관찰된 리스크

- `/healthz`가 외부 호출에서 404로 응답(원인 추가 확인 필요)
- 조직/프로젝트 정책으로 Cloud Build 경로가 제한될 가능성
