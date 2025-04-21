# omok.py

import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

# --- 설정 값 ---
BOARD_SIZE = 15
STAR_POINTS = [(3,3), (3,11), (7,7), (11,3), (11,11)]

# --- 사이드바: 사용자 정보 입력 ---
st.sidebar.title("게임 설정")
player_black = st.sidebar.text_input("흑 플레이어 이름", value="Black")
player_white = st.sidebar.text_input("백 플레이어 이름", value="White")
time_limit_min = st.sidebar.number_input("제한 시간 (분)", min_value=1, max_value=60, value=20)
game_name = st.sidebar.text_input("게임 이름", value="OMOK by GPT")
if st.sidebar.button("게임 시작"):
    st.session_state.started = True
    st.session_state.start_time = datetime.now()
    st.session_state.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    st.session_state.current = 1  # 1=흑, 2=백

if 'started' not in st.session_state:
    st.session_state.started = False

# --- 타이틀 ---
st.title(f"{game_name} (Web Version)")

# --- 오목판 그리기 함수 ---
def draw_board(board):
    fig, ax = plt.subplots(figsize=(6,6))
    # 전체 배경 흰색, 판 영역만 베이지
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#F0D9B5')

    # 격자
    for i in range(BOARD_SIZE):
        ax.plot([0, BOARD_SIZE-1], [i, i], color='black', zorder=1)
        ax.plot([i, i], [0, BOARD_SIZE-1], color='black', zorder=1)

    # 화점
    for x, y in STAR_POINTS:
        ax.scatter(x, y, s=50, color='black', zorder=1)

    # 돌
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y, x] == 1:
                ax.scatter(x, y, s=200, color='black', zorder=3)
            elif board[y, x] == 2:
                ax.scatter(
                    x, y, s=200,
                    facecolors='white', edgecolors='black',
                    linewidths=1.5, zorder=4
                )

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-1, BOARD_SIZE)
    ax.set_ylim(-1, BOARD_SIZE)
    ax.set_aspect('equal')
    st.pyplot(fig)

# --- 메인 화면 로직 ---
if st.session_state.started:
    # 1) 오목판 먼저 렌더링
    draw_board(st.session_state.board)

    # 2) 현재 차례 표시
    turn = "흑" if st.session_state.current == 1 else "백"
    current_player = player_black if turn == "흑" else player_white
    st.markdown(f"**현재 차례: {turn} ({current_player})**")

    # 3) 그 아래에 좌표 입력 폼
    with st.form("move_form"):
        col = st.number_input("가로 좌표 (0~14)", min_value=0, max_value=BOARD_SIZE-1, step=1)
        row = st.number_input("세로 좌표 (0~14)", min_value=0, max_value=BOARD_SIZE-1, step=1)
        if st.form_submit_button("착수"):
            if st.session_state.board[row, col] == 0:
                st.session_state.board[row, col] = st.session_state.current
                st.session_state.current = 3 - st.session_state.current
            else:
                st.warning("⚠️ 이미 돌이 놓여 있습니다.")

    # TODO:
    # - 5목 승리 검사
    # - 제한 시간 타이머
    # - 전적 저장 및 불러오기
    # - 업데이트 내역 표시

else:
    st.info("사이드바에서 플레이어 이름, 시간, 게임 이름을 설정하고 '게임 시작' 버튼을 눌러주세요.")
