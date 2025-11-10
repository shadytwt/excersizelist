import tkinter as tk
from tkinter import messagebox
import random

def displayMenu():
    """Shows difficulty selection screen."""
    clear_window()

    title = tk.Label(root, text="🧮 MATHS QUIZ 🧮", bg="#F7F9FB", fg="#2B2D42",
                     font=("Helvetica", 22, "bold"))
    title.pack(pady=30)

    tk.Label(root, text="Select Difficulty Level", bg="#F7F9FB", fg="#2B2D42",
             font=("Helvetica", 14, "bold")).pack(pady=10)

    create_menu_button("Easy (1-digit)", lambda: start_quiz(1))
    create_menu_button("Moderate (2-digit)", lambda: start_quiz(2))
    create_menu_button("Advanced (4-digit)", lambda: start_quiz(3))


def create_menu_button(text, command):
    """Helper to create styled buttons."""
    btn = tk.Button(root, text=text, command=command,
                    bg="#8D99AE", fg="white", font=("Helvetica", 12, "bold"),
                    activebackground="#EF233C", activeforeground="white",
                    relief="flat", width=20, height=2)
    btn.pack(pady=8)


def randomInt(level):
    """Returns random integer based on difficulty."""
    if level == 1:
        return random.randint(1, 9)
    elif level == 2:
        return random.randint(10, 99)
    else:
        return random.randint(1000, 9999)


def decideOperation():
    """Randomly returns '+' or '-'."""
    return random.choice(['+', '-'])


def clear_window():
    """Removes all widgets from the window."""
    for widget in root.winfo_children():
        widget.destroy()


def start_quiz(level):
    """Initializes variables and starts quiz."""
    global difficulty, question_num, score, attempt
    difficulty = level
    question_num = 0
    score = 0
    attempt = 1
    next_question()


def next_question():
    """Generates and displays the next question."""
    global num1, num2, op, correct_answer, question_num, attempt
    clear_window()
    question_num += 1
    attempt = 1

    if question_num > 10:
        displayResults()
        return

    num1 = randomInt(difficulty)
    num2 = randomInt(difficulty)
    op = decideOperation()
    correct_answer = num1 + num2 if op == '+' else num1 - num2

    tk.Label(root, text=f"Question {question_num} of 10", bg="#F7F9FB",
             fg="#2B2D42", font=("Helvetica", 14, "italic")).pack(pady=10)

    tk.Label(root, text=f"{num1} {op} {num2} =", bg="#F7F9FB",
             fg="#D90429", font=("Helvetica", 32, "bold")).pack(pady=20)

    global answer_entry
    answer_entry = tk.Entry(root, font=("Helvetica", 20), justify='center',
                            bg="#EDF2F4", relief="flat")
    answer_entry.pack(pady=10, ipadx=10, ipady=5)
    answer_entry.focus()

    tk.Button(root, text="Submit", bg="#2B2D42", fg="white",
              activebackground="#8D99AE", activeforeground="white",
              font=("Helvetica", 13, "bold"), width=10,
              relief="flat", command=check_answer).pack(pady=20)


def check_answer():
    """Checks user's answer and awards score."""
    global score, attempt

    try:
        user_answer = int(answer_entry.get())
    except ValueError:
        messagebox.showwarning("Invalid", "Please enter a number.")
        return

    if user_answer == correct_answer:
        if attempt == 1:
            messagebox.showinfo("Correct!", "✅ Correct! +10 points")
            score += 10
        else:
            messagebox.showinfo("Correct!", "✅ Correct on second try! +5 points")
            score += 5
        next_question()
    else:
        if attempt == 1:
            messagebox.showwarning("Incorrect", "❌ Wrong! Try again.")
            attempt = 2
            answer_entry.delete(0, tk.END)
        else:
            messagebox.showinfo("Incorrect", f"❌ Wrong again! The correct answer was {correct_answer}.")
            next_question()


def displayResults():
    """Displays the final result and grade."""
    clear_window()

    tk.Label(root, text="🎉 Quiz Completed! 🎉", bg="#F7F9FB",
             fg="#2B2D42", font=("Helvetica", 20, "bold")).pack(pady=20)

    tk.Label(root, text=f"Your final score: {score}/100", bg="#F7F9FB",
             fg="#D90429", font=("Helvetica", 16, "bold")).pack(pady=10)

    if score >= 90:
        grade = "A+"
    elif score >= 80:
        grade = "A"
    elif score >= 70:
        grade = "B"
    elif score >= 60:
        grade = "C"
    else:
        grade = "F"

    tk.Label(root, text=f"Your grade: {grade}", bg="#F7F9FB",
             fg="#2B2D42", font=("Helvetica", 16)).pack(pady=10)

    tk.Button(root, text="Play Again", bg="#2B2D42", fg="white",
              font=("Helvetica", 12, "bold"), activebackground="#8D99AE",
              relief="flat", width=15, command=displayMenu).pack(pady=10)

    tk.Button(root, text="Exit", bg="#EF233C", fg="white",
              font=("Helvetica", 12, "bold"), activebackground="#D90429",
              relief="flat", width=15, command=root.destroy).pack(pady=5)



root = tk.Tk()
root.title("Maths Quiz Game")
root.geometry("420x500")
root.configure(bg="#F7F9FB")
root.resizable(False, False)

displayMenu()

root.mainloop()
