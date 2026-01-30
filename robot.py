import serial
import tkinter as tk
import tictactoe as ttt

ssc32 = serial.Serial('COM4', 115200)
step_size = 10

defaults = {
    "base": 1500,
    "shoulder": 2150,
    "elbow": 2150,
    "wrist": 1300,
    "rotate": 1400,
    "grip": 1000
}

cube_default_position = {
    "base": 1105,
    "shoulder": 1460,  # using the higher stable value
    "elbow": 1330,
    "wrist": 700,
    "rotate": 1400,
    "grip": 1000
}

pickup_1_position = {
    "base": 1125,
    "shoulder": 1320,
    "elbow": 1400,
    "wrist": 660,
    "rotate": 1400,
    "grip": 1000
}

pickup_2_position = {
    "base": 1125,
    "shoulder": 1200,
    "elbow": 1230,
    "wrist": 670,
    "rotate": 1400,
    "grip": 1000
}

pickup_3_position = {
    "base": 1125,
    "shoulder": 1100,
    "elbow": 1060,
    "wrist": 680,
    "rotate": 1400,
    "grip": 1000
}


pickup_4_position = {
    "base": 1125,
    "shoulder": 980,
    "elbow": 890,
    "wrist": 690,
    "rotate": 1400,
    "grip": 1000
}

pickup_5_position = {
    "base": 1125,
    "shoulder": 940,
    "elbow": 800,
    "wrist": 890,
    "rotate": 1400,
    "grip": 1000
}

top_middle = {
    "base": 1495,
    "shoulder": 1310,
    "elbow": 1230,
    "wrist": 700,
    "rotate": 1400,
    "grip": 1000
}

middle_position = {
    "base": 1495,
    "shoulder": 1190,
    "elbow": 1230,
    "wrist": 700,
    "rotate": 1400,
    "grip": 1000
}

top_middle_position = {
    "base": 1495,
    "shoulder": 1430,
    "elbow": 1560,
    "wrist": 700,
    "rotate": 1400,
    "grip": 1000
}

top_left_position = {
    "base": 1720,
    "shoulder": 1360,
    "elbow": 1480,
    "wrist": 640,
    "rotate": 1400,
    "grip": 1000
}

top_right_position = {
    "base": 1250,
    "shoulder": 1360,
    "elbow": 1480,
    "wrist": 640,
    "rotate": 1400,
    "grip": 1000
}

middle_left_position = {
    "base": 1670,
    "shoulder": 1190,
    "elbow": 1230,
    "wrist": 700,
    "rotate": 1400,
    "grip": 1000
}

middle_middle_position = {
    "base": 1495,
    "shoulder": 1190,
    "elbow": 1230,
    "wrist": 700,
    "rotate": 1400,
    "grip": 1000
}

middle_right_position = {
    "base": 1290,
    "shoulder": 1190,
    "elbow": 1230,
    "wrist": 700,
    "rotate": 1400,
    "grip": 1000
}
# Bottom Left
# Base - 1625     
# Shoulder - 930
# Elbow - 750
# Wrist - 700
# Rotate - 1400
# Grip - 1000

bottom_left_position = {
    "base": 1625,
    "shoulder": 930,
    "elbow": 750,
    "wrist": 700,
    "rotate": 1400,
    "grip": 1000
}

bottom_middle_position = {
    "base": 1495,
    "shoulder": 870,
    "elbow": 580,
    "wrist": 510,
    "rotate": 1400,
    "grip": 1000
}
# needs work
bottom_right_position = {
    "base": 1340,
    "shoulder": 860,
    "elbow": 430,
    "wrist": 540,
    "rotate": 1400,
    "grip": 1000
}

grab = {
    "grip": 1410
}

release = {
    "grip": 1000
}

fields = {
    "base": "#0 P",
    "shoulder": "#1 P",
    "elbow": "#2 P",
    "wrist": "#3 P",
    "rotate": "#4 P",
    "grip": "#5 P"
}

current = {}

# Counter for tic-tac-toe games (selects pickup position)
tictactoe_game_counter = -1
pickup_positions = [pickup_1_position, pickup_2_position, pickup_3_position, pickup_4_position, pickup_5_position]

