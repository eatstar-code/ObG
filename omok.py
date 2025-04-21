# omok.py

import streamlit as st
from PIL import Image, ImageDraw
import numpy as np
from datetime import datetime

# --- 설정 값 ---
BOARD_SIZE  = 15
CANVAS_PX   = 600
CELL_PX     = CANVAS_PX // (BOARD_SIZE - 1)
STAR_POINTS = [(3,3),(3,11),(7,7),(11,3),(11,11)]

# --- 사이드바: 게임 설정 ---
st.sidebar.title("게임 설정")
player_black   = st.sidebar.text_input("흑 플레이어 이름", "Black")
player_white   = st.sidebar.text_input("백 플레이어 이름", "White")
_               = st.sidebar.number_input("제한 시간 (분)", 1, 60, 20)
game_name      = st.sidebar.text_input("게임 이름", "OMOK by GPT")

if st.sidebar.button("게임 시작"):
    st.session_state.started = True
    st.session_state.board   = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    st.session_state.current = 1

if 'started' not in st.session_state:
    st.session_state.started = False

st.title(f"{game_name} (Web Version)")

def make_board_image(board):
    img  = Image.new("RGB", (CANVAS_PX, CANVAS_PX), "#F0D9B5")
    draw = ImageDraw.Draw(img)
    # 그리드
    for i in range(BOARD_SIZE):
        c = i * CELL_PX
        draw.line([(0, c), (CANVAS_PX, c)], fill="black")
        draw.line([(c, 0), (c, CANVAS_PX)], fill="black")
    # 화점
    for x,y in STAR_POINTS:
        cx, cy = x*CELL_PX, y*CELL_PX
        draw.ellipse([(cx-5, cy-5),(cx+5, cy+5)], fill="black")
    # 돌
    r = CELL_PX//2 - 2
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            if board[y,x] == 1:   # 흑돌
                cx, cy = x*CELL_PX, y*CELL_PX
                draw.ellipse([(cx-r,cy-r),(cx+r,cy+r)], fill="black")
            elif board[y,x] == 2: # 백돌
                cx, cy = x*CELL_PX, y*CELL_PX
                draw.ellipse([(cx-r,cy-r),(cx+r,cy+r)],
                             fill="white", outline="black", width=2)
    return img

if st.session_state.started:
    # 1) 바둑판 이미지
    board_img = make_board_image(st.session_state.board)
    st.image(board_img, use_column_width=False)

    # 2) 15×15 버튼 격자
    st.markdown("<div style='display:grid;grid-template-columns:repeat(15,1fr);"
                "width:600px;margin-top:-600px;pointer-events:none;'>"
                + "".join(
                    f"<button style='width:100%;height:{CELL_PX}px;"
                    "background:transparent;border:none;pointer-events:auto;' "
                    f"onclick='alert(\"{x},{y}\")'></button>"
                    for y in range(15) for x in range(15)
                )
                + "</div>", unsafe_allow_html=True)

    # 위 예제는 버튼 클릭 시 JS alert로 좌표를 확인할 수 있고,
    # Streamlit 에서 onclick 이벤트를 직접 받아오진 못하지만,
    # HTML 버튼 대신 아래와 같이 각 셀마다 st.button을 배치해도 됩니다.

    # 👉 순수 Streamlit 방식 (안정적입니다):
    """
    turn = "흑" if st.session_state.current==1 else "백"
    st.write(f"**현재 차례: {turn}**")

    for y in range(BOARD_SIZE):
        cols = st.columns(BOARD_SIZE, gap="small")
        for x, col in enumerate(cols):
            label = "●" if st.session_state.board[y,x]==1 else \
                    "○" if st.session_state.board[y,x]==2 else ""
            with col:
                if st.button(label, key=f"{y}-{x}"):
                    if st.session_state.board[y,x]==0:
                        st.session_state.board[y,x] = st.session_state.current
                        st.session_state.current = 3 - st.session_state.current
    """

else:
    st.info("사이드바에서 설정 후 ‘게임 시작’ 버튼을 눌러주세요.")
