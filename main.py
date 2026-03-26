
import tkinter as tk
import random
import matplotlib.pyplot as plt

# -------------------------------
# WINDOW
# -------------------------------
root = tk.Tk()
root.title("AI Focus System")
root.geometry("500x650")

bg = "#eef1f7"
accent = "#6C63FF"

root.configure(bg=bg)

# -------------------------------
# GLOBAL
# -------------------------------
level = 1
score = 0
numbers = []
difficulty = "easy"

answers = {}
q_index = 0

focus = 0
discipline = 0

# -------------------------------
# FRAME SYSTEM
# -------------------------------
frames = {}

def create_frame(name):
    frame = tk.Frame(root, bg=bg)
    frame.place(x=0, y=0, width=500, height=650)
    frames[name] = frame
    return frame

def show(name):
    frames[name].tkraise()

start_frame = create_frame("start")
difficulty_frame = create_frame("difficulty")
game_frame = create_frame("game")
question_frame = create_frame("question")
result_frame = create_frame("result")
loading_frame = create_frame("loading")


# -------------------------------
# START SCREEN 
# -------------------------------
header = tk.Label(start_frame,
    text="AI Focus & Habit Intelligence System",
    font=("Segoe UI", 20, "bold"),
    bg="#2d89ef",
    fg="white",
    padx=20, pady=15)

header.pack(fill="x")

card = tk.Frame(start_frame, bg="white", bd=2, relief="solid")
card.pack(pady=120, ipadx=40, ipady=30)


tk.Label(card,
         text="Welcome!",
         font=("Segoe UI", 14, "bold"),
         bg="white").pack(pady=10)

tk.Label(card,
         text="Train your focus and analyze your habits",
         bg="white").pack(pady=5)

tk.Button(card,
          text="Start",
          bg="#2d89ef",
          fg="white",
          command=lambda: show("difficulty")).pack(pady=20)


card = tk.Frame(start_frame, bg="white", bd=2, relief="solid")
card.pack(pady=120, ipadx=40, ipady=30)

def loading_screen():
    show("loading")

    for widget in loading_frame.winfo_children():
        widget.destroy()

    tk.Label(loading_frame,
        text="Analyzing your performance...",
        font=("Segoe UI", 16),
        bg=bg).pack(pady=150)

    root.after(2000, lambda: show("result"))

# -------------------------------
# DIFFICULTY
# -------------------------------
tk.Label(difficulty_frame, text="Select Difficulty",
         font=("Segoe UI", 14), bg=bg).pack(pady=40)

def set_difficulty(d):
    global difficulty
    difficulty = d
    start_game()

tk.Button(difficulty_frame, text="Easy",
          command=lambda: set_difficulty("easy")).pack(pady=10)

tk.Button(difficulty_frame, text="Medium",
          command=lambda: set_difficulty("medium")).pack(pady=10)

tk.Button(difficulty_frame, text="Hard",
          command=lambda: set_difficulty("hard")).pack(pady=10)

# -------------------------------
# GAME
# -------------------------------
sequence_label = tk.Label(game_frame, font=("Segoe UI", 16), bg=bg)
sequence_label.pack(pady=40)

entry = tk.Entry(game_frame)
entry.pack(pady=10)

def start_game():
    global level, score
    level = 1
    score = 0
    show("game")
    play_level()
    answers.clear()
    

def play_level():
    global numbers

    if difficulty == "easy":
        numbers = [str(random.randint(1, 9)) for _ in range(level + 3)]

    elif difficulty == "medium":
        numbers = [random.choice([
            str(random.randint(1, 9)),
            chr(random.randint(65, 90))
        ]) for _ in range(level + 4)]

    else:
        numbers = [str(random.randint(1, 9)) for _ in range(level + 6)]

    sequence_label.config(text=" ".join(numbers))

    if difficulty == "hard":
        root.after(2000, lambda: sequence_label.config(text="(Enter Reverse Order)"))
    else:
        root.after(2000, lambda: sequence_label.config(text=""))

