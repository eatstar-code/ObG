import os
import sqlite3
import tkinter as tk
from tkinter import messagebox, simpledialog
import datetime

# --- DB initialization ---
DB_PATH = os.path.join(os.path.dirname(__file__), 'omok.db')
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
conn.execute("""
    CREATE TABLE IF NOT EXISTS games (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        match_time TEXT NOT NULL,
        black_player TEXT NOT NULL,
        white_player TEXT NOT NULL,
        time_limit_min INTEGER NOT NULL
    );
""")
conn.execute("""
    CREATE TABLE IF NOT EXISTS moves (
        game_id INTEGER NOT NULL REFERENCES games(id) ON DELETE CASCADE,
        move_no INTEGER NOT NULL,
        player INTEGER NOT NULL,
        x INTEGER NOT NULL,
        y INTEGER NOT NULL,
        PRIMARY KEY (game_id, move_no)
    );
""")
conn.commit()

# --- Load existing records ---
def load_game_records():
    cur = conn.cursor()
    cur.execute(
        "SELECT id, name, match_time, black_player, white_player, time_limit_min FROM games"
    )
    records = []
    for gid, name, mt, black, white, tl in cur.fetchall():
        cur.execute(
            "SELECT player, x, y FROM moves WHERE game_id=? ORDER BY move_no", (gid,)
        )
        moves = cur.fetchall()
        records.append({
            'id': gid,
            'name': name,
            'match_time': mt,
            'black': black,
            'white': white,
            'time_limit_min': tl,
            'moves': moves
        })
    return records

# --- Settings ---
BOARD_SIZE = 15
CELL_SIZE = 30
MARGIN = 20
DEFAULT_TIME_LIMIT_MIN = 20
STAR_POINTS = [(3, 3), (3, 11), (7, 7), (11, 3), (11, 11)]

# --- Tkinter 메인 윈도우 초기화 ---
root = tk.Tk()
root.title("OMOK by GPT(ObG) v1.1")

# --- Global State ---
board = [[0] * BOARD_SIZE for _ in range(BOARD_SIZE)]
current_player = 1
black_time = 0
white_time = 0
move_history = []
game_records = load_game_records()

game_name = ""
match_time = ""
black_player = "흑 유저"
white_player = "백 유저"
time_limit = DEFAULT_TIME_LIMIT_MIN * 60
timer_id = None
game_counter = len(game_records) + 1

# --- Function definitions ---
def ask_game_info():
    global game_name, match_time, black_player, white_player
    global time_limit, black_time, white_time, move_history, game_counter
    dlg = tk.Toplevel(root)
    dlg.title("게임 정보 입력")
    labels = [
        "게임 이름",
        "대국 일시 (YYYY-MM-DD HH:MM)",
        "제한 시간(분)",
        "흑 플레이어",
        "백 플레이어"
    ]
    entries = {}
    for i, text in enumerate(labels):
        tk.Label(dlg, text=text).grid(row=i, column=0, padx=5, pady=5, sticky="e")
        e = tk.Entry(dlg)
        e.grid(row=i, column=1, padx=5, pady=5)
        entries[text] = e
    entries[labels[0]].insert(0, f"새 게임 {game_counter}")
    entries[labels[1]].insert(0, datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    entries[labels[2]].insert(0, str(DEFAULT_TIME_LIMIT_MIN))
    entries[labels[3]].insert(0, "흑 유저")
    entries[labels[4]].insert(0, "백 유저")
    def on_submit():
        global game_name, match_time, time_limit, black_player, white_player
        global black_time, white_time, move_history, game_counter
        vals = {lbl: entries[lbl].get().strip() for lbl in labels}
        game_name = vals[labels[0]] or f"새 게임 {game_counter}"
        match_time = vals[labels[1]] or datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        tl_str = vals[labels[2]]
        time_limit = int(tl_str) * 60 if tl_str.isdigit() else DEFAULT_TIME_LIMIT_MIN * 60
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

# Drawing functions
canvas = tk.Canvas(root, width=MARGIN*2+CELL_SIZE*(BOARD_SIZE-1), height=MARGIN*2+CELL_SIZE*(BOARD_SIZE-1), bg='#F0D9B5')

def draw_board():
    canvas.delete('all')
    for i in range(BOARD_SIZE):
        y = MARGIN + i * CELL_SIZE
        canvas.create_line(MARGIN, y, MARGIN + CELL_SIZE*(BOARD_SIZE-1), y)
        canvas.create_line(y, MARGIN, y, MARGIN + CELL_SIZE*(BOARD_SIZE-1))
    for sx, sy in STAR_POINTS:
        cx = MARGIN + sx*CELL_SIZE; cy = MARGIN + sy*CELL_SIZE; r=3
        canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill='black')

