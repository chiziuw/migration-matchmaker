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
    