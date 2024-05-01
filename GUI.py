import tkinter as tk


class ScoreCalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Score Calculator")
        self.geometry("400x400")
        self.resizable(False, False)

        self.label = tk.Label(self, text="Enter the total number of students:")
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text="Submit", command=self.submit_scores)
        self.button.pack()

        self.exit_button = tk.Button(self, text="Exit", command=self.exit_app)
        self.exit_button.pack()

    def submit_scores(self):
        student = int(self.entry.get())

        score_window = ScoreWindow(self, student)
        score_window.mainloop()

    def exit_app(self):
        self.destroy()


class ScoreWindow(tk.Toplevel):
    def __init__(self, master, student):
        super().__init__(master)
        self.title("Enter Scores")
        self.geometry("400x400")
        self.resizable(False, False)

        self.master = master
        self.student = student

        self.label = tk.Label(self, text=f'Enter {self.student} score(s):')
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text="Submit", command=self.process_scores)
        self.button.pack()

        self.exit_button = tk.Button(self, text="Exit", command=self.exit_window)
        self.exit_button.pack()


    def process_scores(self):
        scores = self.entry.get().strip().split()
        if len(scores) != self.student:
            error_window = ErrorWindow(self, f"You entered {len(scores)} scores instead of {self.student}.")
            error_window.mainloop()
        else:
            scores = [int(score) for score in scores]
            best_score = max(scores)
            for i, score in enumerate(scores):
                grade = self.calculate_grade(score, best_score)
                result = f"Student {i + 1} score is {score} and grade is {grade}"
                result_label = tk.Label(self, text=result)
                result_label.pack()




    def calculate_grade(self, score, best_score):
        if score >= best_score - 10:
            return "A"
        elif score >= best_score - 20:
            return "B"
        elif score >= best_score - 30:
            return "C"
        elif score >= best_score - 40:
            return "D"
        else:
            return "F"

    def exit_window(self):
        self.destroy()


class ErrorWindow(tk.Toplevel):
    def __init__(self, master, message):
        super().__init__(master)
        self.title("Error")
        self.geometry("200x100")
        self.resizable(False, False)

        self.label = tk.Label(self, text=message)
        self.label.pack()


