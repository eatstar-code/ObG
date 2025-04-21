import streamlit as st
import matplotlib.pyplot as plt

BOARD_SIZE = 15
CELL_SIZE = 1

def draw_board():
    fig, ax = plt.subplots(figsize=(6,6))
    for i in range(BOARD_SIZE):
        ax.plot([0, BOARD_SIZE-1], [i, i], color='black')  # 가로줄
        ax.plot([i, i], [0, BOARD_SIZE-1], color='black')  # 세로줄

    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_xlim(-1, BOARD_SIZE)
    ax.set_ylim(-1, BOARD_SIZE)
    ax.set_aspect('equal')
    st.pyplot(fig)

st.title("OMOK by GPT (Web Version)")
draw_board()
