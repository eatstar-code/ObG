# omok.py

import streamlit as st
import numpy as np
import io, base64
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
_              = st.sidebar.number_input("제한 시간 (분)", 1, 60, 20)  # 아직 사용 안 함
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
    # 격자
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
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE):
            cx, cy = x*CELL_PIXELS, y*CELL_PIXELS
            if board[y, x] == 1:   # 흑돌
                draw.ellipse([(cx-r_stone, cy-r_stone), (cx+r_stone, cy+r_stone)], fill="black")
            elif board[y, x] == 2: # 백돌
                draw.ellipse(
                    [(cx-r_stone, cy-r_stone), (cx+r_stone, cy+r_stone)],
                    fill="white", outline="black", width=2
                )
    return img

if st.session_state.started:
    # 1) PIL 이미지 생성
    board_img = render_board_image(st.session_state.board)

    # 2) base64로 인코딩 → data URL 생성
    buf = io.BytesIO()
    board_img.save(buf, format="PNG")
    b64 = base64.b64encode(buf.getvalue()).decode("utf-8")
    data_url = f"data:image/png;base64,{b64}"

    # 3) background_image에 URL로 넘겨 캔버스 생성
    canvas_res = st_canvas(
        background_image=data_url,
        width=CANVAS_SIZE, height=CANVAS_SIZE,
        stroke_width=0,
        drawing_mode="point",
        key="omok_canvas",
    )

    # 4) 클릭 이벤트 처리
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

    # 5) 현재 차례 표시
    turn   = "흑" if st.session_state.current == 1 else "백"
    player = player_black if turn == "흑" else player_white
    st.markdown(f"**현재 차례: {turn} ({player})**")

else:
    st.info("사이드바에서 설정 후 ‘게임 시작’ 버튼을 눌러주세요.")
