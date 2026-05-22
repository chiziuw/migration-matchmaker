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