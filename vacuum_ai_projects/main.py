import tkinter as tk
from ui.app import VacuumApp

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Vacuum Cleaner AI")
    app = VacuumApp(root)
    root.mainloop()

def run_step(self):
    try:
        step_data = next(self.search_generator)
        self.update_log_panel(step_data["log"])
        if "solution" in step_data:
            if step_data["solution"] is not None:
                self.animate_solution(step_data["solution"].get_path())
            return
    except StopIteration:
        pass