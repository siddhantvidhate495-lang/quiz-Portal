import tkinter as tk
from dataclasses import dataclass
import random
import tkinter.messagebox
from queue import Queue  # <-- Queue imported

# ---------------- DATA STRUCTURE -----------------
@dataclass
class Question:
    question: str
    options: list
    answer: str

quiz_questions = [
    Question("What is the capital of India?", ["Delhi", "Mumbai", "Kolkata", "Chennai"], "Delhi"),
    Question("Largest ocean?", ["Indian", "Pacific", "Arctic", "Atlantic"], "Pacific")
]

# Queue for admin-added questions
admin_queue = Queue()

# ---------------- COLORS -----------------
BG_COLOR = "#f0f8ff"
PRIMARY_COLOR = "#4a6fa5"
SECONDARY_COLOR = "#6b5b95"
CORRECT_COLOR = "#50c878"
WRONG_COLOR = "#ff6b6b"
BUTTON_COLOR = "#dfe6fd"
TEXT_COLOR = "#2c3e50"

# ---------------- MAIN WINDOW -----------------
window = tk.Tk()
window.title("Quiz Portal")
window.geometry("900x650")
window.configure(bg=BG_COLOR)

# ---------------- VARIABLES -----------------
current_question_index = 0
user_score = 0
time_left = 15
timer_running = False
question_answered = False
timer_display = None

# ------------------- FRAMES -------------------
main_screen = tk.Frame(window, bg=BG_COLOR)
admin_screen = tk.Frame(window, bg=BG_COLOR)
quiz_screen = tk.Frame(window, bg=BG_COLOR)
result_screen = tk.Frame(window, bg=BG_COLOR)

# ------------------- CLEAR FRAME -------------------
def clear_frame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

# ------------------- MAIN MENU -------------------
def show_main_menu():
    hide_all_screens()
    clear_frame(main_screen)
    
    title = tk.Label(main_screen, text="Quiz Portal", font=("Arial", 32, "bold"), bg=BG_COLOR, fg=PRIMARY_COLOR)
    title.pack(pady=40)

    start_btn = tk.Button(main_screen, text="Start Quiz", font=("Arial", 22), width=20, bg=PRIMARY_COLOR, fg="white",
                         command=start_quiz)
    start_btn.pack(pady=20)

    admin_btn = tk.Button(main_screen, text="Admin Panel", font=("Arial", 22), width=20, bg=SECONDARY_COLOR, fg="white",
                          command=show_admin_panel)
    admin_btn.pack(pady=20)

    main_screen.pack(fill="both", expand=True)

# ------------------- HIDE ALL SCREENS -------------------
def hide_all_screens():
    for screen in [main_screen, admin_screen, quiz_screen, result_screen]:
        screen.pack_forget()

# ------------------- ADMIN PANEL -------------------
def show_admin_panel():
    hide_all_screens()
    clear_frame(admin_screen)
    
    tk.Label(admin_screen, text="Admin - Add New Question", font=("Arial", 26, "bold"), bg=BG_COLOR, fg=PRIMARY_COLOR).pack(pady=20)

    question_entry = tk.Entry(admin_screen, font=("Arial", 18), width=40)
    question_entry.insert(0, "Enter question")
    question_entry.pack(pady=10)

    option1_entry = tk.Entry(admin_screen, font=("Arial", 18), width=40)
    option1_entry.insert(0, "Option 1")
    option1_entry.pack(pady=10)

    option2_entry = tk.Entry(admin_screen, font=("Arial", 18), width=40)
    option2_entry.insert(0, "Option 2")
    option2_entry.pack(pady=10)

    option3_entry = tk.Entry(admin_screen, font=("Arial", 18), width=40)
    option3_entry.insert(0, "Option 3")
    option3_entry.pack(pady=10)

    option4_entry = tk.Entry(admin_screen, font=("Arial", 18), width=40)
    option4_entry.insert(0, "Option 4")
    option4_entry.pack(pady=10)

    answer_entry = tk.Entry(admin_screen, font=("Arial", 18), width=40)
    answer_entry.insert(0, "Correct Answer")
    answer_entry.pack(pady=10)

    # ------------------ ADD QUESTION TO QUEUE -------------------
    def add_question():
        new_question = question_entry.get()
        opt1 = option1_entry.get()
        opt2 = option2_entry.get()
        opt3 = option3_entry.get()
        opt4 = option4_entry.get()
        correct_ans = answer_entry.get()

        if not new_question or not opt1 or not opt2 or not opt3 or not opt4 or not correct_ans:
            tk.messagebox.showerror("Error", "Please fill all fields")
            return

        # Add question to the queue
        admin_queue.put(Question(new_question, [opt1, opt2, opt3, opt4], correct_ans))
        tk.messagebox.showinfo("Success", "Question queued successfully!")
        show_admin_panel()

    # ------------------ PROCESS QUEUE -------------------
    def process_queue():
        if admin_queue.empty():
            tk.messagebox.showinfo("Info", "No questions in queue.")
            return
        while not admin_queue.empty():
            quiz_questions.append(admin_queue.get())
        tk.messagebox.showinfo("Success", "All queued questions added to quiz!")

    tk.Button(admin_screen, text="Add Question", font=("Arial", 20), bg=CORRECT_COLOR, fg="white",
              command=add_question).pack(pady=20)

    tk.Button(admin_screen, text="Process Queued Questions", font=("Arial", 20), bg=SECONDARY_COLOR, fg="white",
              command=process_queue).pack(pady=10)

    tk.Button(admin_screen, text="Back", font=("Arial", 18), bg="#888", fg="white",
              command=show_main_menu).pack(pady=10)

    admin_screen.pack(fill="both", expand=True)

