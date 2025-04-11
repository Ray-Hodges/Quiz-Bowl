# quiz.py

import tkinter as tk
from tkinter import messagebox
from database import get_connection

class QuizCategorySelection:
    def __init__(self, root):
        self.root = root
        self.root.title("Choose Quiz Category")
        self.root.geometry("300x250")

        tk.Label(root, text="Select a Quiz", font=("Arial", 14)).pack(pady=20)

        self.course_var = tk.StringVar()
        courses = ["DS_3850", "DS_3860", "FIN_3210", "DS_4125", "PSY_1030"]
        for course in courses:
            tk.Radiobutton(root, text=course, variable=self.course_var, value=course).pack(anchor="w", padx=30)

        tk.Button(root, text="Start Quiz", command=self.start_quiz).pack(pady=10)
        tk.Button(root, text="Back to Main Menu", command=self.back_to_main).pack(pady=5)

    def start_quiz(self):
        course = self.course_var.get()
        if not course:
            messagebox.showerror("Error", "Please select a course.")
            return

        self.root.destroy()
        quiz_root = tk.Tk()
        QuizInterface(quiz_root, course)
        quiz_root.mainloop()

    def back_to_main(self):
        self.root.destroy()
        from main import QuizApp
        main_root = tk.Tk()
        QuizApp(main_root)
        main_root.mainloop()

class QuizInterface:
    def __init__(self, root, course):
        self.root = root
        self.course = course
        self.root.title(f"{course} Quiz")
        self.root.geometry("500x400")

        self.conn = get_connection()
        self.cursor = self.conn.cursor()
        self.cursor.execute(f"SELECT * FROM {course}")
        self.questions = self.cursor.fetchall()
        self.conn.close()

        self.current_index = 0
        self.score = 0
        self.user_answer = tk.StringVar()

        self.question_label = tk.Label(root, wraplength=450, font=("Arial", 12))
        self.question_label.pack(pady=20)

        self.radio_buttons = []
        for i in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.user_answer, value="", font=("Arial", 10))
            rb.pack(anchor="w", padx=30)
            self.radio_buttons.append(rb)

        self.feedback_label = tk.Label(root, text="", font=("Arial", 10))
        self.feedback_label.pack(pady=10)

        self.next_button = tk.Button(root, text="Next", command=self.next_question)
        self.next_button.pack(pady=10)

        self.show_question()

    def show_question(self):
        if self.current_index >= len(self.questions):
            self.end_quiz()
            return

        question = self.questions[self.current_index]
        self.user_answer.set("")  # Clear selection

        self.question_label.config(text=f"Q{self.current_index + 1}: {question[1]}")
        options = question[2:6]
        for i, rb in enumerate(self.radio_buttons):
            rb.config(text=options[i], value=chr(65 + i))  # A, B, C, D

        self.feedback_label.config(text="")

    def next_question(self):
        question = self.questions[self.current_index]
        selected = self.user_answer.get()

        if not selected:
            messagebox.showerror("Error", "Please select an answer.")
            return

        correct = question[6].strip().upper()
        if selected == correct:
            self.score += 1
            self.feedback_label.config(text="✅ Correct!", fg="green")
        else:
            self.feedback_label.config(text=f"❌ Incorrect! Correct answer: {correct}", fg="red")

        self.current_index += 1
        self.root.after(1000, self.show_question)

    def end_quiz(self):
        messagebox.showinfo("Quiz Completed", f"Your score: {self.score} / {len(self.questions)}")
        self.root.destroy()
        from main import QuizApp
        main_root = tk.Tk()
        QuizApp(main_root)
        main_root.mainloop()
