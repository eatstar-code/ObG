# ObG v1.1 - Windows용 Docker 실행 가이드

이 문서는 Windows 환경에서 **Docker를 이용해 ObG (Omok by GPT) v1.1**을 실행하는 방법을 안내합니다.

---

## 📆 필요 도구

| 도구 | 다운로드 링크 | 설명 |
|------|----------------|------|
| Docker Desktop | [https://www.docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop) | Docker 실행 환경 |
| VcXsrv | [https://sourceforge.net/projects/vcxsrv/](https://sourceforge.net/projects/vcxsrv/) | Tkinter GUI 출력을 위한 X 서버 |

---

## ✅ 실행 순서

### 1️⃣ VcXsrv 실행

1. 설치 후 `XLaunch` 실행
2. 설정:
   - **Display settings**: Multiple windows
   - **Start no client** 선택
   - ✅ **Disable access control** 체크
3. Finish 클릭 → X 서버 실행됨 ( 작업표시줄에 아이콘 표시 )

---

### 2️⃣ Docker 이미지 설치

```bash
docker pull ghcr.io/eatstar-code/omok-gui:1.1
```

---

### 3️⃣ Docker로 프로그램 실행

```bash
docker run -it --rm -e DISPLAY=host.docker.internal:0 ghcr.io/eatstar-code/omok-gui:1.1
```

> ⚠ 위 명마에서 `DISPLAY=host.docker.internal:0` 는 반복 필요한 환경변수입니다. GUI가 정상 작동하기 위해 필요해요.

---

### 4️⃣ 게임 시작

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

- 이 버전은 `ghcr.io`를 통해 배포되며, 변경 없이 Docker만 있으면 실행 가능합니다.
- macOS 및 Linux 사용자는 [`mac_linux_package.md`](./mac_linux_package.md)를 참조해주세요.

---

© 2025 EATSTAR