def increment(entry):
    value = int(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, str(value + step_size))
    display()

def decrement(entry):
    value = int(entry.get())
    entry.delete(0, tk.END)
    entry.insert(0, str(value - step_size))
    display()

def display():
    values = [f"{fields[label]}{entry.get()}" for label, entry in entries.items()]
    output_field.delete(0, tk.END)
    output_field.insert(0, " ".join(values) + " T1000")

def send():
    ssc32.write((output_field.get() + "\r").encode())

def home():
    for label, entry in entries.items():
        entry.delete(0, tk.END)
        entry.insert(0, str(defaults[label]))
    display()
    send()

def home_no_grip():
    for label, entry in entries.items():
        if label != "grip":
            entry.delete(0, tk.END)
            entry.insert(0, str(defaults[label]))
    display()

def apply_position(position, include_grip=False):
    for label, value in position.items():
        if value is None:
            continue
        if label == "grip" and not include_grip:
            continue
        entries[label].delete(0, tk.END)
        entries[label].insert(0, str(value))
        current[label] = value
    display()

def grab_grip():
    apply_position(grab, include_grip=True)

def release_grip():
    apply_position(release, include_grip=True)

def set_top_middle():
    # stage 1: set + send everything except base
    target_base = top_middle.get("base")

    stage1 = dict(top_middle)
    stage1["base"] = None  # don't change base yet
    apply_position(stage1)

    cmd1 = build_command(exclude_labels={"base"}, t=1000)
    send_command(cmd1)

    # stage 2: after 2 seconds, move base only
    def move_base_only():
        if target_base is None:
            return
        entries["base"].delete(0, tk.END)
        entries["base"].insert(0, str(target_base))
        display()

        cmd2 = f"{fields['base']}{target_base} T1000"
        send_command(cmd2)

    root.after(2000, move_base_only)

def build_command(exclude_labels=None, t=1000):
    if exclude_labels is None:
        exclude_labels = set()
    parts = []
    for label, entry in entries.items():
        if label in exclude_labels:
            continue
        parts.append(f"{fields[label]}{entry.get()}")
    return " ".join(parts) + f" T{t}"

def send_command(cmd: str):
    ssc32.write((cmd + "\r").encode())


def set_middle_position():
    apply_position(middle_position)

# Map tic-tac-toe board indices (0-8) to robot arm positions
# Board layout:
#  0 1 2
#  3 4 5
#  6 7 8
tictactoe_board_positions = {
    0: top_left_position,
    1: top_middle_position,
    2: top_right_position,
    3: middle_left_position,
    4: middle_middle_position,
    5: middle_right_position,
    6: bottom_left_position,
    7: bottom_middle_position,
    8: bottom_right_position,
}

def execute_ai_move_on_board(board_index):
    """
    Execute a physical robot move with the following sequence:
    1. Move to Default
    2. Move to Cube Default
    3. Move to Pickup position and grab
    4. Move back to Default
    5. Move to board position
    6. Release the block
    7. Move back to Default
    Each step is separated by a few second intervals for timing.
    """
    # Step 0: Move to Default position
    set_top_middle()
    cmd0 = build_command(t=1000)
    send_command(cmd0)
    
    # Step 1: After 2 seconds, move to Cube Default position
    def step1_cube_default():
        apply_position(cube_default_position)
        cmd1 = build_command(t=1000)
        send_command(cmd1)
        
        # Step 2: After 2 more seconds, move to Pickup position and grab
        def step2_pickup_grab():
            pickup_pos = pickup_positions[tictactoe_game_counter % len(pickup_positions)]
            print("Picking up from position:", tictactoe_game_counter % len(pickup_positions))
            apply_position(pickup_pos)
            cmd2 = build_command(t=1000)
            send_command(cmd2)
            
            # Step 3: After 2 more seconds, grab the block
            def step3_grab():
                grab_grip()
                cmd3 = build_command(t=500)
                send_command(cmd3)
                
                # Step 4: After 2 more seconds, move back to Default (using set_top_middle with internal timing)
                def step4_default():
                    set_top_middle()
                    
                    # Step 5: After 4.5 seconds (accounting for set_top_middle's internal 2s delay + movement), move to board position
                    def step5_board_position():
                        target_pos = tictactoe_board_positions[board_index]
                        apply_position(target_pos, include_grip=False)
                        cmd5 = build_command(t=1000)
                        send_command(cmd5)
                        
                        # Step 6: After 2 more seconds, release the block
                        def step6_release():
                            release_grip()
                            cmd6 = build_command(t=500)
                            send_command(cmd6)
                            
                            # Step 7: After 2 more seconds, move back to Default
                            def step7_final_default():
                                set_top_middle()
                            
                            root.after(2000, step7_final_default)
                        
                        root.after(2000, step6_release)
                    
                    root.after(4500, step5_board_position)
                
                root.after(2000, step4_default)
            
            root.after(2000, step3_grab)
        
        root.after(2000, step2_pickup_grab)
    
    root.after(2000, step1_cube_default)

