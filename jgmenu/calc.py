#!/usr/bin/python3

import tkinter as tk
from tkinter import ttk

# Colors
LABEL_COLOR = "#25265E"

# Fonts
DEFAULT_FONT_STYLE = ("Arial", 20)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)

class TkinterCalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("375x667")
        self.window.resizable(1, 1)
        self.window.title("Calculator")

        # Apply a modern theme
        style = ttk.Style(self.window)
        style.configure('TFrame', background='#D9D9D9')
        style.configure('TLabel', background='#D9D9D9', foreground='#000FFF', font=('Helvetica', 12))
        style.configure('TButton', background='#2E2E2E', foreground='white', font=('Helvetica', 12), relief='raised', padding=(10, 5))
        style.configure('TScale', background='#2E2E2E')
        style.map('TButton', background=[('active', '#5E5E5E')])

        self.total_expression = ""
        self.current_expression = ""

        self.display_frame = self.create_display_frame()
        self.total_label, self.label = self.create_display_labels()

        self.digits = {
            7: (1, 1),
            8: (1, 2),
            9: (1, 3),
            4: (2, 1),
            5: (2, 2),
            6: (2, 3),
            1: (3, 1),
            2: (3, 2),
            3: (3, 3),
            0: (4, 2),
            '.': (4, 1)
        }
        self.operations = {
            "/": "\u00F7",
            "*": "\u00D7",
            "-": "-",
            "+": "+",
        }

        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.bind_keys()

    def run(self):
        self.window.mainloop()

    # Create
    def create_sqrt_button(self):
        button = ttk.Button(self.buttons_frame, text="\u221ax", command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def create_equals_button(self):
        button = ttk.Button(self.buttons_frame, text="=", command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = ttk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_label = ttk.Label(self.display_frame, text=self.total_expression, anchor=tk.E)
        total_label.pack(expand=True, fill='both', padx=24)
        total_label.configure(font=SMALL_FONT_STYLE)

        label = ttk.Label(self.display_frame, text=self.current_expression, anchor=tk.E)
        label.pack(expand=True, fill='both', padx=24)
        label.configure(font=LARGE_FONT_STYLE)

        return total_label, label

    def create_display_frame(self):
        frame = ttk.Frame(self.window, height=221)
        frame.pack(expand=True, fill="both")
        return frame

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = ttk.Button(self.buttons_frame, text=str(digit), command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = ttk.Button(self.buttons_frame, text=symbol, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def create_clear_button(self):
        button = ttk.Button(self.buttons_frame, text="C", command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def create_square_button(self):
        button = ttk.Button(self.buttons_frame, text="x\u00b2", command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def add_to_expression(self, value):
        self.current_expression += str(value)
        self.update_label()

    def append_operator(self, operator):
        self.current_expression += operator
        self.total_expression += self.current_expression
        self.current_expression = ""
        self.update_total_label()
        self.update_label()

    # Handle
    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    # Update
    def update_total_label(self):
        expression = self.total_expression

        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')

        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    # Evaluate
    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()

        try:
            self.current_expression = str(eval(self.total_expression))
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

if __name__ == "__main__":
    tkinter_calculator = TkinterCalculator()
    tkinter_calculator.run()
