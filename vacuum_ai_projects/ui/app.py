import tkinter as tk
from tkinter import ttk, scrolledtext
import random

from models.state import State
from algorithms.bfs_type1 import BFSType1
from algorithms.bfs_type2 import BFSType2
from algorithms.dfs_type1 import DFSType1
from algorithms.dfs_type2 import DFSType2
from algorithms.ids_type1 import IDSType1
from algorithms.ids_type2 import IDSType2
from algorithms.ucs import UCS

class VacuumApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1400x850")
        self.rows = 6
        self.cols = 6
        self.robot_pos = (0, 0)
        self.dirts = set()
        self.obstacles = set()
        self.search_generator = None
        self.is_auto_running = False
        self.is_animating = False
        # Biến lưu trữ ID của các tiến trình delay để có thể ngắt (Cancel)
        self.auto_job = None
        self.animation_job = None
        # --- Setup UI ---
        self.setup_ui()
        self.generate_random_map()

    def setup_ui(self):
        # 1. KHUNG BÊN TRÁI: Control Panel
        self.frame_left = tk.Frame(self.root, width=220, bg="#f0f0f0", padx=10, pady=10)
        self.frame_left.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(self.frame_left, text="CONTROLS", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)
        tk.Label(self.frame_left, text="Map Size (m x n):", bg="#f0f0f0").pack(anchor=tk.W, pady=(5, 0))
        size_frame = tk.Frame(self.frame_left, bg="#f0f0f0")
        size_frame.pack(fill=tk.X, pady=5)
        self.row_var = tk.IntVar(value=4)
        self.col_var = tk.IntVar(value=4)
        tk.Label(size_frame, text="Rows:", bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Spinbox(size_frame, from_=1, to=6, textvariable=self.row_var, width=3).pack(side=tk.LEFT, padx=5)
        tk.Label(size_frame, text="Cols:", bg="#f0f0f0").pack(side=tk.LEFT)
        tk.Spinbox(size_frame, from_=1, to=6, textvariable=self.col_var, width=3).pack(side=tk.LEFT)
        tk.Button(self.frame_left, text="Generate Map", command=self.generate_random_map, width=15).pack(pady=10)
        tk.Label(self.frame_left, text="Algorithms:", bg="#f0f0f0").pack(pady=(15, 0))
        self.algo_var = tk.StringVar(value="BFS_T1")
        tk.Radiobutton(self.frame_left, text="BFS Type 1", variable=self.algo_var, value="BFS_T1", bg="#f0f0f0").pack(
            anchor=tk.W)
        tk.Radiobutton(self.frame_left, text="BFS Type 2", variable=self.algo_var, value="BFS_T2", bg="#f0f0f0").pack(
            anchor=tk.W)
        tk.Radiobutton(self.frame_left, text="DFS Type 1", variable=self.algo_var, value="DFS_T1", bg="#f0f0f0").pack(
            anchor=tk.W)
        tk.Radiobutton(self.frame_left, text="DFS Type 2", variable=self.algo_var, value="DFS_T2", bg="#f0f0f0").pack(
            anchor=tk.W)
        tk.Radiobutton(self.frame_left, text="IDS Type 1", variable=self.algo_var, value="IDS_T1", bg="#f0f0f0").pack(anchor=tk.W)
        tk.Radiobutton(self.frame_left, text="IDS Type 2", variable=self.algo_var, value="IDS_T2", bg="#f0f0f0").pack(anchor=tk.W)
        tk.Radiobutton(self.frame_left, text="UCS (Uniform Cost)", variable=self.algo_var, value="UCS", bg="#f0f0f0").pack(anchor=tk.W)
        # KHU VỰC CÁC NÚT ĐIỀU KHIỂN
        tk.Button(self.frame_left, text="Start / Reset", command=self.start_search, width=15, bg="#4CAF50",
                  fg="white").pack(pady=(20, 5))
        tk.Button(self.frame_left, text="Next Step", command=self.next_step, width=15).pack(pady=5)
        tk.Label(self.frame_left, text="Log Auto Speed (ms):", bg="#f0f0f0").pack(anchor=tk.W, pady=(15, 0))
        self.speed_var = tk.IntVar(value=500)
        tk.Scale(self.frame_left, from_=50, to=2000, orient=tk.HORIZONTAL, variable=self.speed_var, bg="#f0f0f0").pack(
            fill=tk.X)
        self.btn_auto = tk.Button(self.frame_left, text="Auto Run", command=self.toggle_auto_run, width=15)
        self.btn_auto.pack(pady=5)
        # 2. KHUNG GIỮA: Visualize Môi trường
        self.frame_center = tk.Frame(self.root, padx=10, pady=10)
        self.frame_center.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        tk.Label(self.frame_center, text="ENVIRONMENT", font=("Arial", 14, "bold")).pack(pady=5)
        self.canvas_size = 500
        self.canvas = tk.Canvas(self.frame_center, width=self.canvas_size, height=self.canvas_size, bg="white",
                                relief=tk.SUNKEN, bd=2)
        self.canvas.pack(pady=10)
        # KHU VỰC SOLUTION PATH
        self.frame_bottom = tk.Frame(self.frame_center, pady=10)
        self.frame_bottom.pack(fill=tk.BOTH, expand=True)
        self.lbl_stats = tk.Label(self.frame_bottom, text="Status: Ready", font=("Arial", 11, "bold"), fg="blue")
        self.lbl_stats.pack(anchor=tk.W)
        tk.Label(self.frame_bottom, text="FINAL SOLUTION PATH:", font=("Arial", 10, "bold")).pack(anchor=tk.W,
                                                                                                  pady=(10, 2))
        self.solution_text = tk.Text(self.frame_bottom, height=4, width=60, state=tk.DISABLED, font=("Consolas", 10),
                                     bg="#fdfdfd", fg="#D84315", wrap=tk.WORD)
        self.solution_text.pack(fill=tk.X, pady=2)
        self.frame_right = tk.Frame(self.root, width=500, padx=10, pady=10)
        self.frame_right.pack(side=tk.RIGHT, fill=tk.BOTH)
        tk.Label(self.frame_right, text="ALGORITHM LOGS", font=("Arial", 14, "bold")).pack(pady=5)
        self.log_text = scrolledtext.ScrolledText(self.frame_right, width=80, height=35, state=tk.DISABLED,
                                                  font=("Consolas", 10), wrap=tk.NONE)
        x_scrollbar = tk.Scrollbar(self.frame_right, orient=tk.HORIZONTAL, command=self.log_text.xview)
        self.log_text.config(xscrollcommand=x_scrollbar.set)
        self.log_text.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        x_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.log_text.tag_configure("bold_pop", font=("Consolas", 10, "bold"), foreground="#D84315")
        self.log_text.tag_configure("bold_title", font=("Consolas", 10, "bold"), foreground="#1976D2")
        self.log_text.tag_configure("bold_goal", font=("Consolas", 10, "bold"), foreground="green")

    def append_log(self, text_msg, tag=None):
        is_at_bottom = self.log_text.yview()[1] >= 0.99
        self.log_text.config(state=tk.NORMAL)
        if tag:
            self.log_text.insert(tk.END, text_msg + "\n", tag)
        else:
            self.log_text.insert(tk.END, text_msg + "\n")
        if is_at_bottom:
            self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def format_trace_log(self, step_data):
        log_msg = step_data.get("log", "")
        # 1. Format lại Log action
        if "POP" in log_msg:
            self.append_log(f"\n[▼] {log_msg}", "bold_pop")
        elif "GENERATE" in log_msg:
            self.append_log(f"  [+] {log_msg}")
        elif "PUSH" in log_msg:
            self.append_log(f"    [→] {log_msg}")
        elif "GOAL" in log_msg.upper():
            self.append_log(f"\n[★] {log_msg}", "bold_goal")
        else:
            self.append_log(log_msg)
        # 2. Format Frontier
        if "frontier" in step_data:
            f_states = [
                f"({n.state.robot_pos[0]},{n.state.robot_pos[1]}|D:{len(n.state.dirts)})[{n.action if n.action else 'START'}]"
                for n in step_data["frontier"]]
            self.append_log(f"    [Frontier: {len(f_states)} nodes]", "bold_title")
            for i in range(0, len(f_states), 4):
                chunk = ", ".join(f_states[i:i + 4])
                self.append_log(f"       {chunk}")
        # 3. Format Reached (Explored)
        if "explored" in step_data:
            sorted_explored = sorted(step_data["explored"],
                                     key=lambda s: (len(s.dirts), s.robot_pos[0], s.robot_pos[1]), reverse=True)
            e_states = [f"({s.robot_pos[0]},{s.robot_pos[1]}|D:{len(s.dirts)})" for s in sorted_explored]
            self.append_log(f"    [Reached: {len(e_states)} states]", "bold_title")
            for i in range(0, len(e_states), 5):
                chunk = ", ".join(e_states[i:i + 5])
                self.append_log(f"       {chunk}")

    def clear_solution_box(self):
        self.solution_text.config(state=tk.NORMAL)
        self.solution_text.delete(1.0, tk.END)
        self.solution_text.config(state=tk.DISABLED)

    def stop_all(self):
        self.is_auto_running = False
        self.is_animating = False
        self.search_generator = None
        if self.auto_job is not None:
            self.root.after_cancel(self.auto_job)
            self.auto_job = None
        if self.animation_job is not None:
            self.root.after_cancel(self.animation_job)
            self.animation_job = None
        self.btn_auto.config(text="Auto Run", bg="SystemButtonFace", fg="black")
        self.append_log("\n[!!!] ĐÃ DỪNG TẤT CẢ TIẾN TRÌNH.")
        self.lbl_stats.config(text="Status: Stopped by User", fg="red")

    def generate_random_map(self):
        self.stop_all()
        self.obstacles.clear()
        self.dirts.clear()
        self.rows = self.row_var.get()
        self.cols = self.col_var.get()
        total_cells = self.rows * self.cols
        self.robot_pos = (random.randint(0, self.rows - 1), random.randint(0, self.cols - 1))
        max_dirts = max(1, min(4, total_cells // 3))
        max_obstacles = max(0, min(5, total_cells - max_dirts - 1))
        while len(self.dirts) < max_dirts:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (r, c) != self.robot_pos:
                self.dirts.add((r, c))
        while len(self.obstacles) < max_obstacles:
            r, c = random.randint(0, self.rows - 1), random.randint(0, self.cols - 1)
            if (r, c) != self.robot_pos and (r, c) not in self.dirts:
                self.obstacles.add((r, c))
        self.clear_solution_box()
        self.draw_grid()
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.lbl_stats.config(text=f"Map Generated: {self.rows}x{self.cols}. Ready.", fg="blue")

    def draw_grid(self, current_robot_pos=None, current_dirts=None):
        self.canvas.delete("all")
        cell_w = self.canvas_size / self.cols
        cell_h = self.canvas_size / self.rows
        r_pos = current_robot_pos if current_robot_pos else self.robot_pos
        d_set = current_dirts if current_dirts is not None else self.dirts
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * cell_w, r * cell_h
                x2, y2 = x1 + cell_w, y1 + cell_h
                # 1. TÔ MÀU NỀN VÀ VẬT CẢN
                color = "white"
                if (r, c) in self.obstacles:
                    color = "#424242"
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")
                # 2. VẼ ICON RÁC (DIRT)
                if (r, c) in d_set:
                    center_x = (x1 + x2) / 2
                    center_y = (y1 + y2) / 2
                    font_size = int(min(cell_w, cell_h) * 0.5)
                    self.canvas.create_text(center_x, center_y, text="🦠DIRTY",
                                  fill="#C0892A",
                                  font=("Consolas", 15, "bold"))
                if (r, c) == r_pos:
                    # Lấy tọa độ tâm gốc
                    cx = (x1 + x2) / 2
                    cy = (y1 + y2) / 2
                    radius = min(cell_w, cell_h) * 0.3
                    COLOR_AGENT = "#D8E2FF"
                    self.canvas.create_oval(cx - radius, cy - radius, cx + radius, cy + radius,
                                            fill=COLOR_AGENT, outline="#9B8BFF", width=2)
                    emoji_size = int(radius * 0.7)
                    self.canvas.create_text(cx, cy, text="🤖", font=("Segoe UI Emoji", emoji_size))


    def start_search(self):
        self.stop_all()  # Reset lại trạng thái
        algo_choice = self.algo_var.get()
        initial_state = State(self.robot_pos, self.dirts)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.append_log(f"--- STARTING {algo_choice} ---")
        self.clear_solution_box()
        self.lbl_stats.config(text="Searching...", fg="orange")
        self.draw_grid()
        if algo_choice == "BFS_T1":
            algo = BFSType1(self.rows, self.cols, self.obstacles)
        elif algo_choice == "BFS_T2":
            algo = BFSType2(self.rows, self.cols, self.obstacles)
        elif algo_choice == "DFS_T1":
            algo = DFSType1(self.rows, self.cols, self.obstacles)
        elif algo_choice == "DFS_T2":
            algo = DFSType2(self.rows, self.cols, self.obstacles)
        elif algo_choice == "IDS_T1":
            algo = IDSType1(self.rows, self.cols, self.obstacles)
        elif algo_choice == "IDS_T2":
            algo = IDSType2(self.rows, self.cols, self.obstacles)
        elif algo_choice == "UCS":
            algo = UCS(self.rows, self.cols, self.obstacles)
        self.search_generator = algo.search(initial_state)

    def toggle_auto_run(self):
        if not self.search_generator:
            self.append_log("Vui lòng bấm Start trước!")
            return
        self.is_auto_running = not self.is_auto_running
        if self.is_auto_running:
            self.btn_auto.config(text="Pause", bg="#FF9800", fg="white")
            self.append_log(">> RESUME Auto Run...")
            self.auto_step()
        else:
            self.btn_auto.config(text="Resume", bg="#2196F3", fg="white")
            self.append_log("|| PAUSE Auto Run.")

    def auto_step(self):
        if self.is_auto_running and self.search_generator:
            self.next_step()
            if self.is_auto_running and self.search_generator:
                self.auto_job = self.root.after(self.speed_var.get(), self.auto_step)

    def next_step(self):
        if not self.search_generator:
            if not self.is_animating:
                self.append_log("Vui lòng bấm Start trước!")
            return
        try:
            step_data = next(self.search_generator)
            self.format_trace_log(step_data)
            if "solution" in step_data:
                if step_data["solution"] is not None:
                    path = step_data["solution"].get_path()
                    actions = [node.action for node in path if node.action is not None]
                    action_str = " -> ".join(actions)
                    self.append_log(f"\n=> SUCCESS! Giải pháp tốn {len(path) - 1} bước.")
                    self.lbl_stats.config(text=f"Solved! Steps: {len(path) - 1}", fg="green")
                    self.solution_text.config(state=tk.NORMAL)
                    self.solution_text.delete(1.0, tk.END)
                    self.solution_text.insert(tk.END, action_str)
                    self.solution_text.config(state=tk.DISABLED)
                    self.append_log("\n>> Đang phát Animation Solution...")
                    self.is_animating = True
                    self.animate_solution(path, step_index=0)
                else:
                    self.append_log("\n=> FAILED! Không tìm thấy đường.")
                    self.lbl_stats.config(text="Failed: No solution", fg="red")
                self.is_auto_running = False
                self.btn_auto.config(text="Auto Run", bg="SystemButtonFace", fg="black")
                self.search_generator = None
        except StopIteration:
            self.search_generator = None

    def animate_solution(self, path_nodes, step_index):
        if not self.is_animating:
            return
        if step_index < len(path_nodes):
            node = path_nodes[step_index]
            self.draw_grid(current_robot_pos=node.state.robot_pos, current_dirts=node.state.dirts)
            self.animation_job = self.root.after(800, lambda: self.animate_solution(path_nodes, step_index + 1))
        else:
            self.append_log(">> Hoàn tất Animation.")
            self.is_animating = False