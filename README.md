# ObG (Omok by GPT)

## 📑 목차
- [ObG는 무엇인가요?](#obg는-무엇인가요)
- [업데이트 내역](#업데이트-내역)
  - [v1.0 – 2025-04-20](#v10-–-2025-04-20)
- [구현된 주요 기능](#구현된-주요-기능)
- [향후 로드맵](#향후-로드맵)
- [프로그램을 위해 도와주세요!](#프로그램을-위해-도와주세요)
- [다운로드](#다운로드)

---

## ObG는 무엇인가요?
ObG는 **Omok by GPT**의 약자로, ChatGPT를 활용해 개발한 GUI 기반 오목 프로그램입니다.  
기존에 C언어로 텍스트 기반 오목을 구현한 경험을 바탕으로, ChatGPT에 로직을 구현·디버깅하도록 요청하여 빠르게 틀을 잡고 완성했습니다.  
실제 개발 기간 중 약 2시간은 오류를 해결하며 ChatGPT와 주고받은 디버깅 시간이었지만, 그 과정이 매우 흥미로웠습니다.

---

## 업데이트 내역

### v1.0 – 2025-04-20
**작성자**: EATSTAR (https://github.com/eatstar-code)  
**개발 도구**: ChatGPT o4-mini-high, Visual Studio Code  
**개발 기간**: 약 2시간 반 (exe 배포 작업 제외)

---

## 구현된 주요 기능
- **GUI 기반 오목 시스템**  
- **게임 정보 입력**  
  - 게임 이름  
  - 대국 일시 (YYYY-MM-DD HH:MM)  
  - 제한 시간(분)  
  - 흑/백 플레이어 이름  
- **게임 규칙**  
  - 시간 초과 시 기권 패배 처리  
  - 5줄 완성 시 승리  
- **게임 종료 후 전적 관리**  
  - 전적 저장 및 조회 기능 제공

---

## 향후 로드맵
1. **금수(3·3, 6목) 규칙 검출 및 방지**  
2. **AI 대국 기능** 구현  
3. **전적 데이터베이스 연동**  (장기 저장 및 분석)  

> 최우선 과제: 전적 DB 연동 (v1.1 목표)

---

## 프로그램을 위해 도와주세요!
프로그램 발전을 위해 의견이나 제안이 있다면 아래 연락처로 알려주세요:  
📧 eatstar.code@gmail.com

---

## 다운로드
### ObG v1.0 (Windows)
Python 설치 없이 바로 실행 가능한 EXE 파일을 제공합니다.  

[설치형 파일](https://drive.google.com/file/d/13idUxS4BbB_giOrATfSWCNPxb7VGsVCN/view?usp=sharing)

[디펜더 해제 방법](https://kissi-pro.tistory.com/entry/%ED%8C%8C%EC%9D%BC%EC%97%90-%EB%B0%94%EC%9D%B4%EB%9F%AC%EC%8A%A4-%EB%98%90%EB%8A%94-%EA%B8%B0%ED%83%80-%EC%82%AC%EC%9A%A9%EC%9E%90-%EB%8F%99%EC%9D%98-%EC%97%86%EC%9D%B4-%EC%84%A4%EC%B9%98%EB%90%9C-%EC%86%8C%ED%94%84%ED%8A%B8%EC%9B%A8%EC%96%B4%EA%B0%80-%EC%9E%88%EA%B8%B0-%EB%95%8C%EB%AC%B8%EC%97%90-%EC%9E%91%EC%97%85%EC%9D%B4-%EC%99%84%EB%A3%8C%EB%90%98%EC%A7%80-%EC%95%8A%EC%95%98%EC%8A%B5%EB%8B%88%EB%8B%A4)
### 현재 바이러스 오탐지로 Windows Defender를 해제 후 실행하시거나, Visual Studio Code에 코드를 직접 입력하셔서 실행해야 합니다.

---

*© 2025 EATSTAR*

---
