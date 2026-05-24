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

# HOVER ANIMATION FUNCTIONS
def on_enter(e):
    e.widget['backgroun'] = '#2563eb'
def on_level(e):
    e.widget['background'] ='#3b82f6'

# SIDEBAR
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

# SCREEN 1: WELCOME
tk.Label(screens["Welcome"], text="Find Your Perfect City!", font=("Helvetica", 24, "bold"), bg="#F8FAFC", fg="#0F172A").pack(pady=(80, 10))
tk.Label(screens["Welcome"], text="Answer some questions and we'll analyze all 36 states\nacross Nigeria to find your most optimal destination.", font=("Helvetica", 13), bg="#F8FAFC", fg="#64748B", justify="center").pack(pady=10)

start_button = tk.Button(screens["Welcome"], text="Launch Analysis", font=("Helvetica", 12, "bold"), bg="#3B82F6", fg="white", bd=0, padx=20, pady=10, cursor="hand2", command=lambda: show_screen("Questionnaire"))
start_button.pack(pady=40)
start_button.bind("<Enter>", on_enter)
start_button.bind("<Leave>", on_leave)

# SCREEN 2: QUESTIONNAIRE
tk.Label(screens["Questionnaire"], text="Enter Your Information", font=("Helvetica", 20, "bold"), bg="#F8FAFC", fg="#0F172A").pack(pady=(40, 20))

card = tk.Frame(screens["Questionnaire"], bg="white", padx=40, pady=30, relief="flat")
card.pack()

tk.Label(card, text="Max Monthly Rent (₦):", font=("Helvetica", 11, "bold"), bg="white", fg="#334155").pack(anchor="w")
budget_entry = ttk.Entry(card, font=("Helvetica", 12), width=30)
budget_entry.pack(pady=(5, 15))

tk.Label(card, text="Target Industry:", font=("Helvetica", 11, "bold"), bg="white", fg="#334155").pack(anchor="w")
industry_dropdown = ttk.Combobox(card, values=["Agriculture", "Education", "Tourism", "Tech", "Manufacturing"], font=("Helvetica", 12), width=28, state="readonly")
industry_dropdown.pack(pady=(5, 15))

tk.Label(card, text="Preferred Density:", font=("Helvetica", 11, "bold"), bg="white", fg="#334155").pack(anchor="w")
density_dropdown = ttk.Combobox(card, values=["Low", "Medium"], font=("Helvetica", 12), width=28, state="readonly")
density_dropdown.pack(pady=(5, 20))

# SCREEN 3: LOADING SCREEN
tk.Label(screens["Loading"], text="⚙️ Processing Data...", font=("Helvetica", 18, "bold"), bg="#F8FAFC", fg="#0F172A").pack(pady=(150, 20))
progress_bar = ttk.Progressbar(screens["Loading"], orient="horizontal", length=300, mode="determinate")
progress_bar.pack()
loading_text = tk.Label(screens["Loading"], text="Scanning the country...", font=("Helvetica", 10), bg="#F8FAFC", fg="#64748B")
loading_text.pack(pady=10)

# SCREEN 4: RESULTS
tk.Label(screens["Results"], text="Top Results", font=("Helvetica", 22, "bold"), bg="#F8FAFC", fg="#0F172A").pack(pady=(40, 15))
result_text = tk.StringVar()
result_display = tk.Label(screens["Results"], text="", textvariable=result_text, font=("Helvetica", 13), bg="#F8FAFC", fg="#334155", justify="left")
result_display.pack(pady=10)

def reset_and_restart():
    budget_entry.delete(0, tk.END)
    industry_dropdown.set('')
    density_dropdown.set('')
    show_screen("Welcome")

restart_button = tk.Button(screens["Results"], text="← Search Again", font=("Helvetica", 11, "bold"), bg="#64748B", fg="white", bd=0, padx=15, pady=8, cursor="hand2", command=reset_and_restart)
restart_button.pack(pady=30)

# 5. INTEGRATION LOGIC & ANIMATION
def calculate_and_display(user):
    matches = calculate_best_match(user, all_locations)
    if len(matches) == 0:
        result_text.set("❌ No affordable locations found.\nIncrease your budget and try again.")
    else:
        output_string = ""
        for index, match in enumerate(matches):
            loc = match[1] 
            output_string += f"🏆 Rank {index + 1}: {loc.name}, {loc.state} State\n"
            output_string += f"   💰 Est. Rent: ₦{loc.rent:,}\n"
            output_string += f"   🏢 Industry: {loc.industry}  |  📊 Density: {loc.density}\n\n"
        result_text.set(output_string)
    show_screen("Results")

def trigger_loading_screen():
    try:
        budget_val = budget_entry.get().strip()
        if not budget_val:
            result_text.set("⚠️ Error: Please enter a budget.")
            show_screen("Results")
            return
            
        budget = int(budget_val)
        industry = industry_dropdown.get()
        density = density_dropdown.get()
        
        user = UserProfile(budget, industry, density)
        if not user.is_valid():
            result_text.set("⚠️ Error: Please select an option from all menus.")
            show_screen("Results")
            return

        show_screen("Loading")
        progress_bar['value'] = 0
        for i in range(101):
            window.after(i * 15, lambda val=i: progress_bar.configure(value=val))
            
        window.after(1600, lambda: calculate_and_display(user))
        
    except ValueError:
        result_text.set("⚠️ Error: Budget must be a valid number.")
        show_screen("Results")

submit_btn = tk.Button(card, text="Analyze Matches", font=("Helvetica", 12, "bold"), bg="#3B82F6", fg="white", bd=0, padx=20, pady=10, cursor="hand2", command=trigger_loading_screen)
submit_btn.pack(pady=10)
submit_btn.bind("<Enter>", on_enter)
submit_btn.bind("<Leave>", on_leave)

# 6. RUN THE APP
all_locations = load_locations("locations_data.csv")
show_screen("Welcome")
window.mainloop()