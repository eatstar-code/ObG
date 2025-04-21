# omok.py

import streamlit as st
import numpy as np
from PIL import Image, ImageDraw
from datetime import datetime

# --- 설정 값 ---
BOARD_SIZE  = 15
CANVAS_PX   = 600
CELL_PX     = CANVAS_PX // (BOARD_SIZE - 1)
STAR_POINTS = [(3,3),(3,11),(7,7),(11,3),(11,11)]

# --- 세션 초기화 ---
if 'board' not in st.session_state:
    st.session_state.board   = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    st.session_state.current = 1  # 1=흑, 2=백

# --- 사이드바: 게임 설정 ---
st.sidebar.title("게임 설정")
player_black   = st.sidebar.text_input("흑 플레이어 이름", "Black")
player_white   = st.sidebar.text_input("백 플레이어 이름", "White")
_               = st.sidebar.number_input("제한 시간 (분)", 1, 60, 20)
game_name      = st.sidebar.text_input("게임 이름", "OMOK by GPT")

# --- 제목 ---
st.title(f"{game_name} (Web Version)")

# --- 바둑판 이미지 생성 함수 ---
def render_board_image(board):
    img  = Image.new("RGB", (CANVAS_PX, CANVAS_PX), "#F0D9B5")
    draw = ImageDraw.Draw(img)
    # 격자
    for i in range(BOARD_SIZE):
        c = i * CELL_PX
        draw.line([(0, c), (CANVAS_PX, c)], fill="black")
        draw.line([(c, 0), (c, CANVAS_PX)], fill="black")
    # 화점
    for x, y in STAR_POINTS:
        cx, cy = x*CELL_PX, y*CELL_PX
        draw.ellipse([(cx-5, cy-5), (cx+5, cy+5)], fill="black")
    # 돌
    r = CELL_PX//2 - 2
    for yy in range(BOARD_SIZE):
        for xx in range(BOARD_SIZE):
            if board[yy, xx] == 1:   # 흑돌
                draw.ellipse(
                    [(xx*CELL_PX - r, yy*CELL_PX - r),
                     (xx*CELL_PX + r, yy*CELL_PX + r)],
                    fill="black"
                )
            elif board[yy, xx] == 2: # 백돌
                draw.ellipse(
                    [(xx*CELL_PX - r, yy*CELL_PX - r),
                     (xx*CELL_PX + r, yy*CELL_PX + r)],
                    fill="white", outline="black", width=2
