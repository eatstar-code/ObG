# ObG v1.1 - Windows용 Docker 실행 가이드

이 문서는 Windows 환경에서 **Docker를 이용해 ObG (Omok by GPT) v1.x**을 실행하는 방법을 안내합니다.

---

## 📆 필요 도구

| 도구 | 다운로드 링크 | 설명 |
|------|----------------|------|
| Docker Desktop | [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) | Docker 실행 환경 |
| VcXsrv | [https://sourceforge.net/projects/vcxsrv/](https://sourceforge.net/projects/vcxsrv/) | Tkinter GUI 출력을 위한 X 서버 |

---

## ✅ 실행 순서

### 1️⃣ Docker Desktop 실행 

1. 설치 후 바탕화면 또는 시작 메뉴에서 `Docker Desktop` 실행
2. 작업표시줄에 🐳 고래 아이콘이 뜨면 실행 완료!

### 2️⃣ VcXsrv 실행

1. 설치 후 `XLaunch` 실행
2. 설정:
   - **Display settings**: Multiple windows
   - **Start no client** 선택
   - ✅ **Disable access control** 체크
3. Finish 클릭 → X 서버 실행됨 ( 작업표시줄에 아이콘 표시 )

### 3️⃣ Docker 이미지 설치

cmd에서 명령어를 입력. (예: 1.1 버전인 경우, 1.x를 1.1로 바꾸세요)
```bash
docker pull ghcr.io/eatstar-code/omok-gui:1.x
```

### 4️⃣ Docker로 프로그램 실행

cmd에서 이어서 명령어를 입력.
```bash
docker run -it --rm -e DISPLAY=host.docker.internal:0 ghcr.io/eatstar-code/omok-gui:1.x
```

또는

Docker Desktop > Images에서 실행
단, 실행하면 나오는 Optimal Setting의 Environment variables에서 
Variable과 Value에 각각 DISPLAY, host.docker.internal:0를 넣고 실행해야 함.

### 5️⃣ 게임 시작

- GUI 창이 들어오면 `게임 정보 입력` 창이 표시됩니다.
- 이름, 시간, 플레이어 정보를 입력하고 게임을 시작하세요!

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

