import tkinter as tk
from tkinter import messagebox, simpledialog, ttk


def load_students():
    students = []
    try:
        with open("studentMarks.txt", "r") as f:
            lines = [line.strip() for line in f.readlines() if line.strip()]
            n = int(lines[0])
            for line in lines[1:]:
                parts = [p.strip() for p in line.split(",")]
                code = int(parts[0])
                name = parts[1]
                marks = list(map(int, parts[2:5]))
                exam = int(parts[5])
                students.append({
                    "code": code,
                    "name": name,
                    "cw1": marks[0],
                    "cw2": marks[1],
                    "cw3": marks[2],
                    "exam": exam
                })
        return students
    except Exception as e:
        messagebox.showerror("Error", f"Error loading student data:\n{e}")
        return []

def save_students(students):
    with open("studentMarks.txt", "w") as f:
        f.write(str(len(students)) + "\n")
        for s in students:
            line = f"{s['code']}, {s['name']}, {s['cw1']},{s['cw2']},{s['cw3']},{s['exam']}\n"
            f.write(line)

def calc_total(s):
    return s["cw1"] + s["cw2"] + s["cw3"]

def calc_percentage(s):
    total = calc_total(s) + s["exam"]
    return (total / 160) * 100

def calc_grade(percent):
    if percent >= 70: return "A"
    elif percent >= 60: return "B"
    elif percent >= 50: return "C"
    elif percent >= 40: return "D"
    else: return "F"

def format_student(s):
    total = calc_total(s)
    percent = calc_percentage(s)
    grade = calc_grade(percent)
    return (f"Name: {s['name']}\n"
            f"Student Number: {s['code']}\n"
            f"Coursework Total: {total}/60\n"
            f"Exam Mark: {s['exam']}/100\n"
            f"Overall %: {percent:.2f}%\n"
            f"Grade: {grade}\n"
            "----------------------------\n")


def view_all():
    students = load_students()
    if not students: return
    output = ""
    total_percent = 0
    for s in students:
        output += format_student(s)
        total_percent += calc_percentage(s)
    avg = total_percent / len(students)
    output += f"\nTotal Students: {len(students)}\nAverage %: {avg:.2f}%"
    update_text(output)

def view_individual():
    students = load_students()
    if not students: return
    selected = simpledialog.askstring("Student Search", "Enter student name or code:")
    if not selected: return
    found = None
    for s in students:
        if selected.lower() in s["name"].lower() or selected == str(s["code"]):
            found = s
            break
    if found:
        update_text(format_student(found))
    else:
        update_text("Student not found.")

def show_highest():
    students = load_students()
    if not students: return
    best = max(students, key=calc_percentage)
    update_text("Top Student:\n\n" + format_student(best))

def show_lowest():
    students = load_students()
    if not students: return
    worst = min(students, key=calc_percentage)
    update_text("Lowest Scoring Student:\n\n" + format_student(worst))


def sort_students():
    students = load_students()
    if not students: return
    order = messagebox.askquestion("Sort Order", "Sort in ascending order?\n(Click 'No' for descending)")
    students.sort(key=calc_percentage, reverse=(order == "no"))
    output = ""
    for s in students:
        output += format_student(s)
    update_text(output)

def add_student():
    students = load_students()
    code = simpledialog.askinteger("Add Student", "Enter student code (1000-9999):")
    name = simpledialog.askstring("Add Student", "Enter student name:")
    cw1 = simpledialog.askinteger("Add Student", "Enter coursework mark 1 (out of 20):")
    cw2 = simpledialog.askinteger("Add Student", "Enter coursework mark 2 (out of 20):")
    cw3 = simpledialog.askinteger("Add Student", "Enter coursework mark 3 (out of 20):")
    exam = simpledialog.askinteger("Add Student", "Enter exam mark (out of 100):")
    if not all([code, name, cw1, cw2, cw3, exam]):
        messagebox.showwarning("Invalid", "All fields are required.")
        return
    students.append({"code": code, "name": name, "cw1": cw1, "cw2": cw2, "cw3": cw3, "exam": exam})
    save_students(students)
    messagebox.showinfo("Success", "Student added successfully!")

def delete_student():
    students = load_students()
    if not students: return
    target = simpledialog.askstring("Delete Student", "Enter name or student code:")
    found = None
    for s in students:
        if target.lower() in s["name"].lower() or target == str(s["code"]):
            found = s
            break
    if found:
        students.remove(found)
        save_students(students)
        messagebox.showinfo("Deleted", f"Student '{found['name']}' deleted.")
    else:
        messagebox.showwarning("Not Found", "No matching student found.")

def update_student():
    students = load_students()
    target = simpledialog.askstring("Update Student", "Enter name or student code:")
    found = None
    for s in students:
        if target.lower() in s["name"].lower() or target == str(s["code"]):
            found = s
            break
    if not found:
        messagebox.showwarning("Not Found", "Student not found.")
        return
    field = simpledialog.askstring("Update Field", "Enter field to update (name, cw1, cw2, cw3, exam):")
    if not field or field not in ["name", "cw1", "cw2", "cw3", "exam"]:
        messagebox.showwarning("Invalid", "Invalid field.")
        return
    new_value = simpledialog.askstring("New Value", f"Enter new value for {field}:")
    if field.startswith("cw") or field == "exam":
        new_value = int(new_value)
    found[field] = new_value
    save_students(students)
    messagebox.showinfo("Updated", f"{found['name']}'s record updated successfully!")

def update_text(content):
    text_box.config(state="normal")
    text_box.delete(1.0, tk.END)
    text_box.insert(tk.END, content)
    text_box.config(state="disabled")

root = tk.Tk()
root.title("🎓 Student Manager")
root.geometry("800x600")
root.configure(bg="#f0f4f8")

title = tk.Label(root, text="Student Manager Dashboard", font=("Helvetica", 20, "bold"), bg="#f0f4f8", fg="#333")
title.pack(pady=10)

button_frame = tk.Frame(root, bg="#f0f4f8")
button_frame.pack(pady=10)

buttons = [
    ("View All Records", view_all, "#0077B6"),
    ("View Individual Record", view_individual, "#023E8A"),
    ("Show Highest Score", show_highest, "#0096C7"),
    ("Show Lowest Score", show_lowest, "#00B4D8"),
    ("Sort Records", sort_students, "#48CAE4"),
    ("Add Student", add_student, "#90E0EF"),
    ("Delete Student", delete_student, "#CAF0F8"),
    ("Update Student", update_student, "#ADE8F4")
]

for i, (text, cmd, color) in enumerate(buttons):
    b = tk.Button(button_frame, text=text, command=cmd, bg=color, fg="#fff",
                  font=("Helvetica", 12, "bold"), width=20, height=2, relief="flat")
    b.grid(row=i//2, column=i%2, padx=10, pady=6)

text_box = tk.Text(root, height=20, width=90, wrap=tk.WORD, bg="#fff", fg="#222", font=("Consolas", 11))
text_box.pack(pady=15)
text_box.config(state="disabled")

root.mainloop()

