# omok.py

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from streamlit_plotly_events import plotly_events
from datetime import datetime

# --- 설정 값 ---
BOARD_SIZE = 15
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
    st.session_state.current = 1  # 1=흑, 2=백

if 'started' not in st.session_state:
    st.session_state.started = False

st.title(f"{game_name} (Web Version)")

def draw_board_figure(board):
    fig = go.Figure()

    # 1) 격자 그리기
    for i in range(BOARD_SIZE):
        fig.add_shape(type="line",
                      x0=0, y0=i, x1=BOARD_SIZE-1, y1=i,
                      line=dict(color="black", width=1))
        fig.add_shape(type="line",
                      x0=i, y0=0, x1=i, y1=BOARD_SIZE-1,
                      line=dict(color="black", width=1))

    # 2) 화점
    sx, sy = zip(*STAR_POINTS)
    fig.add_trace(go.Scatter(
        x=[x for x in sx], y=[y for y in sy],
        mode="markers", marker=dict(size=8, color="black"),
        hoverinfo="skip",
    ))

    # 3) 돌
    blacks = [(x,y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if board[y,x]==1]
    whites = [(x,y) for y in range(BOARD_SIZE) for x in range(BOARD_SIZE) if board[y,x]==2]

    if blacks:
        bx, by = zip(*blacks)
        fig.add_trace(go.Scatter(
            x=bx, y=by, mode="markers",
            marker=dict(size=24, color="black"),
            hoverinfo="skip"
        ))
    if whites:
        wx, wy = zip(*whites)
        fig.add_trace(go.Scatter(
            x=wx, y=wy, mode="markers",
            marker=dict(size=24, color="white", line=dict(color="black", width=2)),
            hoverinfo="skip"
        ))

    fig.update_xaxes(showticklabels=False, range=[-0.5, BOARD_SIZE-0.5])
    fig.update_yaxes(showticklabels=False, range=[BOARD_SIZE-0.5, -0.5])
    fig.update_layout(width=600, height=600, margin=dict(l=20,r=20,t=20,b=20))
    return fig

if st.session_state.started:
    # 1) Plotly 오목판 그리기
    fig = draw_board_figure(st.session_state.board)

    # 2) 클릭 이벤트 받아오기
    clicked = plotly_events(fig, click_event=True, key="omok_click")

    # 3) 클릭한 좌표 처리
    if clicked:
        x, y = clicked[0]["x"], clicked[0]["y"]
        xi, yi = int(round(x)), int(round(y))
        if 0 <= xi < BOARD_SIZE and 0 <= yi < BOARD_SIZE:
            if st.session_state.board[yi, xi] == 0:
                st.session_state.board[yi, xi] = st.session_state.current
                st.session_state.current = 3 - st.session_state.current
            else:
                st.warning("⚠️ 이미 돌이 놓여 있습니다.")

    # 4) 현재 차례 표시
    turn   = "흑" if st.session_state.current == 1 else "백"
    player = player_black if turn == "흑" else player_white
    st.markdown(f"**현재 차례: {turn} ({player})**")

    # 5) 판 갱신
    st.plotly_chart(fig, use_container_width=False)

else:
    st.info("사이드바에서 설정 후 ‘게임 시작’ 버튼을 눌러주세요.")