def open_tictactoe():
    global tictactoe_game_counter
    tictactoe_game_counter = -1

    ttt_win = tk.Toplevel(root)
    ttt_win.title("Tic-Tac-Toe")
    ttt_win.resizable(False, False)

    # ensure the tic-tac-toe module exposes a shared board
    if not hasattr(ttt, "board") or not isinstance(ttt.board, list):
        try:
            ttt.board = [ttt.EMPTY] * 9
        except Exception:
            ttt.board = [None] * 9

    # reset shared board
    for i in range(9):
        ttt.board[i] = ttt.EMPTY

    buttons = []

    status = tk.Entry(ttt_win, width=25, justify="center")
    status.insert(0, "Your turn (X)")
    status.grid(row=0, column=0, columnspan=3, pady=10)

    def end_game(message):
        status.delete(0, tk.END)
        status.insert(0, message)
        for b in buttons:
            b.config(state=tk.DISABLED)

    def check_game_over():
        w = ttt.winner(ttt.board)
        if w == ttt.HUMAN:
            end_game("You win")
            return True
        if w == ttt.AI:
            end_game("AI wins")
            return True
        if ttt.is_full(ttt.board):
            end_game("Draw")
            return True
        return False

    def ai_move():
        global tictactoe_game_counter
        move = ttt.best_ai_move(ttt.board)
        if move is not None:
            ttt.board[move] = ttt.AI
            buttons[move].config(text=ttt.AI, state=tk.DISABLED)
            
            # Disable all buttons while robot moves
            for b in buttons:
                b.config(state=tk.DISABLED)
            status.delete(0, tk.END)
            status.insert(0, "AI moving...")
            
            # Increment counter for next pickup position
            tictactoe_game_counter += 1
            
            # Execute the robot movement and wait for it to complete
            def complete_ai_move():
                if not check_game_over():
                    status.delete(0, tk.END)
                    status.insert(0, "Your turn (X)")
                    # Re-enable empty cells for human
                    for i, b in enumerate(buttons):
                        if ttt.board[i] is ttt.EMPTY:
                            b.config(state=tk.NORMAL)
            
            # Total movement time: ~19 seconds (accounting for set_top_middle's internal timing)
            # Sequence: Defaults(2s) + CubeDefault(1s+2s) + Pickup(1s+2s) + Grab(0.5s+2s) + Default(4.5s) + Board(1s+2s) + Release(0.5s+2s) + Default(4.5s)
            execute_ai_move_on_board(move)
            ttt_win.after(19000, complete_ai_move)

        else:
            if not check_game_over():
                status.delete(0, tk.END)
                status.insert(0, "Your turn (X)")

    def human_move(index):
        if ttt.board[index] is not ttt.EMPTY:
            return

        ttt.board[index] = ttt.HUMAN
        buttons[index].config(text=ttt.HUMAN, state=tk.DISABLED)

        if check_game_over():
            return

        status.delete(0, tk.END)
        status.insert(0, "AI thinking...")
        ttt_win.after(200, ai_move)

    for r in range(3):
        for c in range(3):
            idx = r * 3 + c
            btn = tk.Button(
                ttt_win,
                text=" ",
                width=6,
                height=3,
                font=("Arial", 20),
                command=lambda i=idx: human_move(i)
            )
            btn.grid(row=r + 1, column=c, padx=5, pady=5)
            buttons.append(btn)


