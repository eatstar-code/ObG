import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime

# --- 설정 값 ---
BOARD_SIZE = 15   # 바둑판 크기 (15×15)
CELL_SIZE = 30    # 한 칸 픽셀 크기
MARGIN = 20       # 여백
DEFAULT_TIME_LIMIT_MIN = 20  # 기본 제한 시간 (분)
STAR_POINTS = [(3,3),(3,11),(7,7),(11,3),(11,11)]  # 화점 좌표

# --- 전역 상태 및 메인 윈도우 초기화 ---
root = tk.Tk()
root.title("OMOK by GPT(ObG) v1.0")

board = [[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]  # 0: 빈,1:흑,2:백
current_player = 1
black_time = 0
white_time = 0
move_history = []         # 현재 게임 착수 기록

game_records = []         # 저장된 게임 전적 리스트
# 메타데이터 초기값
game_name = ""
match_time = ""
black_player = "흑 유저"
white_player = "백 유저"
time_limit = DEFAULT_TIME_LIMIT_MIN * 60  # 초 단위

timer_id = None
game_counter = 1

# --- 게임 정보 입력 (단일 폼 Toplevel) ---
def ask_game_info():
    global game_name, match_time, black_player, white_player, time_limit, black_time, white_time, move_history, game_counter
    dlg = tk.Toplevel(root)
    dlg.title("게임 정보 입력")
    labels = ["게임 이름", "대국 일시 (YYYY-MM-DD HH:MM)", "제한 시간(분)", "흑 플레이어", "백 플레이어"]
    entries = {}
    for i, text in enumerate(labels):
        tk.Label(dlg, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        e = tk.Entry(dlg)
        e.grid(row=i, column=1, padx=5, pady=5)
        entries[text] = e
    # 기본값 설정
    entries[labels[0]].insert(0, f"새 게임 {game_counter}")
    entries[labels[1]].insert(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    entries[labels[2]].insert(0, str(DEFAULT_TIME_LIMIT_MIN))
    entries[labels[3]].insert(0, "흑 유저")
    entries[labels[4]].insert(0, "백 유저")

    def on_submit():
        global game_name, match_time, time_limit, black_player, white_player, black_time, white_time, move_history, game_counter
        vals = {lbl: entries[lbl].get().strip() for lbl in labels}
        game_name = vals[labels[0]] or f"새 게임 {game_counter}"
        match_time = vals[labels[1]] or "불명"
        tl_str = vals[labels[2]]
        time_limit = int(tl_str)*60 if tl_str.isdigit() else DEFAULT_TIME_LIMIT_MIN*60
        black_player = vals[labels[3]] or "흑 유저"
        white_player = vals[labels[4]] or "백 유저"
        black_time = time_limit
        white_time = time_limit
        move_history.clear()
        game_counter += 1
        dlg.destroy()

    tk.Button(dlg, text="확인", command=on_submit).grid(row=len(labels), column=0, columnspan=2, pady=10)
    dlg.transient(root)
    dlg.grab_set()
    root.wait_window(dlg)

# --- 바둑판 그리기 ---
canvas = tk.Canvas(root, width=MARGIN*2+CELL_SIZE*(BOARD_SIZE-1), height=MARGIN*2+CELL_SIZE*(BOARD_SIZE-1), bg='#F0D9B5')
# (캔버스 배치는 메뉴 및 업데이트 영역 아래에서 수행)

def draw_board():
    canvas.delete('all')
    for i in range(BOARD_SIZE):
        y = MARGIN + i*CELL_SIZE
        canvas.create_line(MARGIN, y, MARGIN+CELL_SIZE*(BOARD_SIZE-1), y)
        canvas.create_line(y, MARGIN, y, MARGIN+CELL_SIZE*(BOARD_SIZE-1))
    for (sx, sy) in STAR_POINTS:
        cx = MARGIN+sx*CELL_SIZE; cy = MARGIN+sy*CELL_SIZE; r=3
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='black')

# --- 착수 처리 및 승리 검사 ---
def in_bounds(x, y): return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def place_stone(x, y):
    if board[y][x] != 0: return False
    board[y][x] = current_player
    move_history.append((current_player, x, y))
    return True

def draw_stone(x, y):
    cx = MARGIN + x*CELL_SIZE; cy = MARGIN + y*CELL_SIZE; r = CELL_SIZE//2 - 2
    color = 'black' if board[y][x] == 1 else 'white'
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=color)

def check_win(x, y):
    for dx, dy in ((1,0),(0,1),(1,1),(1,-1)):
        cnt = 1; nx, ny = x+dx, y+dy
        while in_bounds(nx, ny) and board[ny][nx] == current_player:
            cnt+=1; nx+=dx; ny+=dy
        nx, ny = x-dx, y-dy
        while in_bounds(nx, ny) and board[ny][nx] == current_player:
            cnt+=1; nx-=dx; ny-=dy
        if cnt>=5: return True
    return False

def switch_player():
    global current_player
    current_player = 2 if current_player == 1 else 1

# --- 타이머 함수 ---
def format_time(sec): return f"{sec//60:02d}:{sec%60:02d}"

def update_timer_labels():
    black_label.config(text=f"흑 ({black_player}) {format_time(black_time)}")
    white_label.config(text=f"백 ({white_player}) {format_time(white_time)}")

def tick():
    global black_time, white_time, timer_id
    if current_player == 1:
        black_time -= 1
        if black_time == 0:
            messagebox.showinfo("시간 종료", f"흑 ({black_player}) 시간 종료. 백 ({white_player}) 승리!")
            end_game(); return
    else:
        white_time -= 1
        if white_time == 0:
            messagebox.showinfo("시간 종료", f"백 ({white_player}) 시간 종료. 흑 ({black_player}) 승리!")
            end_game(); return
    update_timer_labels()
    timer_id = root.after(1000, tick)

# --- 게임 종료 ---
def end_game():
    global timer_id
    if timer_id:
        root.after_cancel(timer_id)
    canvas.unbind('<Button-1>')

# --- 클릭 이벤트 ---
def on_click(e):
    x = round((e.x - MARGIN)/CELL_SIZE)
    y = round((e.y - MARGIN)/CELL_SIZE)
    if in_bounds(x, y) and place_stone(x, y):
        draw_stone(x, y)
        if check_win(x, y):
            winner = black_player if current_player == 1 else white_player
            messagebox.showinfo("승리", f"{winner} 승리!")
            end_game(); return
        switch_player()
canvas.bind('<Button-1>', on_click)

# --- 새 게임 초기화 ---
def reset_game():
    global board, current_player, move_history, timer_id
    if move_history:
        game_records.append({
            'name': game_name, 'match_time': match_time,
            'black': black_player, 'white': white_player,
            'time_limit_min': time_limit//60, 'moves': move_history.copy()
        })
    ask_game_info()
    if timer_id:
        root.after_cancel(timer_id)
    for y in range(BOARD_SIZE):
        for x in range(BOARD_SIZE): board[y][x] = 0
    current_player = 1
    move_history.clear()
    draw_board()
    canvas.bind('<Button-1>', on_click)
    update_timer_labels()
    timer_id = root.after(1000, tick)

# --- 전적 목록 보기 ---
def show_record_list():
    win = tk.Toplevel(root); win.title("전적 목록")
    lb = tk.Listbox(win, width=50, height=10)
    for i, rec in enumerate(game_records, start=1):
        lb.insert(tk.END, f"{i}. {rec['name']} ({rec['time_limit_min']}분) {rec['black']} vs {rec['white']} @ {rec['match_time']}")
    lb.pack(side=tk.LEFT, fill=tk.Y, padx=5, pady=5)
    frm = tk.Frame(win); frm.pack(side=tk.RIGHT, padx=5)
    tk.Button(frm, text="전적 보기", command=lambda: show_record(lb.curselection()[0]) if lb.curselection() else None).pack()

def show_record(idx):
    rec = game_records[idx]
    win = tk.Toplevel(root); win.title(f"전적: {rec['name']}")
    tk.Label(win, text=f"{rec['name']} | {rec['black']} vs {rec['white']} | {rec['match_time']} | {rec['time_limit_min']}분").pack(pady=5)
    size = MARGIN*2 + CELL_SIZE*(BOARD_SIZE-1)
    rc = tk.Canvas(win, width=size, height=size, bg='#F0D9B5'); rc.pack(padx=10, pady=10)
    for i in range(BOARD_SIZE):
        y = MARGIN + i*CELL_SIZE
        rc.create_line(MARGIN, y, MARGIN + CELL_SIZE*(BOARD_SIZE-1), y)
        rc.create_line(y, MARGIN, y, MARGIN + CELL_SIZE*(BOARD_SIZE-1))
    for sx, sy in STAR_POINTS:
        rc.create_oval(MARGIN+sx*CELL_SIZE-3, MARGIN+sy*CELL_SIZE-3, MARGIN+sx*CELL_SIZE+3, MARGIN+sy*CELL_SIZE+3, fill='black')
    for i,(pl,x,y) in enumerate(rec['moves'], start=1):
        cx = MARGIN + x*CELL_SIZE; cy = MARGIN + y*CELL_SIZE; r = CELL_SIZE//2 - 2
        col = 'black' if pl == 1 else 'white'; rc.create_oval(cx-r, cy-r, cx+r, cy+r, fill=col)
        rc.create_text(cx, cy, text=str(i), fill='white' if col=='black' else 'black', font=(None,12,'bold'))

# --- 업데이트 안내 창 ---
def show_updates():
    win = tk.Toplevel(root)
    win.title("업데이트 안내")
    text = tk.Text(win, wrap='word', width=60, height=15)
    text.pack(padx=10, pady=10)
    updates = """
================================================
"OMOK by GPT(ObG)"
release date : 2025-04-20 (v1.0)
made by EATSTAR (https://github.com/eatstar-code)
================================================
v1.0 (2시간 반 소요)
기본적인 오목 시스템을 GUI로 구현
게임 시작시 게임 이름, 유저 이름, 게임시간, 시각을 입력.
시간초과시 기권패, 5줄 완성시 승리하는 규칙
게임을 마치면 전적을 볼 수 있음

- 앞으로의 목표
3.3이나 6목같은 수를 막는 코드가 없음
AI가 두는 기능은 없음
전적을 장기적으로 저장하는 DB 시스템이 없음

모두 GPT를 활용한 코드로, 본인은 질문과 디버그만 함.
유료버전인 ChatGPT o4 mini-high(코드 특화)로 작성함.
Visual Studio를 사용하여 작성함.
================================================
"""
    text.insert('1.0', updates)
    text.config(state='disabled')

# --- 시작 ---
ask_game_info()

# 오목판 그리기 및 표시
draw_board()
canvas.pack(pady=(0,5))
canvas.bind('<Button-1>', on_click)

# --- 메뉴 (바둑판 아래) ---
# 타이머 영역
timer_frame = tk.Frame(root, bg='#F0D9B5')
timer_frame.pack(fill='x', pady=(10,0))
black_label = tk.Label(timer_frame, text=f"흑 ({black_player}) {format_time(black_time)}", bg='#F0D9B5', font=(None,14))
black_label.pack(side='left', padx=10)
white_label = tk.Label(timer_frame, text=f"백 ({white_player}) {format_time(white_time)}", bg='#F0D9B5', font=(None,14))
white_label.pack(side='right', padx=10)

# 타이머 시작 및 업데이트
black_time = white_time = time_limit
update_timer_labels()
timer_id = root.after(1000, tick)

# 컨트롤 버튼 영역
btn_frame = tk.Frame(root, bg='#F0D9B5')
btn_frame.pack(fill='x')
tk.Button(btn_frame, text="초기화", command=reset_game).pack(side='left', padx=10)
tk.Label(btn_frame, text="OMOK by GPT(ObG) v1.0", bg='#F0D9B5', font=(None,12,'italic')).pack(side='left', expand=True)
tk.Button(btn_frame, text="전적", command=show_record_list).pack(side='right', padx=10)

# 업데이트 내역 영역
update_frame = tk.Frame(root, bg='#F0D9B5')
update_frame.pack(fill='x')
tk.Button(update_frame, text="업데이트 내역", command=show_updates).pack(side='right', padx=10, pady=5)

root.mainloop()
