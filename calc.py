

# https://www.fileformat.info/info/unicode/char/a.htm

import tkinter as tk

DARK = '#313842'
LABEL = '#c5dcfc'
DIGIT = '#91b4e6'
OPRN = '#7faef0'
EQUAL = '#5379b0'

SMALL_FONT = ('Arial', 16)
LARGE_FONT = ('Arial', 40, 'bold')
DIGIT_FONT = ('Arial', 24, 'bold')
DEFAULT_FONT = ('Arial', 20)


class Calculator:
    def __init__(self):
        self.window = tk.Tk()               # root
        self.window.geometry('375x667')
        self.window.resizable(0, 0)         # not resizable
        self.window.title('Calculator')

        self.total_expression = ""          # small total on top
        self.current_expression = ""        # current value

        self.display_frame = self.create_display_frame()  # the order will be when they gonna be executed

        self.total_label, self.label = self.create_display_labels()

        self.digits = {  # skip the first row
            7: (1, 1),
            8: (1, 2),
            9: (1, 3),  # row=grid_value[0], column=grid_value[1]
            4: (2, 1),
            5: (2, 2),
            6: (2, 3),  # 7 = row: 1, column: 1
            1: (3, 1),
            2: (3, 2),
            3: (3, 3),
            '.': (4, 1),
            0: (4, 2)
        }
        self.operations = {"/": "\u00F7", "*": "\u00D7", "-": "-", "+": "+"}

        self.buttons_frame = self.create_buttons_frame()

        self.buttons_frame.rowconfigure(0, weight=1)  # add buttons to frame
        for i in range(1, 5):
            self.buttons_frame.rowconfigure(i, weight=1)
            self.buttons_frame.columnconfigure(i, weight=1)

        self.create_digit_buttons()  # have to be below buttons_frame cus frame has to be created before btns
        self.create_operation_buttons()
        self.create_special_buttons()
        self.bind_keys()


    def bind_keys(self):            # accepts keyboard inputs
        self.window.bind("<Return>", lambda event: self.evaluate())     # pressing then enter = equal btn

        for key in self.digits:
            self.window.bind(str(key), lambda event, digit=key: self.add_to_expression(digit))
        for key in self.operations:
            self.window.bind(key, lambda event, operator=key: self.append_operator(operator))
            

    def create_special_buttons(self): 
        self.create_equal_button()
        self.create_clear_button()
        self.create_delete_button()
        self.create_square_button()
        self.create_sqrt_button()

    def create_display_labels(self):
        total_label = tk.Label(self.display_frame,
                               text=self.total_expression,
                               anchor=tk.E,
                               bg=DARK,
                               fg=LABEL,
                               padx=24,
                               font=SMALL_FONT)
        total_label.pack(expand=True, fill='both')

        label = tk.Label(self.display_frame,
                         text=self.current_expression,
                         anchor=tk.E,
                         bg=DARK,
                         fg=LABEL,
                         padx=24,
                         font=LARGE_FONT)
        label.pack(expand=True, fill='both')

        return total_label, label

    def create_display_frame(self):
        frame = tk.Frame(self.window, heigh=150, bg=DARK)
        frame.pack(
            expand=True, fill='both'
        )  # organizes widgets in blocks before placing them in the parent widget.
        return frame

    def add_to_expression(self, value):  # add digit to current display
        self.current_expression += str(value)
        self.update_label()

    def create_digit_buttons(self):
        for digit, grid_value in self.digits.items(
        ):  # use lambda to wrap command into a function, x=digit to bind the digit according to every press and display it
            button = tk.Button(
                self.buttons_frame,
                text=str(digit),
                bg=DIGIT,
                fg=DARK,
                font=DIGIT_FONT,
                borderwidth=0,
                command=lambda x=digit: self.add_to_expression(x))
            button.grid(row=grid_value[0],
                        column=grid_value[1],
                        sticky=tk.NSEW)  # NSEW = stick everywhere


    def append_operator(self, operator):
        self.current_expression += operator  # append the operator to current expression
        self.total_expression += self.current_expression
        self.current_expression = ""  # reset
        self.update_total_label()  # update to main display
        self.update_label()  # then transfer to top display

    def create_operation_buttons(self):
        i = 0
        for operator, symbol in self.operations.items():  # use lambda so every time an oprn is pressed it would be recorded and updated to display
            button = tk.Button(
                self.buttons_frame,
                text=symbol,
                bg=OPRN,
                fg=LABEL,
                font=DEFAULT_FONT,
                borderwidth=0,
                command=lambda x=operator: self.append_operator(x))
            button.grid(row=i, column=4, sticky=tk.NSEW)  # last column, vertical
            i += 1


    def clear(self):
        self.current_expression = ""
        self.total_expression = ""
        self.update_total_label()
        self.update_label()

    def create_clear_button(self):
        button = tk.Button(self.buttons_frame,
                           text='C',
                           bg=OPRN,
                           fg=LABEL,
                           font=DEFAULT_FONT,
                           borderwidth=0,
                           command=self.clear)
        button.grid(row=0, column=1, sticky=tk.NSEW)


    def evaluate(self):                                             # for equal btns
        self.total_expression += self.current_expression
        self.update_total_label()
        try:
            self.current_expression = str(eval(self.total_expression))  # eval, calc then display on main screen

            self.total_expression = ""                                  # total value is reset
        except Exception as e:
            self.current_expression = "Error"                           # catch 1/0 = error
        finally:
            self.update_label()

    def create_equal_button(self):
        button = tk.Button(self.buttons_frame,
                           text='=',
                           bg=EQUAL,
                           fg=LABEL,
                           font=DEFAULT_FONT,
                           borderwidth=0,
                           command=self.evaluate)
        button.grid(row=4, column=4, sticky=tk.NSEW) 


    def delete(self):
        self.current_expression = self.current_expression[:-1]    # delete last digit   
        self.update_label()

    def create_delete_button(self):
        button = tk.Button(self.buttons_frame,
                           text='\u232B',
                           bg=OPRN,
                           fg=LABEL,
                           font=SMALL_FONT,
                           borderwidth=0,
                           command=self.delete)
        button.grid(row=4, column=3, sticky=tk.NSEW)  


    def square(self):                                              # f"" = str.format(), ** = power
        self.current_expression = str(eval(f"{self.current_expression}**2"))
        self.update_label()

    def create_square_button(self):
        button = tk.Button(self.buttons_frame,
                    text='x\u00b2',
                    bg=OPRN,
                    fg=LABEL,
                    font=DEFAULT_FONT,
                    borderwidth=0,
                    command=self.square)
        button.grid(row=0, column=2, sticky=tk.NSEW)  


    def sqrt(self):                                              
        self.current_expression = str(eval(f"{self.current_expression}**0.5"))
        self.update_label()

    def create_sqrt_button(self):
        button = tk.Button(self.buttons_frame,
                    text='\u221a',
                    bg=OPRN,
                    fg=LABEL,
                    font=DEFAULT_FONT,
                    borderwidth=0,
                    command=self.sqrt)
        button.grid(row=0, column=3, sticky=tk.NSEW)  


    def create_buttons_frame(self):
        frame = tk.Frame(self.window, height=200)
        frame.pack(expand=True, fill='both')
        return frame

    def update_total_label(self):                                    # update top display
        expression = self.total_expression
        for operator, symbol in self.operations.items():
            expression = expression.replace(operator, f" {symbol} ") # show x and % symbol
        self.total_label.config(text=expression)

    def update_label(self):                                 # update current display
        self.label.config(text=self.current_expression[:11])        # show 11 digits

    def run(self):
        self.window.mainloop()  # loop forever until user closes the program


# main
if __name__ == '__main__':  # protects users from accidentally invoking the script when they didn't intend to
    calc = Calculator()
    calc.run()