def check():
    global level, score

    user = entry.get().split()
    correct_list = numbers[::-1] if difficulty == "hard" else numbers

    correct = sum(1 for i in range(len(correct_list))
                  if i < len(user) and user[i] == correct_list[i])

    score += correct
    entry.delete(0, tk.END)

    if level < 3:
        level += 1
        play_level()
    else:
        global q_index
        q_index = 0   

        show("question")
        load_question()
        print("Score:", score)

tk.Button(game_frame, text="Submit", command=check).pack()

# -------------------------------
# QUESTIONS
# -------------------------------
q_label = tk.Label(question_frame,
                   font=("Segoe UI", 14),
                   bg=bg)
q_label.pack(pady=60)

slider = tk.Scale(question_frame,
                  orient="horizontal",
                  length=300)
slider.pack()

questions = [
    ("Study hours?", "study", 0, 10),
    ("Sleep hours?", "sleep", 0, 12),
    ("Phone usage?", "phone", 0, 24),
    ("Exercise minutes?", "exercise", 0, 180)
]

def load_question():
    global q_index

    if q_index < len(questions):
        q, key, mn, mx = questions[q_index]
        q_label.config(text=q)
        slider.config(from_=mn, to=mx)
    else:
        analyze()

def next_question():
    global q_index
    answers[questions[q_index][1]] = slider.get()
    q_index += 1
    load_question()

tk.Button(question_frame, text="Next",
          command=next_question).pack(pady=20)

# -------------------------------
# RESULT
# -------------------------------
def analyze():
    global focus, discipline

    show("result")

    for w in result_frame.winfo_children():
        w.destroy()

    study = answers.get("study", 0)
    sleep = answers.get("sleep", 0)
    phone = answers.get("phone", 0)
    exercise = answers.get("exercise", 0)

        
    discipline = 0

    if study >= 6:
        discipline += 3
    elif study >= 3:
        discipline += 2
    else:
        discipline += 1

    if sleep >= 7:
        discipline += 3
    elif sleep >= 5:
        discipline += 2
    else:
        discipline += 1

    if phone <= 4:
        discipline += 3
    elif phone <= 8:
        discipline += 2
    else:
        discipline += 1

    if exercise >= 60:
        discipline += 4
    elif exercise >= 30:
        discipline += 3
    elif exercise >= 10:
        dicipline  += 2
    else:
        discipline += 1

    # SCALE score to 10 
    scaled_score = min(score, 10)

    focus = int((scaled_score * 0.7) + (discipline * 0.3))
    focus = max(0, min(focus, 10))    

    # CARD
    card = tk.Frame(result_frame, bg="white", bd=2, relief="solid")
    card.place(relx=0.5, rely=0.5, anchor="center", width=380, height=400)

    tk.Label(card, text="AI ANALYSIS",
             font=("Segoe UI", 18, "bold"),
             bg="white").pack(pady=15)

    tk.Label(card,
             text=f"Focus: {focus} | Discipline: {discipline}",
             font=("Segoe UI", 12),
             bg="white").pack(pady=10)

    # Feedback
    fb = "✔ Good Focus" if focus >= 7 else "✘ Improve Focus"

    tk.Label(card, text=fb,
             bg="white",
             relief="solid",
             bd=1,
             padx=10, pady=5).pack(pady=10)

    # Suggestions
    suggestions = []
    if study < 5: suggestions.append("• Study more")
    if sleep < 6: suggestions.append("• Improve sleep")
    if phone > 5: suggestions.append("• Reduce phone usage")
    if exercise < 10: suggestions.append("• Exercise daily")

    if not suggestions:
        suggestions.append("• Excellent routine")

    tk.Label(card,
             text="\n".join(suggestions),
             bg="#eaf7ea",
             relief="solid",
             bd=1,
             padx=10, pady=5).pack(pady=10)

    # Buttons
    btn_frame = tk.Frame(card, bg="white")
    btn_frame.pack(pady=10)

    tk.Button(btn_frame, text="Graph",
              command=show_graph).pack(side="left", padx=10)

    tk.Button(btn_frame, text="Back",
              command=lambda: show("start")).pack(side="right", padx=10)

# -------------------------------
# GRAPH
# -------------------------------
def show_graph():
    plt.bar(["Focus", "Discipline"], [focus, discipline])
    plt.title("Performance")
    plt.show()

# -------------------------------
# START
# -------------------------------
show("start")
root.mainloop()
