"""
Improved Calculator GUI

- Encapsulated in a Calculator class (no globals)
- Uses ttk for consistent look & larger, accessible fonts
- Uses StringVar for the display
- Supports float arithmetic and operator chaining
- Handles divide-by-zero and invalid input gracefully
- Keyboard bindings for accessibility (digits, + - * /, Enter, Backspace, Esc)
- Uses grid layout for consistent placement/resizing
- Single mainloop call
"""
import tkinter as tk
from tkinter import ttk
from typing import Optional

class Calculator(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Accessible Calculator")
        self.geometry("360x460")
        self.resizable(False, False)

        # Styling
        self.style = ttk.Style(self)
        try:
            self.style.theme_use("clam")
        except Exception:
            pass
        self.font = ("Segoe UI", 14)

        # State
        self.display_var = tk.StringVar(value="0")
        self._operand: Optional[float] = None
        self._operator: Optional[str] = None
        self._reset_next = False  # whether next digit press should start a new entry

        self._build_ui()
        self._bind_keys()

    def _build_ui(self) -> None:
        # Display frame
        disp_frame = ttk.Frame(self, padding=(10, 10, 10, 0))
        disp_frame.pack(fill="x")

        display = ttk.Entry(
            disp_frame,
            textvariable=self.display_var,
            font=("Segoe UI", 20),
            justify="right",
            state="readonly",
        )
        # Make entry focusable for screen readers; use readonly to disallow typing
        display.pack(fill="x", ipady=10)

        # Buttons frame
        btn_frame = ttk.Frame(self, padding=10)
        btn_frame.pack(fill="both", expand=True)

        btn_cfg = {"width": 6, "padding": 6}
        # Layout using grid (row, column)
        buttons = [
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("/", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("*", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("-", 3, 3),
            ("0", 4, 0), (".", 4, 1), ("=", 4, 2), ("+", 4, 3),
        ]

        for (text, r, c) in buttons:
            action = (lambda val=text: self.on_button(val))
            btn = ttk.Button(btn_frame, text=text, command=action)
            btn.grid(row=r, column=c, sticky="nsew", padx=4, pady=4)
            btn.configure(style="TButton")
            btn.bind("<Return>", lambda e, val=text: self.on_button(val))  # keyboard activation

        # Extra controls row
        clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear)
        clear_btn.grid(row=0, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)
        del_btn = ttk.Button(btn_frame, text="Del", command=self.backspace)
        del_btn.grid(row=0, column=2, sticky="nsew", padx=4, pady=4)
        quit_btn = ttk.Button(btn_frame, text="Quit", command=self.destroy)
        quit_btn.grid(row=0, column=3, sticky="nsew", padx=4, pady=4)

        # Make columns expand evenly
        for i in range(4):
            btn_frame.columnconfigure(i, weight=1)
        for i in range(5):
            btn_frame.rowconfigure(i, weight=1)

        # Set accessible focus order (tab order)
        clear_btn.focus_set()

    def _bind_keys(self) -> None:
        # Digits and dot
        for key in "0123456789.":
            self.bind(key, lambda e, ch=key: self.on_digit(ch))
        # Operators
        for key in ("+", "-", "*", "/"):
            self.bind(key, lambda e, op=key: self.on_operator(op))
        # Enter/Return for equals
        self.bind("<Return>", lambda e: self.calculate())
        # Backspace -> delete last char
        self.bind("<BackSpace>", lambda e: self.backspace())
        # Escape -> clear
        self.bind("<Escape>", lambda e: self.clear())

    # UI actions
    def on_button(self, token: str) -> None:
        if token in "0123456789.":
            self.on_digit(token)
        elif token in "+-*/":
            self.on_operator(token)
        elif token == "=":
            self.calculate()
        else:
            # safety fallback
            pass

    def on_digit(self, ch: str) -> None:
        cur = self.display_var.get()
        if self._reset_next or cur == "0":
            new = ch if ch != "." else "0."
            self._reset_next = False
        else:
            # avoid multiple dots
            if ch == "." and "." in cur:
                return
            new = cur + ch
        self.display_var.set(new)

    def on_operator(self, op: str) -> None:
        try:
            cur_val = float(self.display_var.get())
        except ValueError:
            self.display_var.set("Error")
            return
        if self._operand is not None and not self._reset_next:
            # chain previous operation
            self._compute(cur_val)
        else:
            self._operand = cur_val
        self._operator = op
        self._reset_next = True

    def calculate(self) -> None:
        if self._operator is None or self._operand is None:
            return
        try:
            cur_val = float(self.display_var.get())
        except ValueError:
            self.display_var.set("Error")
            return
        try:
            result = self._compute(cur_val)
        except ZeroDivisionError:
            self.display_var.set("∞")
            self._operand = None
            self._operator = None
            self._reset_next = True
            return
        # Display result cleanly: int without .0 when possible
        if result.is_integer():
            self.display_var.set(str(int(result)))
        else:
            # limit display length
            self.display_var.set(str(round(result, 10)).rstrip("0").rstrip("."))
        self._operand = None
        self._operator = None
        self._reset_next = True

    def _compute(self, right: float) -> float:
        assert self._operator is not None and self._operand is not None
        left = self._operand
        op = self._operator
        if op == "+":
            val = left + right
        elif op == "-":
            val = left - right
        elif op == "*":
            val = left * right
        elif op == "/":
            if right == 0:
                raise ZeroDivisionError
            val = left / right
        else:
            raise ValueError("Unknown operator")
        # store intermediate result for chaining
        self._operand = val
        self._reset_next = True
        return val

    def clear(self) -> None:
        self.display_var.set("0")
        self._operand = None
        self._operator = None
        self._reset_next = False

    def backspace(self) -> None:
        cur = self.display_var.get()
        if len(cur) <= 1:
            self.display_var.set("0")
        else:
            self.display_var.set(cur[:-1])

if __name__ == "__main__":
    app = Calculator()
    app.mainloop()