# ------------------ QUIZ FUNCTIONS -------------------
def start_quiz():
    hide_all_screens()
    global current_question_index, user_score, timer_running
    current_question_index = 0
    user_score = 0
    timer_running = False
    random.shuffle(quiz_questions)
    load_question()

def load_question():
    hide_all_screens()
    global time_left, timer_running, question_answered, timer_display
    
    timer_running = False
    clear_frame(quiz_screen)
    
    time_left = 15
    timer_running = True
    question_answered = False

    if current_question_index >= len(quiz_questions):
        show_result()
        return

    current_question = quiz_questions[current_question_index]

    timer_display = tk.Label(quiz_screen, text=f"Time Left: {time_left}", font=("Arial", 24), fg=WRONG_COLOR, bg=BG_COLOR)
    timer_display.pack(pady=10)

    question_number = tk.Label(quiz_screen, text=f"Question {current_question_index + 1}/{len(quiz_questions)}", 
                             font=("Arial", 18), bg=BG_COLOR, fg=TEXT_COLOR)
    question_number.pack(pady=5)

    tk.Label(quiz_screen, text=current_question.question, font=("Arial", 24), wraplength=800, 
             bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)

    options_frame = tk.Frame(quiz_screen, bg=BG_COLOR)
    options_frame.pack()

    for option in current_question.options:
        btn = tk.Button(options_frame, text=option, font=("Arial", 20), width=25, bg=BUTTON_COLOR, fg=TEXT_COLOR,
                       command=lambda opt=option: select_option(opt))
        btn.pack(pady=10)

    next_btn = tk.Button(quiz_screen, text="Next", font=("Arial", 20), bg=PRIMARY_COLOR, fg="white",
                        command=next_question)
    next_btn.pack(pady=30)

    quiz_screen.pack(fill="both", expand=True)
    update_timer()

def select_option(selected_option):
    global user_score, question_answered, timer_running
    
    if question_answered:
        return
        
    question_answered = True
    timer_running = False
    
    correct_answer = quiz_questions[current_question_index].answer
    
    # Color the buttons
    for widget in quiz_screen.winfo_children():
        if isinstance(widget, tk.Frame):
            for btn in widget.winfo_children():
                if btn.cget("text") == correct_answer:
                    btn.config(bg=CORRECT_COLOR, fg="white")
                elif btn.cget("text") == selected_option and selected_option != correct_answer:
                    btn.config(bg=WRONG_COLOR, fg="white")
                else:
                    btn.config(bg="#e0e0e0", fg=TEXT_COLOR)
                
    if selected_option == correct_answer:
        user_score += 1

def next_question():
    global current_question_index, timer_running
    timer_running = False
    current_question_index += 1
    load_question()

def update_timer():
    global time_left, timer_running
    if timer_running and time_left > 0:
        time_left -= 1
        timer_display.config(text=f"Time Left: {time_left}")
        window.after(1000, update_timer)
    elif timer_running and time_left <= 0:
        timer_running = False
        if not question_answered:
            next_question()

# ------------------ RESULT SCREEN -------------------
def show_result():
    hide_all_screens()
    global timer_running
    timer_running = False
    
    clear_frame(result_screen)
    
    tk.Label(result_screen, text="Quiz Finished!", font=("Arial", 32, "bold"), bg=BG_COLOR, fg=PRIMARY_COLOR).pack(pady=40)
    
    score_text = f"Your Score: {user_score} / {len(quiz_questions)}"
    tk.Label(result_screen, text=score_text, font=("Arial", 26), bg=BG_COLOR, fg=TEXT_COLOR).pack(pady=20)
    
    percentage = (user_score / len(quiz_questions)) * 100
    if percentage >= 80:
        performance = "Excellent!"
    elif percentage >= 60:
        performance = "Good job!"
    else:
        performance = "Keep practicing!"
        
    tk.Label(result_screen, text=performance, font=("Arial", 22), bg=BG_COLOR, fg=SECONDARY_COLOR).pack(pady=10)
    
    tk.Button(result_screen, text="Back to Home", font=("Arial", 22), bg=PRIMARY_COLOR, fg="white", 
              command=show_main_menu).pack(pady=30)

    result_screen.pack(fill="both", expand=True)

# ------------------ START APP -------------------
show_main_menu()
window.mainloop()
