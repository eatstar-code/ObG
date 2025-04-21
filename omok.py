# omok.py

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime
from streamlit_drawable_canvas import st_canvas

# --- 설정 값 ---
BOARD_SIZE = 15
CANVAS_SIZE = 600         # 픽셀
CELL_PIXELS = CANVAS_SIZE // (BOARD_SIZE - 1)
STAR_POINTS = [(3,3), (3,11), (7,7), (11,3), (11,11)]

# --- 사이드바: 게임 설정 ---
st.sidebar.title("게임 설정")
player_black = st.sidebar.text_input("흑 플레이어 이름", value="Black")
player_white = st.sidebar.text_input("백 플레이어 이름", value="White")
time_limit_min = st.sidebar.number_input("제한 시간 (분)", min_value=1, max_value=60, value=20)
game_name = st.sidebar.text_input("게임 이름", value="OMOK by GPT")
if st.sidebar.button("게임 시작"):
    st.session_state.started = True
    st.session_state.board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    st.session_state.current = 1
    st.session_state.last_click = None

# 세션 초기값
if 'started' not in st.session_state:
    st.session_state.started = False

st.title(f"{game_name} (Web Version)")

def draw_matplotlib_board(board):
    """백업용: matplotlib으로 렌더링할 때 사용"""
    fig, ax = plt.subplots(figsize=(6,6))
    fig.patch.set_facecolor('white')
    ax.set_facecolor('#F0D9B5')

    # 격자
    for i in range(BOARD_SIZE):
        ax.plot([0, BOARD_SIZE-1], [i, i], 'k', zorder=1)
        ax.plot([i, i], [0, BOARD_SIZE-1], 'k', zorder=1)
    # 화점
    for x, y in STAR_POINTS:
        ax.scatter(x, y, s=50, c='k', zorder=1)
    # 돌 표시
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y,x] == 1:
                ax.scatter(x, y, s=200, c='k', zorder=3)
            elif board[y,x] == 2:
                ax.scatter(x, y, s=200,
                           facecolors='white', edgecolors='black',
                           linewidths=1.5, zorder=4)
    ax.set_xticks([]); ax.set_yticks([])
    ax.set_xlim(-1, BOARD_SIZE); ax.set_ylim(-1, BOARD_SIZE)
    ax.set_aspect('equal')
    return fig

if st.session_state.started:
    # 1) canvas 세팅
    canvas_result = st_canvas(
        fill_color="rgba(0,0,0,0)",  # 투명
        stroke_width=1,
        stroke_color="black",
        background_color="#F0D9B5",
        height=CANVAS_SIZE,
        width=CANVAS_SIZE,
        drawing_mode="transform",     # 클릭만 받고 그림은 안 그려짐
        key="omok_canvas",
    )

    # 격자와 화점은 background_color 위에 matplotlib으로 한 번 그리고,
    # streamlit의 이미지 오버레이 기능을 쓰지 못하므로, 
    # 백업용으로 matplotlib 그림도 사이드에 띄움 (선택)
    st.pyplot(draw_matplotlib_board(st.session_state.board))

    # 2) 클릭 좌표 처리
    if canvas_result.json_data:
        events = canvas_result.json_data["objects"]
        # 클릭 이벤트는 objects에 추가되므로, 마지막 one만 처리
        if events:
            last = events[-1]
            x_pix = last["left"]
            y_pix = last["top"]
            # 가장 가까운 교차점 좌표로 변환
            x_idx = int(round(x_pix / CELL_PIXELS))
            y_idx = int(round(y_pix / CELL_PIXELS))
            # 보드 내일 때만 처리
            if 0 <= x_idx < BOARD_SIZE and 0 <= y_idx < BOARD_SIZE:
                # 한 번만 처리하도록
                if st.session_state.last_click != (x_idx, y_idx):
                    st.session_state.last_click = (x_idx, y_idx)
                    if st.session_state.board[y_idx, x_idx] == 0:
                        st.session_state.board[y_idx, x_idx] = st.session_state.current
                        st.session_state.current = 3 - st.session_state.current
                    else:
                        st.warning("⚠️ 이미 돌이 있습니다.")

    # 3) 현재 차례 표시
    turn = "흑" if st.session_state.current == 1 else "백"
    player = player_black if turn == "흑" else player_white
    st.markdown(f"**현재 차례: {turn} ({player})**")

    # TODO: 승리 체크, 타이머, 전적 관리 등

else:
    st.info("사이드바에서 설정 후 '게임 시작'을 눌러주세요.")
