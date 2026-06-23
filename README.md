# Python Development with UV

이 프로젝트는 Rust로 작성된 초고속 파이썬 패키지 및 가상환경 관리 도구인 **UV**를 사용하여 환경이 설정되어 있습니다.

## 🛠️ UV 설치 정보

`pip`를 통해 사용자 라이브러리 경로에 `uv`가 설치되었습니다.
- **실행 파일 경로**: `/Users/chrisj0923/Library/Python/3.10/bin/uv`

### 터미널에서 `uv` 명령어를 바로 사용하기 (PATH 설정)

터미널에서 `uv` 명령어를 직접 실행할 수 있도록 쉘 설정 파일(`~/.zshrc`)에 경로를 추가해 주세요:

```bash
# ~/.zshrc 파일에 경로 추가
echo 'export PATH="$HOME/Library/Python/3.10/bin:$PATH"' >> ~/.zshrc

# 설정 반영
source ~/.zshrc
```

---

## 🚀 프로젝트 사용 방법

### 1. 프로그램 실행
`uv run`을 사용하면 필요한 파이썬 가상환경(`.venv`)을 자동으로 생성 및 활성화하여 스크립트를 실행합니다.

```bash
uv run main.py
```

### 2. 패키지 추가
프로젝트에 필요한 의존성 패키지를 추가하려면 `uv add`를 사용합니다. (패키지가 자동으로 `pyproject.toml` 및 `uv.lock`에 기록됩니다.)

```bash
uv add <패키지명>
# 예: uv add requests
```

### 3. 패키지 제거
설치된 패키지를 제거하려면 `uv remove`를 사용합니다.

```bash
uv remove <패키지명>
# 예: uv remove requests
```

---

## 📂 프로젝트 파일 구성

- `pyproject.toml`: 프로젝트 메타데이터 및 의존성 패키지 정의 파일
- `uv.lock`: 정확한 패키지 버전을 잠금 관리하는 파일
- `.python-version`: 프로젝트에서 사용할 파이썬 버전 명시 (`3.10`)
- `.venv/`: `uv`가 관리하는 가상환경 디렉터리
- `main.py`: 실행용 진입점 스크립트 파일
