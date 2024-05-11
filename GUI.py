import tkinter as tk
import csv


class GradeCalculatorApp(tk.Tk):  # main window created
    def __init__(self):
        super().__init__()
        self.title("Grade Calculator")
        self.geometry("400x400")
        self.resizable(False, False)

        self.student_names = []

        self.label = tk.Label(self, text="Enter the total number of students (maximum 4):")
        self.label.pack()

        self.entry = tk.Entry(self)
        self.entry.pack()

        self.button = tk.Button(self, text="Submit", command=self.create_score_window)
        self.button.pack()

        self.exit_button = tk.Button(self, text="Exit", command=self.exit_app)
        self.exit_button.pack()

    def create_score_window(self):
        num_students = self.entry.get()
        if not num_students.isdigit():  # validate number of student
            self.show_error("Please enter a valid number.")
            return

        num_students = int(num_students)
        if num_students <= 0 or num_students > 4:
            self.show_error("Number of students must be between 1 and 4.")
            return

        for _ in range(num_students):
            name = tk.StringVar()
            self.student_names.append(name)

            label = tk.Label(self, text="Enter student name:")
            label.pack()

            entry = tk.Entry(self, textvariable=name)
            entry.pack()

        submit_button = tk.Button(self, text="Submit", command=self.validate_names)
        submit_button.pack()

    def validate_names(self):  # validation of name, cant be empty
        for name in self.student_names:
            if not name.get().strip():
                self.show_error("Please enter all student names.")
                return
        self.create_score_input_window()

    def create_score_input_window(self):
        score_window = ScoreInputWindow(self, self.student_names)
        score_window.mainloop()

    def show_error(self, message):
        error_window = ErrorWindow(self, message)
        error_window.mainloop()

    def exit_app(self):  # safe exit
        self.destroy()


class ScoreInputWindow(tk.Toplevel):
    def __init__(self, master, student_names):
        super().__init__(master)
        self.title("Enter Scores")
        self.geometry("400x400")
        self.resizable(False, False)

        self.master = master
        self.student_names = student_names

        self.scores = []

        for name in self.student_names:  # dynamic box
            label = tk.Label(self, text=f'Enter score for {name.get()}:')
            label.pack()

            score = tk.StringVar()
            self.scores.append(score)

            entry = tk.Entry(self, textvariable=score)
            entry.pack()

        submit_button = tk.Button(self, text="Submit", command=self.process_scores)
        submit_button.pack()

    def process_scores(self):
        valid_scores = True  # validation of score
        for score in self.scores:
            score_value = score.get()
            if not score_value.isdigit() or not (0 <= int(score_value) <= 100):
                valid_scores = False
                break

        if not valid_scores:
            self.master.show_error("Please enter valid scores (only digits between 0 and 100).")  # inheritance app
            return

        scores = [int(score.get()) for score in self.scores]
        self.calculate_grades(scores)
        self.write_to_csv(scores)

    def calculate_grades(self, scores):  # define best score
        best_score = max(scores)
        for i, score in enumerate(scores):
            grade = self.calculate_grade(score, best_score)
            result = f"{self.student_names[i].get()}: score is {score}, grade is {grade}"
            result_label = tk.Label(self, text=result, fg="red")  # Change text color to red
            result_label.pack()

        # Inform the user that data has been submitted
        submitted_label = tk.Label(self, text="Submitted", fg="red")
        submitted_label.pack()

    def calculate_grade(self, score, best_score):  # logic for grade calculation
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

    def write_to_csv(self, scores):  # transfer student numerical score and grade into csv file
        with open('grades.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Score', 'Grade'])
            for i, score in enumerate(scores):
                grade = self.calculate_grade(score, max(scores))
                writer.writerow([self.student_names[i].get(), score, grade])


class ErrorWindow(tk.Toplevel):  # Error messages window
    def __init__(self, master, message):
        super().__init__(master)
        self.title("Error")
        self.geometry("300x150")
        self.resizable(False, False)

        self.label = tk.Label(self, text=message)
        self.label.pack()



