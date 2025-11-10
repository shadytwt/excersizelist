import tkinter as tk
from tkinter import messagebox
import random

def load_jokes(filename):
    with open(filename, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    jokes = []
    for line in lines:
        if "?" in line:
            parts = line.split("?", 1)
            setup = parts[0].strip() + "?"
            punchline = parts[1].strip()
            jokes.append((setup, punchline))
    return jokes


def show_setup():
    global current_joke
    current_joke = random.choice(jokes)
    joke_label.config(text=current_joke[0])
    punchline_btn.config(state="normal")
    new_joke_btn.config(state="disabled")
    punchline_label.config(text="")


def show_punchline():
    punchline_label.config(text=current_joke[1])
    new_joke_btn.config(state="normal")
    punchline_btn.config(state="disabled")

root = tk.Tk()
root.title("Alexa: Tell Me a Joke")
root.geometry("500x400")
root.config(bg="#F0F4F8")

try:
    jokes = load_jokes("randomJokes.txt")
except FileNotFoundError:
    messagebox.showerror("Error", "randomJokes.txt not found!")
    root.destroy()
    exit()

tk.Label(root, text="😂 Alexa, Tell Me a Joke 😂", bg="#F0F4F8", fg="#333",
         font=("Helvetica", 18, "bold")).pack(pady=20)

joke_label = tk.Label(root, text="", wraplength=450, justify="center",
                      bg="#F0F4F8", fg="#222", font=("Helvetica", 16))
joke_label.pack(pady=30)

punchline_label = tk.Label(root, text="", wraplength=450, justify="center",
                           bg="#F0F4F8", fg="#D90429", font=("Helvetica", 15, "italic"))
punchline_label.pack(pady=10)

frame = tk.Frame(root, bg="#F0F4F8")
frame.pack(pady=30)

new_joke_btn = tk.Button(frame, text="Alexa, tell me a joke", command=show_setup,
                         bg="#0077B6", fg="white", font=("Helvetica", 12, "bold"),
                         activebackground="#023E8A", width=20, relief="flat")
new_joke_btn.grid(row=0, column=0, padx=10)

punchline_btn = tk.Button(frame, text="Show Punchline", command=show_punchline,
                          bg="#2B2D42", fg="white", font=("Helvetica", 12, "bold"),
                          activebackground="#8D99AE", width=20, relief="flat", state="disabled")
punchline_btn.grid(row=0, column=1, padx=10)

tk.Button(root, text="Exit", command=root.destroy,
          bg="#EF233C", fg="white", font=("Helvetica", 12, "bold"),
          activebackground="#D90429", relief="flat", width=10).pack(pady=10)

root.mainloop()
