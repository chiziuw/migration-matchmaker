import tkinter as tk
from tkinter import ttk
import csv

all_locations = []

# 1. OOP CLASSES
class Location:
    def __init__(self, name, state, density, rent, industry):
        self.name = name
        self.state = state
        self.density = density
        self.rent = int(rent)
        self.industry = industry

    def is_affordable(self, user_budget):
        if self.rent <= user_budget:
            return True
        return False
class UserProfile:
    def __init__(self, budget, industry, density_pref):
        self.budget = int(budget)
        self.industry = industry
        self.density_pref = density_pref

    def is_valid(self):
        if self.budget > 0 and self.industry != "" and self.density_pref != "":
            return True
        return False


# 2. DATA HANDLING
def load_locations(filename):
    locations_list = []
    try:
        with open(filename, mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                if len(row) == 5:
                    new_loc = Location(row[0], row[1], row[2], row[3], row[4])
                    locations_list.append(new_loc)
            print("Success: Database loaded.")
    except FileNotFoundError:
        print(f"Error: Could not find {filename}")
    return locations_list
# 3. MATCHING ALGORITHM
def calculate_best_match(user, locations_data):
    valid_matches = []
    for loc in locations_data:
        score = 0
        if loc.is_affordable(user.budget):
            if loc.industry == user.industry:
                score += 2 
            if loc.density == user.density_pref:
                score += 1 
            valid_matches.append((score, loc))
            
    valid_matches.sort(key=lambda x: x[0], reverse=True)
    return valid_matches[:2]  
# 4. ADVANCED GUI: DASHBOARD SETUP
window = tk.Tk()
window.tittle("Migration Matchmaker")
window.geometry("750x500")
window.configure(bg="#F8FAFC")
#HOVER ANIMATION FUNCTIONS
def on_enter(e):
    e.widget['backgroun'] = '#2563eb'
def on_level(e):
    e.widget['background'] ='#3b82f6'

#SIDEBAR
sidebar = tk.Frame(window, bg="#1e293b", width=200)
sidebar.pack(side="left", fill="y")
sidebar.pack_propagate(False)
tk.Label(sidebar, text ="📍", font=("Helvetica", 40), bg="#1E293B", fg="white").pack(pady=(30, 0))
tk.Label(sidebar, text="Migration\nMatchmaker", font=("Helvetica", 16, "bold"), bg="#1E293B", fg="white").pack(pady=(10, 30))
tk.Label(sidebar, text="🟢 System Online", font=("Helvetica", 10), bg="#1E293B", fg="#4ADE80").pack(side="bottom", pady=20)

# MAIN CONTENT AREA
main_content = tk.Frame(window, bg="#F8FAFC")
main_content.pack(side="right", fill="both", expand=True)

screens = {}

def show_screen(screen_name):
    for frame in screens.values():
        frame.pack_forget()
    screens[screen_name].pack(fill="both", expand=True)

screens["Welcome"] = tk.Frame(main_content, bg="#F8FAFC")
screens["Questionnaire"] = tk.Frame(main_content, bg="#F8FAFC")
screens["Loading"] = tk.Frame(main_content, bg="#F8FAFC")
screens["Results"] = tk.Frame(main_content, bg="#F8FAFC")  