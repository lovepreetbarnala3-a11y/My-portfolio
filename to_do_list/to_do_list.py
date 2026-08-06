import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, simpledialog, ttk

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "tasks.json")


class TodoApp:

    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List")
        self.root.geometry("480x560")
        self.root.minsize(400, 400)
        self.root.configure(bg="#f4f6f8")

        self.tasks = []  # each task: {"text": str, "done": bool, "created": str}

        self._build_ui()
        self.load_tasks()
        self.refresh_list()

    # ---------- UI construction ----------
    def _build_ui(self):
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

        style.configure("TButton", font=("Segoe UI", 10), padding=6)
        style.configure("TLabel", background="#f4f6f8", font=("Segoe UI", 11))

        # Title
        title = tk.Label(
            self.root,
            text="📝 My To-Do List",
            font=("Segoe UI", 18, "bold"),
            bg="#f4f6f8",
            fg="#2c3e50",
        )
        title.pack(pady=(15, 5))

        # Entry frame
        entry_frame = tk.Frame(self.root, bg="#f4f6f8")
        entry_frame.pack(fill="x", padx=15, pady=10)

        self.entry = ttk.Entry(entry_frame, font=("Segoe UI", 11))
        self.entry.pack(side="left", fill="x", expand=True, ipady=5)
        self.entry.bind("<Return>", lambda e: self.add_task())

        add_btn = ttk.Button(entry_frame, text="Add", command=self.add_task)
        add_btn.pack(side="left", padx=(8, 0))

        # Task list frame with scrollbar
        list_frame = tk.Frame(self.root, bg="#f4f6f8")
        list_frame.pack(fill="both", expand=True, padx=15, pady=5)

        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side="right", fill="y")

        self.listbox = tk.Listbox(
            list_frame,
            font=("Segoe UI", 11),
            activestyle="none",
            selectbackground="#a9d6e5",
            yscrollcommand=scrollbar.set,
            highlightthickness=0,
            bd=1,
            relief="solid",
        )
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<Double-Button-1>", lambda e: self.toggle_done())
        scrollbar.config(command=self.listbox.yview)

        # Buttons frame
        btn_frame = tk.Frame(self.root, bg="#f4f6f8")
        btn_frame.pack(fill="x", padx=15, pady=10)

        ttk.Button(
            btn_frame, text="✔ Mark Done", command=self.toggle_done
        ).pack(side="left", expand=True, fill="x", padx=3)
        ttk.Button(btn_frame, text="✎ Edit", command=self.edit_task).pack(
            side="left", expand=True, fill="x", padx=3
        )
        ttk.Button(btn_frame, text="🗑 Delete", command=self.delete_task).pack(
            side="left", expand=True, fill="x", padx=3
        )
        ttk.Button(
            btn_frame, text="Clear Completed", command=self.clear_completed
        ).pack(side="left", expand=True, fill="x", padx=3)

        # Status bar
        self.status_var = tk.StringVar()
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            bg="#e8ebee",
            fg="#555",
            anchor="w",
            font=("Segoe UI", 9),
            padx=10,
            pady=4,
        )
        status_bar.pack(fill="x", side="bottom")

    # ---------- Data operations ----------
    def load_tasks(self):
        """Load tasks.json safely, validate items, and recover from malformed files."""
        self.tasks = []
        if not os.path.exists(DATA_FILE):
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            messagebox.showwarning(
                "Load Error",
                f"Could not parse {os.path.basename(DATA_FILE)}. Starting with an empty task list.\n\nError: {e}",
            )
            # Optionally rename the corrupt file so user can inspect it:
            # os.rename(DATA_FILE, DATA_FILE + ".corrupt")
            self.tasks = []
            return
        except IOError as e:
            messagebox.showwarning(
                "Load Error",
                f"Could not read {os.path.basename(DATA_FILE)}. Starting with an empty task list.\n\nError: {e}",
            )
            self.tasks = []
            return

        # Validate and sanitize loaded data
        if not isinstance(data, list):
            # file might contain a dict or other structure; ignore it
            messagebox.showwarning(
                "Load Error",
                f"{os.path.basename(DATA_FILE)} has unexpected content. Expected a list of tasks — starting empty."
            )
            self.tasks = []
            return

        safe_tasks = []
        for item in data:
            if not isinstance(item, dict):
                continue
            text = item.get("text")
            if text is None:
                # skip items without text
                continue
            text = str(text).strip()
            if not text:
                continue
            done = bool(item.get("done", False))
            created = item.get("created") or datetime.now().strftime("%Y-%m-%d %H:%M")
            safe_tasks.append({"text": text, "done": done, "created": created})
        self.tasks = safe_tasks

    def save_tasks(self):
        """Write tasks out. Use a safe write method to reduce chance of truncation/corruption."""
        try:
            # Simple atomic-ish write: write to temp file then replace.
            tmp_path = DATA_FILE + ".tmp"
            with open(tmp_path, "w", encoding="utf-8") as f:
                json.dump(self.tasks, f, indent=2, ensure_ascii=False)
            # Replace original (atomic on many OSes)
            os.replace(tmp_path, DATA_FILE)
        except Exception as e:
            messagebox.showerror("Save Error", f"Could not save tasks:\n{e}")

    # ---------- List rendering ----------
    def refresh_list(self):
        """Render tasks list safely even if some entries are missing fields."""
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            text = task.get("text", "")
            done = bool(task.get("done", False))
            prefix = "[x] " if done else "[ ] "
            display = prefix + text
            self.listbox.insert(tk.END, display)
            if done:
                idx = self.listbox.size() - 1
                # itemconfig uses 'fg' on tk.Listbox
                try:
                    self.listbox.itemconfig(idx, fg="#888888")
                except Exception:
                    # In case itemconfig is unsupported on some platforms, ignore.
                    pass
        self.update_status()

    def update_status(self):
        total = len(self.tasks)
        done = sum(1 for t in self.tasks if t.get("done"))
        self.status_var.set(f"{done} of {total} tasks completed")

    # ---------- Actions ----------
    def add_task(self):
        text = self.entry.get().strip()
        if not text:
            return
        self.tasks.append(
            {
                "text": text,
                "done": False,
                "created": datetime.now().strftime("%Y-%m-%d %H:%M"),
            }
        )
        self.entry.delete(0, tk.END)
        self.save_tasks()
        self.refresh_list()

    def get_selected_index(self):
        selection = self.listbox.curselection()
        if not selection:
            messagebox.showinfo("No Selection", "Please select a task first.")
            return None
        return selection[0]

    def toggle_done(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        self.tasks[idx]["done"] = not self.tasks[idx]["done"]
        self.save_tasks()
        self.refresh_list()

    def edit_task(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        current_text = self.tasks[idx]["text"]
        new_text = simpledialog.askstring(
            "Edit Task", "Update task:", initialvalue=current_text
        )
        if new_text and new_text.strip():
            self.tasks[idx]["text"] = new_text.strip()
            self.save_tasks()
            self.refresh_list()

    def delete_task(self):
        idx = self.get_selected_index()
        if idx is None:
            return
        confirm = messagebox.askyesno("Delete Task", "Delete this task?")
        if confirm:
            del self.tasks[idx]
            self.save_tasks()
            self.refresh_list()

    def clear_completed(self):
        if not any(t.get("done") for t in self.tasks):
            return
        confirm = messagebox.askyesno(
            "Clear Completed", "Remove all completed tasks?"
        )
        if confirm:
            self.tasks = [t for t in self.tasks if not t.get("done")]
            self.save_tasks()
            self.refresh_list()


def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