root = tk.Tk()
root.title("Numeric Input GUI")

entries = {}

tk.Button(root, text="Play Tic-Tac-Toe", command=open_tictactoe).pack(pady=10)
tk.Button(root, text="Home", command=home).pack(pady=5)
tk.Button(root, text="Home (No Grip)", command=home_no_grip).pack(pady=5)
tk.Button(root, text="Default", command=set_top_middle).pack(pady=5)
tk.Button(root, text="Release", command=release_grip).pack(pady=5)
tk.Button(root, text="Grab", command=grab_grip).pack(pady=5)
tk.Button(root, text="Cube Default", command=lambda: apply_position(cube_default_position)).pack(pady=5)
tk.Button(root, text="Pickup 1", command=lambda: apply_position(pickup_1_position)).pack(pady=5)
tk.Button(root, text="Pickup 2", command=lambda: apply_position(pickup_2_position)).pack(pady=5)
tk.Button(root, text="Pickup 3", command=lambda: apply_position(pickup_3_position)).pack(pady=5)
tk.Button(root, text="Pickup 4", command=lambda: apply_position(pickup_4_position)).pack(pady=5)
tk.Button(root, text="Pickup 5", command=lambda: apply_position(pickup_5_position)).pack(pady=5)



board = tk.Frame(root)
board.pack(pady=10)

positions = [
    [top_left_position, top_middle_position, top_right_position],
    [middle_left_position, middle_middle_position, middle_right_position],
    [bottom_left_position, bottom_middle_position, bottom_right_position]
]

labels = [
    ["TL", "TM", "TR"],
    ["ML", "MM", "MR"],
    ["BL", "BM", "BR"]
]

for r in range(3):
    for c in range(3):
        tk.Button(
            board,
            text=labels[r][c],
            width=6,
            command=lambda p=positions[r][c]: apply_position(p)  # grip ignored here
        ).grid(row=r, column=c, padx=5, pady=5)

for label, default_value in defaults.items():
    frame = tk.Frame(root)
    frame.pack(pady=2, anchor="w")
    tk.Label(frame, text=label.capitalize() + ":", width=10, anchor="w").pack(side=tk.LEFT, padx=5)
    tk.Button(frame, text="-", width=3, command=lambda l=label: decrement(entries[l])).pack(side=tk.LEFT)
    entry = tk.Entry(frame, width=5, justify=tk.CENTER)
    entry.insert(0, str(default_value))
    entry.pack(side=tk.LEFT, padx=5)
    entries[label] = entry
    tk.Button(frame, text="+", width=3, command=lambda l=label: increment(entries[l])).pack(side=tk.LEFT)

tk.Button(root, text="Send to Arm", command=send).pack(pady=10)

output_field = tk.Entry(root, width=60, justify=tk.LEFT)
output_field.pack(pady=10)

display()
root.mainloop()


# Top Left              
# Base - 1720     
# Shoulder - 1360
# Elbow - 1480
# Wrist - 640
# Rotate - 1400
# Grip - 1000

# Top Right
# Base - 1250     
# Shoulder - 1360
# Elbow - 1480
# Wrist - 640
# Rotate - 1400
# Grip - 1000

# Middle Left
# Base - 1670     
# Shoulder - 1190
# Elbow - 1230
# Wrist - 700
# Rotate - 1400
# Grip - 1000

# Middle Right
# Base - 1290     
# Shoulder - 1190
# Elbow - 1230
# Wrist - 700
# Rotate - 1400
# Grip - 1000

# Default 2 (for pickup)
# Base - 1105     
# Shoulder - 1390, 1460
# Elbow - 1230, 1400
# Wrist - 700
# Rotate - 1400
# Grip - 1000


# Pickup Position 1
# Base - 1105     
# Shoulder - 1320
# Elbow - 1400
# Wrist - 700
# Rotate - 1400
# Grip - 1000