def in_bounds(x, y): return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE

def place_stone(x, y):
    if not in_bounds(x, y) or board[y][x] != 0: return False
    board[y][x] = current_player; move_history.append((current_player, x, y)); return True

def draw_stone(x, y):
    cx = MARGIN+x*CELL_SIZE; cy = MARGIN+y*CELL_SIZE; r=CELL_SIZE//2-2
    col = 'black' if board[y][x]==1 else 'white'
    canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill=col)

def check_win(x, y):
    for dx, dy in ((1,0),(0,1),(1,1),(1,-1)):
        cnt=1; nx,ny=x+dx,y+dy
        while in_bounds(nx,ny) and board[ny][nx]==current_player: cnt+=1; nx+=dx; ny+=dy
        nx,ny=x-dx,y-dy
        while in_bounds(nx,ny) and board[ny][nx]==current_player: cnt+=1; nx-=dx; ny-=dy
        if cnt>=5: return True
    return False

def switch_player():
    global current_player; current_player = 2 if current_player==1 else 1

def format_time(sec): return f"{sec//60:02d}:{sec%60:02d}"

def update_timer_labels():
    black_label.config(text=f"흑 ({black_player}) {format_time(black_time)}")
    white_label.config(text=f"백 ({white_player}) {format_time(white_time)}")

def tick():
    global black_time, white_time, timer_id
    if current_player==1:
        black_time-=1
        if black_time<=0: messagebox.showinfo("시간 종료",f"흑 ({black_player}) 시간 종료. 백 승리!"); end_game(); return
    else:
        white_time-=1
        if white_time<=0: messagebox.showinfo("시간 종료",f"백 ({white_player}) 시간 종료. 흑 승리!"); end_game(); return
    update_timer_labels(); timer_id=root.after(1000,tick)

def end_game():
    global timer_id; root.after_cancel(timer_id) if timer_id else None; canvas.unbind('<Button-1>')

def on_click(e):
    x = round((e.x - MARGIN) / CELL_SIZE)
    y = round((e.y - MARGIN) / CELL_SIZE)
    if place_stone(x, y):
        draw_stone(x, y)
        if check_win(x, y):
            winner = black_player if current_player == 1 else white_player
            messagebox.showinfo("승리", f"{winner} 승리!")
            end_game()
            return
        switch_player()

