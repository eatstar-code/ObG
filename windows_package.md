# ObG v1.x - Windows용 Docker 실행 가이드

이 문서는 Windows 환경에서 **Docker를 이용해 ObG (Omok by GPT) v1.x**을 실행하는 방법을 안내합니다.<br>
아래 코드에서 제시된 1.x는 버전에 맞게 고쳐주세요.

---

## 📦 필요 도구

| 도구 | 다운로드 링크 | 설명 |
|------|----------------|------|
| Docker Desktop | [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) | Docker 이미지 기능 프로그램 실행 |
| VcXsrv (XLaunch) | [https://sourceforge.net/projects/vcxsrv/](https://sourceforge.net/projects/vcxsrv/) | GUI 출력용 X 서버 (Tkinter 지원) |

---

## ⚙️ 시스템 사전 설정 (최초 1회만)

### ✅ WSL 업데이트

> 아래 방법으로 명령어(cmd) 창을 실행하세요:
> - **Windows + R** 키를 누르고 `cmd` 입력 후 Enter
> - 또는 시작 메뉴에서 '명령 프롬프트'를 검색하여 실행

```bash
wsl --update
```

> 위 코드를 붙여놓기 하고 Enter

### ✅ Docker Desktop 최초 실행 및 로그인

1. `Docker Desktop` 실행
2. **Google 계정 또는 GitHub 계정으로 로그인** 필요
3. 로그인 후 오른쪽 하단 작업표시줄에 🐳 아이콘이 보이면 완료

> 이후에는 `.bat` 파일이 자동으로 실행해줍니다.

### ✅ VcXsrv 설치

> X 서버는 `.bat` 파일이 자동으로 실행시켜주기 때문에, **한 번도 실행하지 않은 상태여도 무방**합니다.

---

## 🚀 실행 방법

### ✅ 가장 쉬운 방법: `ObG_auto_excute.bat` 더블 클릭

> `.bat` 파일 하나로 모든 실행 절차가 자동화되어 있습니다.

자동 수행 항목:
- ✅ **Docker Desktop 실행 여부 확인 및 자동 실행**
- ✅ **VcXsrv 실행 여부 확인 및 자동 실행 (설치만 되어 있으면 자동 실행 가능)**
- ✅ Docker 이미지 다운로드 (`ghcr.io/eatstar-code/obg:1.x`)
- ✅ 전적 DB 파일 (`omok.db`) 유무 확인 및 안내
- ✅ 프로그램 실행

[.bat 파일, .db 파일 다운로드](https://drive.google.com/file/d/1zJCP5A0Z5sBZpOHvbLllF1gu9Wkm0fB6/view?usp=sharing)[br]
위 파일을 다운로드 받은 후 압축을 풀고, `ObG_auto_excute.bat` 파일을 더블 클릭하세요.

---

## 🛠️ 수동 실행 (Cmd나 Powershell을 직접 사용)

### 1. Docker Desktop 실행

1. **시작 메뉴 또는 바탕화면에서 `Docker Desktop` 실행**
2. 오른쪽 하단 작업표시줄에 🐳 아이콘이 보이면 준비 완료

### 2. VcXsrv (XLaunch) 수동 실행

1. `XLaunch` 실행
2. 아래 설정을 순서대로 적용:
   - **Multiple windows**
   - **Start no client**
   - ✅ **Disable access control** 체크
3. Finish 클릭 후 트레이에 X 아이콘이 보이면 실행 완료

### 3. Docker 이미지 다운로드

```bash
docker pull ghcr.io/eatstar-code/obg:1.x
```

### 4. 프로그램 실행

```bash
docker run -it --rm ^
  -e DISPLAY=host.docker.internal:0 ^
  -v "C:\Your\Path\omok.db":/app/omok.db ^
  ghcr.io/eatstar-code/obg:1.x
```

> `C:\Your\Path\omok.db`는 실제 DB 파일 경로로 변경해주세요.

---

## 🎮 게임 시작

- 프로그램이 실행되면 `게임 정보 입력` 창이 표시됩니다.
- 게임 이름, 대국 일시, 제한 시간, 플레이어 정보를 입력하고 [확인]을 눌러 게임을 시작하세요.
- 전적은 자동으로 저장되며, 다음 시작 시에도 불러올 수 있습니다.

---

## 🧑‍💻 제작자 정보

- **제작자**: EATSTAR (이트스타)  
- [GitHub](https://github.com/eatstar-code) | [Blog](https://eatstar.tistory.com)

---



---

## ❓ 오류 해결

| 오류 메시지 | 해결 방법 |
|-------------|-----------|
| `no display name and no $DISPLAY` | VcXsrv 실행 여부, DISPLAY 환경변수 설정 확인 |
| 실행 시 아무 반응 없음 | VcXsrv에 `Disable access control` 체크했는지 확인 |

---

## 📘 참고

- 이미 두 프로그램이 깔려있다면, 두 프로그램을 모두 실행시키고 이미지 설치, 실행하시면 됩니다.
- macOS 및 Linux 사용자는 ~를 참조해주세요.

---

© 2025 EATSTAR

