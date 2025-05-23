import tkinter as tk
import tkinter.messagebox as messagebox
import math
import fractions  # 添加这个模块来处理分数

LARGE_FONT_STYLE = ("Arial", 40, "bold")
SMALL_FONT_STYLE = ("Arial", 16)
DIGITS_FONT_STYLE = ("Arial", 24, "bold")
DEFAULT_FONT_STYLE = ("Arial", 20)

OFF_WHITE = "#F8FAFF"
WHITE = "#FFFFFF"
LIGHT_BLUE = "#CCEDFF"
LIGHT_GRAY = "#F5F5F5"
LABEL_COLOR = "#25265E"


class Calculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.geometry("475x667")
        self.window.resizable(0, 0)
        self.window.title("Calculator")

        self.total_expression = ""
        self.current_expression = ""
        self.history = []  # 添加历史记录列表
        self.display_frame = self.create_display_frame()

        self.total_label, self.label = self.create_display_labels()

        self.mode = "basic"  # 初始模式
        self.digits = {
            7: (1, 1), 8: (1, 2), 9: (1, 3),
            4: (2, 1), 5: (2, 2), 6: (2, 3),
            1: (3, 1), 2: (3, 2), 3: (3, 3),
            0: (4, 2), '.': (4, 1)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}
        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)
        for x in range(1, 5):
            self.buttons_frame.rowconfigure(x, weight=1)
            self.buttons_frame.columnconfigure(x, weight=1)
        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_mode_switch_button()  # 创建模式切换按钮
        self.bind_keys()

    def bind_keys(self):
        self.window.bind("<Return>", lambda event: self.evaluate())
        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))

        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))

    def create_special_buttons(self):
        self.create_clear_button()
        self.create_equals_button()
        self.create_square_button()
        self.create_sqrt_button()
        self.create_delete_button()  # 创建删除按钮
        self.create_history_button()  # 创建历史记录按钮

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame, text=self.total_expression, anchor=tk.E, bg=LIGHT_GRAY,
                               fg=LABEL_COLOR, padx=24, font=SMALL_FONT_STYLE)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame, text=self.current_expression, anchor=tk.E, bg=LIGHT_GRAY,
                         fg=LABEL_COLOR, padx=24, font=LARGE_FONT_STYLE)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, height=221, bg=LIGHT_GRAY)
        frame.pack(expand=True, fill="both")
        return frame

    def add_to_expression(self, value):
        if self.mode == "scientific" and value in ["sin", "cos", "tan", "asin", "acos", "atan"]:
            self.current_expression += f"math.{value}(math.radians("
        else:
            self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items():
            button = tk.Button(self.buttons_frame, text=str(digit), bg=WHITE, fg=LABEL_COLOR, font=DIGITS_FONT_STYLE,
                               borderwidth=0, command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)

    def append_operator(self, operator):
        if self.current_expression.endswith('/'):
            self.current_expression += operator
        else:
            self.current_expression += operator
            self.total_expression += self.current_expression
            self.current_expression = ""
        self.update_total_label()
        self.update_label()

    def create_operator_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():
            button = tk.Button(self.buttons_frame, text=symbol, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                               borderwidth=0, command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)
            i += 1

    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_label()
        self.update_total_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame, text="C", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)

    def square(self):
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame, text="x\u00b2", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)

    def sqrt(self):
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame, text="\u221ax", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)

    def evaluate(self):
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            # 处理分数表达式
            if '/' in self.total_expression and not self.total_expression.startswith('math.'):
                self.current_expression = str(eval("fractions.Fraction(" + self.total_expression + ")"))
            else:
                self.current_expression = str(eval(self.total_expression))
            self.history.append(self.total_expression + " = " + self.current_expression)  # 保存到历史记录
            self.total_expression = ""
        except Exception as e:
            self.current_expression = "Error"
        finally:
            self.update_label()

    def create_equals_button(self):
        button = tk.Button(self.buttons_frame, text="=", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.evaluate)
        button.grid(row=4, column=3, columnspan=2, sticky=tk.NSEW)

    def create_buttons_frame(self):
        frame = tk.Frame(self.window)
        frame.pack(expand=True, fill="both")
        return frame

    def update_total_label(self):
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f' {symbol} ')
        self.total_label.config(text=expression)

    def update_label(self):
        self.label.config(text=self.current_expression[:11])

    def switch_mode(self):
        if self.mode == "basic":
            self.mode = "scientific"
            self.window.geometry("675x450")  # 调整窗口大小以适应科学模式下的按钮
        elif self.mode == "scientific":
            self.mode = "programmer"
            self.window.geometry("675x450")  # 调整窗口大小以适应编程模式下的按钮
        else:
            self.mode = "basic"
            self.window.geometry("475x667")  # 调整窗口大小以适应基本模式下的按钮
        self.update_buttons()
    def create_mode_switch_button(self):
        button = tk.Button(self.buttons_frame, text="Mode", bg=LIGHT_BLUE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.switch_mode)
        button.grid(row=4, column=0, sticky=tk.NSEW)

    def update_buttons(self):
        for widget in self.buttons_frame.winfo_children():
            widget.destroy()

        self.create_digit_buttons()
        self.create_operator_buttons()
        self.create_special_buttons()
        self.create_mode_switch_button()

        # 在所有模式下都添加清零和删除按钮
        self.create_clear_button()
        self.create_delete_button()

        if self.mode == "scientific":
            self.create_scientific_buttons()
            for i in range(6):  # 根据科学模式下的行数调整
                self.buttons_frame.rowconfigure(i, weight=1)
            self.buttons_frame.columnconfigure(5, weight=1)  # 添加额外的列配置
        elif self.mode == "programmer":
            self.create_programmer_buttons()
            for i in range(5):  # 根据编程模式下的行数调整
                self.buttons_frame.rowconfigure(i, weight=1)
            self.buttons_frame.columnconfigure(5, weight=1)  # 添加额外的列配置


    def create_scientific_buttons(self):
        scientific_buttons = {
            "sin": (0, 5), "cos": (1, 5), "tan": (2, 5), "asin": (3, 5),
            "acos": (4, 5), "atan": (0, 6), "log": (1, 6), "ln": (2, 6),
            "(": (3, 6), ")": (4, 6), "exp": (0, 7), "π": (1, 7)
        }
        for text, grid_value in scientific_buttons.items():
            button = tk.Button(self.buttons_frame, text=text, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=lambda x=text: self.add_to_expression(f"math.{x}(" if x in ["sin", "cos", "tan", "asin", "acos", "atan", "log", "ln", "exp"] else (str(math.pi) if x == "π" else x)))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)
    def create_programmer_buttons(self):
        programmer_buttons = {
            "AND": (0, 5), "OR": (1, 5), "XOR": (2, 5), "NOT": (3, 5),
            "LSH": (4, 5), "RSH": (0, 6), "BIN": (1, 6), "HEX": (2, 6)
        }
        for text, grid_value in programmer_buttons.items():
            button = tk.Button(self.buttons_frame, text=text, bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                            borderwidth=0, command=lambda x=text: self.add_to_expression(x))
            button.grid(row=grid_value[0], column=grid_value[1], sticky=tk.NSEW)    
    def delete_last_char(self):
        self.current_expression = self.current_expression[:-1]
        self.update_label()

    def create_delete_button(self):
        button = tk.Button(self.buttons_frame, text="DEL", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.delete_last_char)
        button.grid(row=0, column=0, sticky=tk.NSEW)

    def show_history(self):
        if self.history:
            history_str = "\n".join(self.history)
            tk.messagebox.showinfo("History", history_str)
        else:
            tk.messagebox.showinfo("History", "No history yet.")

    def create_history_button(self):
        button = tk.Button(self.buttons_frame, text="H", bg=OFF_WHITE, fg=LABEL_COLOR, font=DEFAULT_FONT_STYLE,
                           borderwidth=0, command=self.show_history)
        button.grid(row=4, column=1, sticky=tk.NSEW)

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    calc = Calculator()
    calc.run()