# omok.py

import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
from streamlit_drawable_canvas import st_canvas
from datetime import datetime

# --- 설정 값 ---
BOARD_SIZE  = 15
CANVAS_SIZE = 600
CELL_PIXELS = CANVAS_SIZE // (BOARD_SIZE - 1)
STAR_POINTS = [(3,3), (3,11), (7,7), (11,3), (11,11)]

# --- 사이드바: 게임 설정 ---
st.sidebar.title("게임 설정")
player_black   = st.sidebar.text_input("흑 플레이어 이름", "Black")
player_white   = st.sidebar.text_input("백 플레이어 이름", "White")
_              = st.sidebar.number_input("제한 시간 (분)", 1, 60, 20)
game_name      = st.sidebar.text_input("게임 이름", "OMOK by GPT")

if st.sidebar.button("게임 시작"):
    st.session_state.started = True
    st.session_state.board   = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    st.session_state.current = 1

if 'started' not in st.session_state:
    st.session_state.started = False

st.title(f"{game_name} (Web Version)")

def render_board_image(board: np.ndarray) -> Image.Image:
    img  = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), "#F0D9B5")
    draw = ImageDraw.Draw(img)
    # 그리드
    for i in range(BOARD_SIZE):
        c = i * CELL_PIXELS
        draw.line([(0, c), (CANVAS_SIZE, c)], fill="black")
        draw.line([(c, 0), (c, CANVAS_SIZE)], fill="black")
    # 화점
    for x, y in STAR_POINTS:
        cx, cy, r = x*CELL_PIXELS, y*CELL_PIXELS, 5
        draw.ellipse([(cx-r, cy-r), (cx+r, cy+r)], fill="black")
    # 돌
    r_stone = CELL_PIXELS//2 - 2
    for yy in range(BOARD_SIZE):
        for xx in range(BOARD_SIZE):
            cx, cy = xx*CELL_PIXELS, yy*CELL_PIXELS
            if board[yy, xx] == 1:   # 흑돌
                draw.ellipse(
                    [(cx-r_stone, cy-r_stone), (cx+r_stone, cy+r_stone)],
                    fill="black"
                )
            elif board[yy, xx] == 2: # 백돌
                draw.ellipse(
                    [(cx-r_stone, cy-r_stone), (cx+r_stone, cy+r_stone)],
                    fill="white", outline="black", width=2
                )
    return img

if st.session_state.started:
    # 1) PIL 이미지 생성
    board_img = render_board_image(st.session_state.board)

    # 2) PIL 이미지(또는 numpy array) 직접 넘기기
    canvas_res = st_canvas(
        background_image=board_img,   # ← PIL.Image 객체를 직접 넣습니다
        width=CANVAS_SIZE,
        height=CANVAS_SIZE,
        stroke_width=0,
        drawing_mode="point",
        key="omok_canvas",
    )

    # 3) 클릭 처리 (이전과 동일)
    if canvas_res.json_data and canvas_res.json_data.get("objects"):
        last = canvas_res.json_data["objects"][-1]
        x_pix, y_pix = last["left"], last["top"]
        xi = int(round(x_pix / CELL_PIXELS))
        yi = int(round(y_pix / CELL_PIXELS))
        if 0 <= xi < BOARD_SIZE and 0 <= yi < BOARD_SIZE:
            if st.session_state.board[yi, xi] == 0:
                st.session_state.board[yi, xi] = st.session_state.current
                st.session_state.current = 3 - st.session_state.current
            else:
                st.warning("⚠️ 이미 돌이 놓여 있습니다.")

    # 4) 차례 표시
    turn   = "흑" if st.session_state.current == 1 else "백"
    name   = player_black if turn=="흑" else player_white
    st.markdown(f"**현재 차례: {turn} ({name})**")

else:
    st.info("사이드바에서 설정 후 '게임 시작' 버튼을 눌러주세요.")
