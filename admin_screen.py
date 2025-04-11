# admin_screen.py

import tkinter as tk
from tkinter import messagebox, ttk
from database import get_connection

# --- Admin Login ---
class AdminLogin:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Login")
        self.root.geometry("300x200")

        tk.Label(root, text="Enter Admin Password:").pack(pady=10)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Login", command=self.check_password).pack(pady=10)

    def check_password(self):
        if self.password_entry.get() == "admin123":
            messagebox.showinfo("Success", "Logged in successfully!")
            self.root.destroy()
            dashboard_root = tk.Tk()
            AdminDashboard(dashboard_root)
            dashboard_root.mainloop()
        else:
            messagebox.showerror("Error", "Incorrect password!")

# --- Admin Dashboard ---
class AdminDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Admin Dashboard")
        self.root.geometry("400x300")

        tk.Label(root, text="Admin Dashboard", font=("Arial", 16)).pack(pady=20)
        tk.Button(root, text="Add New Question", width=25, command=self.add_question).pack(pady=10)
        tk.Button(root, text="Manage Questions", width=25, command=self.manage_questions).pack(pady=10)
        tk.Button(root, text="Exit to Main Menu", width=25, command=self.exit_to_main).pack(pady=10)

    def add_question(self):
        self.root.destroy()
        add_root = tk.Tk()
        AddQuestionForm(add_root)
        add_root.mainloop()

    def manage_questions(self):
        self.root.destroy()
        manage_root = tk.Tk()
        QuestionManager(manage_root)
        manage_root.mainloop()

    def exit_to_main(self):
        self.root.destroy()
        from main import QuizApp
        main_root = tk.Tk()
        QuizApp(main_root)
        main_root.mainloop()

# --- Add Question Form ---
class AddQuestionForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Add Question")
        self.root.geometry("400x500")

        tk.Label(root, text="Select Course Category").pack(pady=5)
        self.course_var = tk.StringVar()
        self.course_dropdown = ttk.Combobox(root, textvariable=self.course_var, state="readonly")
        self.course_dropdown['values'] = ["DS_3850", "DS_3860", "FIN_3210", "DS_4125", "PSY_1030"]
        self.course_dropdown.pack(pady=5)

        self.entries = {}
        labels = ["Question Text", "Option A", "Option B", "Option C", "Option D", "Correct Answer (A/B/C/D)"]
        for label in labels:
            tk.Label(root, text=label).pack(pady=3)
            entry = tk.Entry(root, width=40)
            entry.pack(pady=3)
            self.entries[label] = entry

        tk.Button(root, text="Submit", command=self.save_question).pack(pady=15)
        tk.Button(root, text="Back to Dashboard", command=self.back_to_dashboard).pack(pady=5)

    def save_question(self):
        course = self.course_var.get()
        if not course:
            messagebox.showerror("Error", "Please select a course category.")
            return

        question_data = {key: entry.get().strip() for key, entry in self.entries.items()}
        if not all(question_data.values()):
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        try:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"""
                INSERT INTO {course} (question, option_a, option_b, option_c, option_d, correct_answer)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                question_data["Question Text"],
                question_data["Option A"],
                question_data["Option B"],
                question_data["Option C"],
                question_data["Option D"],
                question_data["Correct Answer (A/B/C/D)"].upper()
            ))
            conn.commit()
            conn.close()

            messagebox.showinfo("Success", "Question added successfully!")
            for entry in self.entries.values():
                entry.delete(0, tk.END)

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def back_to_dashboard(self):
        self.root.destroy()
        dash_root = tk.Tk()
        AdminDashboard(dash_root)
        dash_root.mainloop()

# --- Question Manager (View/Edit/Delete) ---
class QuestionManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Manage Questions")
        self.root.geometry("700x500")

        tk.Label(root, text="Select Course Category").pack(pady=5)
        self.course_var = tk.StringVar()
        self.course_dropdown = ttk.Combobox(root, textvariable=self.course_var, state="readonly")
        self.course_dropdown['values'] = ["DS_3850", "DS_3860", "FIN_3210", "DS_4125", "PSY_1030"]
        self.course_dropdown.pack(pady=5)

        tk.Button(root, text="Load Questions", command=self.load_questions).pack(pady=5)

        self.tree = ttk.Treeview(root, columns=("ID", "Question", "A", "B", "C", "D", "Answer"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
        self.tree.pack(fill=tk.BOTH, expand=True, pady=10)

        btn_frame = tk.Frame(root)
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Edit Selected", command=self.edit_selected).grid(row=0, column=0, padx=5)
        tk.Button(btn_frame, text="Delete Selected", command=self.delete_selected).grid(row=0, column=1, padx=5)
        tk.Button(btn_frame, text="Back to Dashboard", command=self.back_to_dashboard).grid(row=0, column=2, padx=5)

    def load_questions(self):
        course = self.course_var.get()
        if not course:
            messagebox.showerror("Error", "Please select a course.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {course}")
        self.questions = cursor.fetchall()
        conn.close()

        self.tree.delete(*self.tree.get_children())
        for q in self.questions:
            self.tree.insert("", tk.END, values=q)

    def edit_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a question to edit.")
            return

        item = self.tree.item(selected[0])
        values = item["values"]
        EditQuestionForm(self.root, self.course_var.get(), values, self.load_questions)

    def delete_selected(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Select a question to delete.")
            return

        item = self.tree.item(selected[0])
        qid = item["values"][0]
        course = self.course_var.get()

        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this question?")
        if confirm:
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {course} WHERE id = ?", (qid,))
            conn.commit()
            conn.close()
            self.load_questions()
            messagebox.showinfo("Deleted", "Question deleted successfully.")

    def back_to_dashboard(self):
        self.root.destroy()
        dash_root = tk.Tk()
        AdminDashboard(dash_root)
        dash_root.mainloop()

# --- Edit Question Form ---
class EditQuestionForm:
    def __init__(self, parent, course, question_data, refresh_callback):
        self.parent = parent
        self.course = course
        self.question_id = question_data[0]
        self.refresh_callback = refresh_callback

        self.edit_win = tk.Toplevel(parent)
        self.edit_win.title("Edit Question")
        self.edit_win.geometry("400x500")

        labels = ["Question", "A", "B", "C", "D", "Answer"]
        self.entries = {}

        for i, label in enumerate(labels):
            tk.Label(self.edit_win, text=label).pack(pady=3)
            entry = tk.Entry(self.edit_win, width=50)
            entry.pack(pady=3)
            entry.insert(0, question_data[i+1])
            self.entries[label] = entry

        tk.Button(self.edit_win, text="Save Changes", command=self.save_changes).pack(pady=10)
        tk.Button(self.edit_win, text="Cancel", command=self.edit_win.destroy).pack()

    def save_changes(self):
        new_data = [entry.get().strip() for entry in self.entries.values()]
        if not all(new_data):
            messagebox.showerror("Error", "Please fill out all fields.")
            return

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(f"""
            UPDATE {self.course}
            SET question = ?, option_a = ?, option_b = ?, option_c = ?, option_d = ?, correct_answer = ?
            WHERE id = ?
        """, (*new_data, self.question_id))
        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Question updated.")
        self.edit_win.destroy()
        self.refresh_callback()
