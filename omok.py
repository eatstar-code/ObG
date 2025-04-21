# omok.py

import streamlit as st
import numpy as np
from datetime import datetime

# --- 설정 값 ---
BOARD_SIZE = 15

# --- 사이드바: 게임 설정 ---
st.sidebar.title("게임 설정")
player_black   = st.sidebar.text_input("흑 플레이어 이름", "Black")
player_white   = st.sidebar.text_input("백 플레이어 이름", "White")
time_limit_min = st.sidebar.number_input("제한 시간 (분)", 1, 60, 20)
game_name      = st.sidebar.text_input("게임 이름", "OMOK by GPT")
if st.sidebar.button("게임 시작"):
    st.session_state.started = True
    st.session_state.board   = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    st.session_state.current = 1  # 1=흑, 2=백

# 세션 초기화
if 'started' not in st.session_state:
    st.session_state.started = False

st.title(f"{game_name} (Web Version)")

if st.session_state.started:
    # 현재 차례
    turn   = "흑" if st.session_state.current == 1 else "백"
    player = player_black if turn == "흑" else player_white
    st.markdown(f"**현재 차례: {turn} ({player})**")

    # 15×15 버튼 그리드
    for y in range(BOARD_SIZE):
        cols = st.columns(BOARD_SIZE, gap="small")
        for x, col in enumerate(cols):
            cell = st.session_state.board[y, x]
            # ● 흑돌, ○ 백돌, 빈칸은 공백
            if cell == 1:
                label = "●"
            elif cell == 2:
                label = "○"
            else:
                label = ""
            # 각 버튼 크기를 CSS로 고정
            with col:
                clicked = st.button(
                    label,
                    key=f"{y}-{x}",
                    help=f"({x}, {y})",
                    args=None,
                )
            if clicked:
                if st.session_state.board[y, x] == 0:
                    st.session_state.board[y, x] = st.session_state.current
                    st.session_state.current = 3 - st.session_state.current
                else:
                    st.warning("⚠️ 이미 돌이 놓여 있습니다.")

    # TODO: 5목 승리 검사, 타이머, 전적 저장 등

else:
    st.info("사이드바에서 설정 후 ‘게임 시작’ 버튼을 눌러주세요.")
