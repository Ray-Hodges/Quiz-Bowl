import tkinter as tk
from admin_screen import AdminLogin
from quiz import QuizCategorySelection

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Bowl Application")
        self.root.geometry("400x300")
        self.create_login_screen()

    def create_login_screen(self):
        tk.Label(self.root, text="Welcome to Quiz Bowl!", font=("Arial", 18)).pack(pady=20)
        tk.Button(self.root, text="Administrator Login", width=20, command=self.open_admin_login).pack(pady=10)
        tk.Button(self.root, text="Take a Quiz", width=20, command=self.open_quiz).pack(pady=10)

    def open_admin_login(self):
        self.root.destroy()
        admin_root = tk.Tk()
        AdminLogin(admin_root)
        admin_root.mainloop()

    def open_quiz(self):
        self.root.destroy()
        quiz_root = tk.Tk()
        QuizCategorySelection(quiz_root)
        quiz_root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = QuizApp(root)
    root.mainloop()
