# Fullstack Risk Assessment Service


## How to use Github

GitHub로 협업하는 방법은 프로젝트의 성격과 팀의 협업 방식에 따라 다르지만, 일반적으로 다음과 같은 단계를 거친다.

### 1. **GitHub 저장소 생성 및 설정**
1. [GitHub](https://github.com/)에 접속하여 계정을 만든다.
2. 새로운 **Repository(저장소)**를 생성한다.
   - `Public` 또는 `Private` 중 선택 가능
   - `README.md`, `.gitignore`, 라이선스 설정 가능
3. 팀원이 접근할 수 있도록 `Settings` → `Manage access`에서 **Collaborator(협업자)**를 추가한다.

### 2. **로컬 환경 설정**

#### 2.1 Git 설치 및 초기 설정

1. Git이 설치되어 있는지 확인하고, 없으면 설치한다.
   ```bash
   git --version
   ```

2. 사용자 정보 설정
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

#### 2.2 저장소 복제 (Clone)

- 팀원이 저장소를 복제하여 로컬에서 작업할 수 있도록 한다.
   ```bash
   git clone https://github.com/username/repository.git
   ```
- 저장소로 이동
   ```bash
   cd repository
   ```

### 3. **브랜치 전략 설정**

#### 3.1 기본 브랜치 전략
- `main`(또는 `master`) 브랜치는 항상 안정적인 상태를 유지하도록 한다.
- 기능별로 새로운 브랜치를 만들어 작업한다.
  ```bash
  git checkout -b feature-branch
  ```
- 작업 후 변경사항을 커밋하고 푸시한다.
  ```bash
  git add .
  git commit -m "기능 추가"
  git push origin feature-branch
  ```

#### 3.2 브랜치 전략 예시
- [] **Git Flow**: `main`, `develop`, `feature`, `release`, `hotfix` 브랜치 활용
- [x] **GitHub Flow**: `main` + `feature` 브랜치, PR 기반
- [] **Trunk-based Development**: `main`에서 직접 개발 후 작은 단위로 병합

### 4. **Pull Request(PR)로 코드 리뷰**
1. 브랜치에서 작업한 후 GitHub에서 **Pull Request (PR)**를 생성한다.
2. 코드 리뷰 후 승인되면 `main` 브랜치에 병합한다.
3. 병합 후 로컬 저장소를 최신 상태로 유지
   ```bash
   git checkout main
   git pull origin main
   ```

### 5. **충돌 해결 및 협업 팁**

#### 5.1 최신 코드 유지 (Pull & Rebase)
```bash
git checkout feature-branch
git pull --rebase origin main
```
- `pull --rebase`를 사용하면 불필요한 병합 커밋을 줄일 수 있음

#### 5.2 충돌 해결
- 충돌이 발생하면 수동으로 수정한 후 다시 커밋
  ```bash
  git add .
  git commit -m "충돌 해결"
  ```

#### 5.3 커밋 메시지 규칙
- 일관된 커밋 메시지를 유지하면 협업이 편리해짐
  - `feat:` 기능 추가
  - `fix:` 버그 수정
  - `docs:` 문서 수정
  - `refactor:` 코드 개선
  - `test:` 테스트 코드 추가

### 6. **GitHub Actions & CI/CD 활용**
- 자동화된 테스트 및 배포를 설정하여 코드 품질을 유지할 수 있음
- `.github/workflows/` 디렉터리에 **CI/CD 파이프라인**을 설정하여 코드 푸시 시 자동 빌드 및 테스트 실행

### 7. **이슈 및 프로젝트 관리**
- `Issues`를 활용하여 버그 및 작업 목록 관리
- `Projects`(Kanban Board)로 할당된 작업을 시각적으로 관리
- `Wiki`를 활용하여 팀 내 기술 문서 정리

### 🚀 **협업 요약**

✅ GitHub 저장소 생성 및 팀원 추가  
✅ `git clone`으로 로컬 환경 설정  
✅ 브랜치 전략에 따라 기능별 개발 (`git checkout -b`)  
✅ PR을 통한 코드 리뷰 및 병합 (`git pull --rebase`)  
✅ 충돌 해결 후 푸시 (`git commit -m "Resolve conflict"`)  
✅ CI/CD 및 Issues, Projects 활용하여 프로젝트 관리

이 방식으로 협업하면 원활한 GitHub 기반 개발이 가능하다.