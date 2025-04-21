import streamlit as st
import datetime

# --- 초기 설정 ---
st.title("OMOK by GPT v1.0")

# --- 세션 상태 초기화 ---
if 'board' not in st.session_state:
    st.session_state.board = [[0]*15 for _ in range(15)]
    st.session_state.current_player = 1
    st.session_state.move_history = []
    st.session_state.game_records = []
    st.session_state.game_info = None
    st.session_state.start_time = None
    st.session_state.time_limit = None
    st.session_state.game_over = False

# --- 게임 정보 입력 폼 ---
with st.form("info_form"):
    name = st.text_input("게임 이름", value=f"새 게임 {len(st.session_state.game_records)+1}")
    date = st.date_input("대국 일시")
    time = st.time_input("시작 시간")
    limit = st.number_input("제한 시간 (분)", min_value=1, value=20)
    black = st.text_input("흑 플레이어 이름", value="흑 유저")
    white = st.text_input("백 플레이어 이름", value="백 유저")
    submitted = st.form_submit_button("게임 시작")

if submitted and not st.session_state.game_info:
    # 게임 정보 기록 및 초기화
    st.session_state.game_info = {
        'name': name,
        'datetime': datetime.datetime.combine(date, time),
        'time_limit': int(limit)*60,
        'black': black,
        'white': white
    }
    st.session_state.start_time = datetime.datetime.now()
    st.session_state.time_limit = int(limit)*60
    st.experimental_rerun()

# --- 타이머 ---
if st.session_state.game_info:
    elapsed = (datetime.datetime.now() - st.session_state.start_time).seconds
    remaining = max(st.session_state.time_limit - elapsed, 0)
    mins, secs = divmod(remaining, 60)
    st.markdown(f"**흑 ({st.session_state.game_info['black']}) 남은 시간:** {mins:02d}:{secs:02d}   &nbsp;&nbsp;&nbsp; **백 ({st.session_state.game_info['white']}) 남은 시간:** {mins:02d}:{secs:02d}")
    if remaining == 0:
        st.error("시간 종료! 게임 오버.")
        st.session_state.game_over = True

# --- 오목판 그리기 ---
def render_board():
    cols = st.columns(15)
    for y in range(15):
        for x in range(15):
            with cols[x]:
                mark = "⚫" if st.session_state.board[y][x]==1 else "⚪" if st.session_state.board[y][x]==2 else ""
                if st.session_state.game_over:
                    st.write(mark)
                else:
                    if st.button(mark or "·", key=f"{x}-{y}"):
                        place_move(x, y)

def place_move(x, y):
    if st.session_state.board[y][x] == 0 and not st.session_state.game_over:
        st.session_state.board[y][x] = st.session_state.current_player
        st.session_state.move_history.append((st.session_state.current_player, x, y))
        if check_win(x, y):
            winner = st.session_state.game_info['black'] if st.session_state.current_player==1 else st.session_state.game_info['white']
            st.success(f"{winner} 승리!")
            st.session_state.game_over = True
        else:
            st.session_state.current_player = 2 if st.session_state.current_player==1 else 1

def check_win(x, y):
    b = st.session_state.board
    p = st.session_state.current_player
    dirs = [(1,0),(0,1),(1,1),(1,-1)]
    for dx, dy in dirs:
        cnt = 1
        nx, ny = x+dx, y+dy
        while 0<=nx<15 and 0<=ny<15 and b[ny][nx]==p:
            cnt+=1; nx+=dx; ny+=dy
        nx, ny = x-dx, y-dy
        while 0<=nx<15 and 0<=ny<15 and b[ny][nx]==p:
            cnt+=1; nx-=dx; ny-=dy
        if cnt>=5: return True
    return False

if st.session_state.game_info:
    render_board()
    # 하단 컨트롤
    c1, c2 = st.columns([1,1])
    if c1.button("초기화"):
        st.session_state.board = [[0]*15 for _ in range(15)]
        st.session_state.current_player = 1
        st.session_state.move_history.clear()
        st.session_state.game_over = False
        st.experimental_rerun()
    if c2.button("전적 저장"):
        st.session_state.game_records.append({
            **st.session_state.game_info,
            'moves': list(st.session_state.move_history)
        })
        st.success("전적이 저장되었습니다.")

if st.session_state.game_records:
    if st.checkbox("저장된 전적 보기"):
        for idx, rec in enumerate(st.session_state.game_records,1):
            st.write(f"{idx}. {rec['name']} | {rec['black']} vs {rec['white']} | {rec['datetime']} | {rec['time_limit']//60}분")
            # 간단한 움직임 확인
            st.write(rec['moves'])
