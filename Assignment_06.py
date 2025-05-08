import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd

# Rules for evaluation
rules = {
    "rule1": ("Meets all project deadlines", 20),
    "rule2": ("Exceeds expectations", 30),
    "rule3": ("Shows initiative and takes on additional responsibilities", 15),
    "rule4": ("Collaborates well in a team", 10),
    "rule5": ("Is always punctual", 10),
    "rule6": ("Receives positive client feedback", 15),
    "rule7": ("Brings new ideas and innovations", 20),
    "rule8": ("Frequently absent or misses deadlines", -25),
    "rule9": ("Consistently performs below expectations", -35)
}

def evaluate_employee():
    try:
        name = entry_name.get()
        position = entry_position.get()
        work_mode = work_mode_var.get()
        experience = entry_experience.get()
        if not name or not position or not experience:
            raise ValueError("Please enter all employee details.")
        
        # Get manager assessment
        score = sum(var.get() * points for (desc, points), var in zip(rules.values(), manager_vars))
        
        # Performance rating & Recommendations
        if score >= 80:
            rating = "Excellent"
            recommendation = "Highly recommended for promotion and incentive increment."
            improvement_suggestion = "Keep up the great work and consider mentoring junior employees."
        elif score >= 60:
            rating = "Good"
            recommendation = "Eligible for incentives; potential for promotion with continued improvement."
            improvement_suggestion = "Work on leadership and strategic thinking to strengthen promotion chances."
        elif score >= 40:
            rating = "Average"
            recommendation = "No immediate promotion; requires improvement in key areas."
            improvement_suggestion = "Focus on teamwork, punctuality, and exceeding expectations."
        else:
            rating = "Needs Improvement"
            recommendation = "Possible risk of demotion or performance review required."
            improvement_suggestion = "Improve consistency, time management, and client interactions."
        
        feedback_text = feedback_entry.get("1.0", tk.END).strip()
        
        result_text = (f"Employee: {name}\nPosition: {position}\nExperience: {experience} years\nWork Mode: {work_mode}\n"
                      f"Final Score: {score}\nPerformance Rating: {rating}\n\nRecommendation: {recommendation}\n"
                      f"Improvement Suggestions: {improvement_suggestion}\n\nManager Feedback: {feedback_text}")
        messagebox.showinfo("Performance Evaluation", result_text)
        
        # Save to history
        save_to_history(name, position, work_mode, experience, score, rating, recommendation, feedback_text)
        
    except ValueError as e:
        messagebox.showerror("Input Error", str(e))

def save_to_history(name, position, work_mode, experience, score, rating, recommendation, feedback):
    data = {"Employee Name": [name], "Position": [position], "Work Mode": [work_mode], "Experience": [experience],
            "Score": [score], "Rating": [rating], "Recommendation": [recommendation], "Feedback": [feedback]}
    df = pd.DataFrame(data)
    try:
        existing_df = pd.read_csv("performance_history.csv")
        df = pd.concat([existing_df, df], ignore_index=True)
    except FileNotFoundError:
        pass
    df.to_csv("performance_history.csv", index=False)

def export_to_excel():
    try:
        df = pd.read_csv("performance_history.csv")
        file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", 
                                                 filetypes=[("Excel Files", "*.xlsx")])
        if file_path:
            df.to_excel(file_path, index=False, engine="openpyxl")
            messagebox.showinfo("Export Successful", "Performance report saved successfully.")
    except FileNotFoundError:
        messagebox.showerror("Error", "No performance history found. Evaluate an employee first!")


# Create GUI window
root = tk.Tk()
root.title("Employee Performance Evaluation")
root.geometry("800x800")

tk.Label(root, text="Employee Name:").pack()
entry_name = tk.Entry(root)
entry_name.pack()

tk.Label(root, text="Current Position:").pack()
entry_position = tk.Entry(root)
entry_position.pack()

tk.Label(root, text="Years of Experience:").pack()
entry_experience = tk.Entry(root)
entry_experience.pack()

tk.Label(root, text="Work Mode:").pack()
work_mode_var = tk.StringVar(value="Hybrid")
tk.OptionMenu(root, work_mode_var, "Remote", "On-Site", "Hybrid").pack()

# Manager assessment
manager_vars = [tk.IntVar() for _ in rules]
tk.Label(root, text="Manager's Review", font=("Arial", 12, "bold")).pack()
frame = tk.Frame(root)
frame.pack()
for (desc, _), var in zip(rules.values(), manager_vars):
    tk.Checkbutton(frame, text=desc, variable=var).pack(anchor="w")

# Feedback Section
tk.Label(root, text="Manager's Feedback:", font=("Arial", 12, "bold")).pack()
feedback_entry = tk.Text(root, height=3, width=40)
feedback_entry.pack()

# Evaluate & Export Buttons
tk.Button(root, text="Evaluate Performance", command=evaluate_employee).pack(pady=5)
tk.Button(root, text="Export Report (Excel)", command=export_to_excel).pack(pady=5)

# Run the GUI
root.mainloop()