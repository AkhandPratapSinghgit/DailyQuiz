import random
import requests
import tkinter as tk
from tkinter import messagebox

class DailyQuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Daily Quiz App")
        self.daily_score = 0
        self.api_url = 'https://opentdb.com/api.php?amount=10&category=17&type=multiple'

        self.questions = []
        self.current_question_index = -1
        self.current_question = None

        # Configure the root window
        self.root.configure(bg="orange")

        # Question number label
        self.question_number_label = tk.Label(root, text="", font=("Times New Roman", 14), bg="orange")
        self.question_number_label.pack(pady=10)

        # Question label
        self.question_label = tk.Label(root, text="", wraplength=400, justify="left", font=("Times New Roman", 16), bg="orange")
        self.question_label.pack(pady=20)

        # Choice variable and radio buttons
        self.choice_var = tk.StringVar()
        self.choices_radiobuttons = []

        for i in range(4):
            rb = tk.Radiobutton(root, text="", variable=self.choice_var, value="", wraplength=400, justify="left",
                                font=("Times New Roman", 14), bg="orange")
            rb.pack(anchor="w", padx=20)
            self.choices_radiobuttons.append(rb)

        # Submit button
        self.submit_button = tk.Button(root, text="Submit", command=self.submit_answer, font=("Times New Roman", 14))
        self.submit_button.pack(pady=20)

        self.run_daily_quiz()

    def fetch_questions(self):
        response = requests.get(self.api_url)
        if response.status_code == 200:
            return response.json()['results']
        else:
            print("Failed to fetch questions.")
            return []

    def display_question(self):
        self.current_question_index += 1
        if self.current_question_index < len(self.questions):
            self.current_question = self.questions[self.current_question_index]
            question_text = self.current_question["question"]
            choices = self.current_question['incorrect_answers'] + [self.current_question['correct_answer']]
            random.shuffle(choices)

            self.question_number_label.config(text=f"Question {self.current_question_index + 1}")
            self.question_label.config(text=question_text)
            self.choice_var.set(None)  # Deselect any previously selected radio button

            for i in range(4):
                self.choices_radiobuttons[i].config(text=choices[i], value=choices[i])

            self.submit_button.pack()  # Show submit button
        else:
            self.end_quiz()

    def submit_answer(self):
        selected_choice = self.choice_var.get()

        if selected_choice:
            self.evaluate_response(selected_choice)
        else:
            messagebox.showwarning("Warning", "Please select an answer before submitting.")

    def evaluate_response(self, user_response):
        correct_answer = self.current_question['correct_answer']
        if user_response == correct_answer:
            messagebox.showinfo("Correct!", "Your answer is correct!")
            self.daily_score += 10  # Points for a correct answer
        else:
            messagebox.showinfo("Incorrect", f"Incorrect. The correct answer is: {correct_answer}")

        self.submit_button.pack_forget()  # Hide submit button
        self.root.after(2000, self.display_question)  # Move to the next question after 2 seconds

    def run_daily_quiz(self):
        self.questions = self.fetch_questions()
        self.display_question()

    def end_quiz(self):
        feedback = self.get_feedback()
        messagebox.showinfo("Quiz Complete", f'Quiz complete! Your daily score is: {self.daily_score} points.\n\n{feedback}')
        self.root.destroy()

    def get_feedback(self):
        if self.daily_score >= 90:
            return "Excellent performance! You have a strong grasp of general knowledge."
        elif self.daily_score >= 70:
            return "Good job! You have a good understanding of general knowledge."
        elif self.daily_score >= 50:
            return "Fair effort! There's room for improvement in your general knowledge."
        else:
            return "Keep practicing! It looks like you need to work on your general knowledge."

if __name__ == "__main__":
    root = tk.Tk()
    app = DailyQuizApp(root)
    root.mainloop()