# --- Save current game ---
def save_current_game():
    cur=conn.cursor(); cur.execute("INSERT INTO games(name,match_time,black_player,white_player,time_limit_min) VALUES(?,?,?,?,?)",
                (game_name,match_time,black_player,white_player,time_limit//60))
    gid=cur.lastrowid
    for i,(pl,x,y) in enumerate(move_history,start=1): cur.execute("INSERT INTO moves(game_id,move_no,player,x,y) VALUES(?,?,?,?,?)",(gid,i,pl,x,y))
    conn.commit()
    game_records.append({'id':gid,'name':game_name,'match_time':match_time,'black':black_player,'white':white_player,'time_limit_min':time_limit//60,'moves':move_history.copy()})

def reset_game():
    global board,current_player,move_history,timer_id
    if move_history: save_current_game()
    ask_game_info()
    root.after_cancel(timer_id) if timer_id else None
    board=[[0]*BOARD_SIZE for _ in range(BOARD_SIZE)]; current_player=1; move_history.clear()
    draw_board(); canvas.bind('<Button-1>',on_click); update_timer_labels(); timer_id=root.after(1000,tick)

def show_record_list():
    win=tk.Toplevel(root); win.title("전적 목록")
    lb=tk.Listbox(win,width=50,height=10)
    for rec in game_records: lb.insert(tk.END,f"{rec['id']}. {rec['name']} ({rec['time_limit_min']}분) {rec['black']} vs {rec['white']} @ {rec['match_time']}")
    lb.pack(side='left',fill='y',padx=5,pady=5)
    frm=tk.Frame(win); frm.pack(side='right',padx=5)
    tk.Button(frm,text="전적 보기",command=lambda: show_record(lb.curselection()[0]) if lb.curselection() else None).pack()

# --- Show single record ---
def show_record(idx):
    rec=game_records[idx]; win=tk.Toplevel(root); win.title(f"전적: {rec['name']}")
    tk.Label(win,text=f"{rec['name']} | {rec['black']} vs {rec['white']} | {rec['match_time']} | {rec['time_limit_min']}분").pack(pady=5)
    size=MARGIN*2+CELL_SIZE*(BOARD_SIZE-1)
    rc=tk.Canvas(win,width=size,height=size,bg='#F0D9B5'); rc.pack(padx=10,pady=10)
    for i in range(BOARD_SIZE): rc.create_line(MARGIN+0,MARGIN+i*CELL_SIZE,MARGIN+(BOARD_SIZE-1)*CELL_SIZE,MARGIN+i*CELL_SIZE); rc.create_line(MARGIN+i*CELL_SIZE,MARGIN,MARGIN+i*CELL_SIZE,MARGIN+(BOARD_SIZE-1)*CELL_SIZE)
    for sx,sy in STAR_POINTS: rc.create_oval(MARGIN+sx*CELL_SIZE-3,MARGIN+sy*CELL_SIZE-3,MARGIN+sx*CELL_SIZE+3,MARGIN+sy*CELL_SIZE+3,fill='black')
    for i,(pl,x,y) in enumerate(rec['moves'],start=1):
        cx,cy=MARGIN+x*CELL_SIZE,MARGIN+y*CELL_SIZE; r=CELL_SIZE//2-2; col='black' if pl==1 else 'white'
        rc.create_oval(cx-r,cy-r,cx+r,cy+r,fill=col); rc.create_text(cx,cy,text=str(i),fill='white' if col=='black' else 'black',font=(None,12,'bold'))

# --- 업데이트 창 ---
def show_updates():
    win=tk.Toplevel(root); win.title("업데이트 내역")
    text=tk.Text(win,wrap='word',width=60,height=20); text.pack(padx=10,pady=10)
    updates="""
================================================
"OMOK by GPT(ObG)"
release date : 2025-04-23 (v1.1)
================================================
v1.1: 전적 데이터베이스 지원, 메뉴 변경
- 전적 데이트베이스를 구축하여 프로그램을 다시 시작해도 전적을 볼 수 있습니다.
- 기존 하단에 있던 초기화, 전적, 업데이트 내역 기능이 상단 좌측에 기능별로 모아집니다.
- 메뉴를 누르면 새 게임(초기화에서 변경), 전적이 나옵니다.
- 정보를 누르면 업데이트 내역과 제작자(신설)가 나옵니다.
================================================
상세한 업데이트 내역은 제작자의 깃허브를 참조하세요.
https://github.com/eatstar-code
"""
    text.insert('1.0',updates); text.config(state='disabled')

# --- 제작자 창 ---
def show_creator():
    win=tk.Toplevel(root); win.title("제작자")
    text=tk.Text(win,wrap='word',width=60,height=20); text.pack(padx=10,pady=10)
    creator="""
    ================================================
    제작자: EATSTAR (이트스타)
    Github: https://github.com/eatstar-code
    Blog : https://eatstar.tistory.com/
    ================================================
    ⓒ EATSTAR 2025
"""
    text.insert('1.0',creator); text.config(state='disabled')

# --- 메뉴바 설정 ---
menubar=tk.Menu(root)
menu_menu=tk.Menu(menubar,tearoff=0)
menu_menu.add_command(label="새 게임",command=reset_game)
menu_menu.add_command(label="전적",command=show_record_list)
menubar.add_cascade(label="메뉴",menu=menu_menu)
info_menu=tk.Menu(menubar,tearoff=0)
info_menu.add_command(label="업데이트 내역",command=show_updates)
info_menu.add_command(label="제작자",command=show_creator)
menubar.add_cascade(label="정보",menu=info_menu)
root.config(menu=menubar)

# --- UI layout & start ---
ask_game_info()
draw_board()
canvas.pack(pady=(0,5))
canvas.bind('<Button-1>', on_click)

# 타이머 표시 프레임
header_frame = tk.Frame(root, bg='#F0D9B5')
header_frame.pack(fill='x', pady=(10,0))

black_label = tk.Label(header_frame, text='', bg='#F0D9B5', font=(None,14))
black_label.pack(side='left', padx=10)
white_label = tk.Label(header_frame, text='', bg='#F0D9B5', font=(None,14))
white_label.pack(side='right', padx=10)

# 프로그램 이름을 타이머 아래 중앙에 표시
name_label = tk.Label(root, text='OMOK by GPT(ObG) v1.1', bg='#F0D9B5', font=(None,12,'italic'))
name_label.pack(fill='x')

# 구분선(빈 줄) - 배경만 표시
name_label = tk.Label(root, bg='#F0D9B5')
name_label.pack(fill='x')

update_timer_labels()
timer_id = root.after(1000, tick)

root.mainloop()
