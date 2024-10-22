# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl

# class NPKComplexFertilizerCalculator:
#     def __init__(self, crop_name, soil_n, soil_p, soil_k):
#         self.crop_name = crop_name  # Name of the crop
#         self.soil_n = soil_n  # Current Nitrogen level (kg/ha)
#         self.soil_p = soil_p  # Current Phosphorus level (kg/ha)
#         self.soil_k = soil_k  # Current Potassium level (kg/ha)

#         # Updated Recommended NPK needs based on Suru sugarcane
#         self.crop_n_needs = 170  # Recommended Nitrogen (kg/ha)
#         self.crop_p_needs = 85   # Recommended Phosphorus (kg/ha)
#         self.crop_k_needs = 85   # Recommended Potassium (kg/ha)

#         # Initialize fuzzy variables
#         self._initialize_fuzzy_system()

#         # Updated growth stages for Suru sugarcane
#         self.growth_stages = {
#             "Germination": {"days": (0, 40), "NPK": (20, 10, 10)},
#             "Tillering": {"days": (41, 135), "NPK": (30, 20, 20)},
#             "Grand Growth": {"days": (136, 300), "NPK": (40, 35, 35)},
#             "Maturity": {"days": (301, 360), "NPK": (20, 15, 15)},
#             "Harvesting": {"days": (360, 400), "NPK": (10, 5, 5)}
#         }

#         # NPK complex fertilizers and individual fertilizers
#         self.fertilizers = {
#             "10:26:26": {"N": 0.10, "P": 0.26, "K": 0.26},
#             "12:32:16": {"N": 0.12, "P": 0.32, "K": 0.16},
#             "15:15:15": {"N": 0.15, "P": 0.15, "K": 0.15},
#             "Urea (46-0-0)": {"N": 0.46, "P": 0.0, "K": 0.0},
#             "DAP (18-46-0)": {"N": 0.18, "P": 0.46, "K": 0.0},
#             "MOP (0-0-60)": {"N": 0.0, "P": 0.0, "K": 0.60},
#             "Ammonium Sulfate (21-0-0)": {"N": 0.21, "P": 0.0, "K": 0.0},
#             "CAN (26-0-0)": {"N": 0.26, "P": 0.0, "K": 0.0},
#             "SSP (0-16-0)": {"N": 0.0, "P": 0.16, "K": 0.0},
#             "TSP (0-44-0)": {"N": 0.0, "P": 0.44, "K": 0.0},
#             "SOP (0-0-50)": {"N": 0.0, "P": 0.0, "K": 0.50},
#         }

#     def _initialize_fuzzy_system(self):
#         # Define fuzzy variables
#         self.n_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'n_needed')
#         self.p_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'p_needed')
#         self.k_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'k_needed')

#         self.n_fertilizer = ctrl.Consequent(np.arange(0, 131, 1), 'n_fertilizer')
#         self.p_fertilizer = ctrl.Consequent(np.arange(0, 101, 1), 'p_fertilizer')
#         self.k_fertilizer = ctrl.Consequent(np.arange(0, 51, 1), 'k_fertilizer')

#         # Membership functions for inputs (N, P, K needs)
#         self.n_needed['low'] = fuzz.trimf(self.n_needed.universe, [0, 0, 100])
#         self.n_needed['medium'] = fuzz.trimf(self.n_needed.universe, [50, 100, 150])
#         self.n_needed['high'] = fuzz.trimf(self.n_needed.universe, [100, 200, 200])

#         self.p_needed['low'] = fuzz.trimf(self.p_needed.universe, [0, 0, 50])
#         self.p_needed['medium'] = fuzz.trimf(self.p_needed.universe, [25, 50, 75])
#         self.p_needed['high'] = fuzz.trimf(self.p_needed.universe, [50, 100, 100])

#         self.k_needed['low'] = fuzz.trimf(self.k_needed.universe, [0, 0, 50])
#         self.k_needed['medium'] = fuzz.trimf(self.k_needed.universe, [25, 40, 50])
#         self.k_needed['high'] = fuzz.trimf(self.k_needed.universe, [40, 50, 50])

#         # Define membership functions for outputs
#         self.n_fertilizer['low'] = fuzz.trimf(self.n_fertilizer.universe, [0, 0, 65])
#         self.n_fertilizer['medium'] = fuzz.trimf(self.n_fertilizer.universe, [30, 65, 100])
#         self.n_fertilizer['high'] = fuzz.trimf(self.n_fertilizer.universe, [65, 130, 130])

#         self.p_fertilizer['low'] = fuzz.trimf(self.p_fertilizer.universe, [0, 0, 30])
#         self.p_fertilizer['medium'] = fuzz.trimf(self.p_fertilizer.universe, [15, 30, 60])
#         self.p_fertilizer['high'] = fuzz.trimf(self.p_fertilizer.universe, [30, 100, 100])

#         self.k_fertilizer['low'] = fuzz.trimf(self.k_fertilizer.universe, [0, 0, 25])
#         self.k_fertilizer['medium'] = fuzz.trimf(self.k_fertilizer.universe, [10, 25, 30])
#         self.k_fertilizer['high'] = fuzz.trimf(self.k_fertilizer.universe, [25, 50, 50])

#         # Define fuzzy rules
#         self.rules = [
#             ctrl.Rule(self.n_needed['low'] & self.p_needed['low'] & self.k_needed['low'],
#                       (self.n_fertilizer['high'], self.p_fertilizer['high'], self.k_fertilizer['high'])),
#             ctrl.Rule(self.n_needed['medium'] & self.p_needed['medium'] & self.k_needed['medium'],
#                       (self.n_fertilizer['medium'], self.p_fertilizer['medium'], self.k_fertilizer['medium'])),
#             ctrl.Rule(self.n_needed['high'] & self.p_needed['high'] & self.k_needed['high'],
#                       (self.n_fertilizer['low'], self.p_fertilizer['low'], self.k_fertilizer['low'])),
#             ctrl.Rule(self.n_needed['low'] & self.p_needed['high'] & self.k_needed['medium'],
#                       (self.n_fertilizer['high'], self.p_fertilizer['medium'], self.k_fertilizer['low'])),
#         ]

#         # Create control system
#         self.fertilizer_ctrl = ctrl.ControlSystem(self.rules)
#         self.fertilizer_sim = ctrl.ControlSystemSimulation(self.fertilizer_ctrl)

#     def fuzzy_logic(self, growth_stage):
#         # Get NPK needs based on growth stage
#         n_needed_target, p_needed_target, k_needed_target = self.get_npk_needs(growth_stage)

#         # Fuzzy logic to calculate fertilizer required
#         n_needed = max(0, n_needed_target - self.soil_n)
#         p_needed = max(0, p_needed_target - self.soil_p)
#         k_needed = max(0, k_needed_target - self.soil_k)

#         # Set inputs to the fuzzy logic system
#         self.fertilizer_sim.input['n_needed'] = n_needed
#         self.fertilizer_sim.input['p_needed'] = p_needed
#         self.fertilizer_sim.input['k_needed'] = k_needed

#         # Compute the fuzzy logic output
#         self.fertilizer_sim.compute()

#         # Get the fertilizer amounts needed
#         n_fertilizer_needed = self.fertilizer_sim.output['n_fertilizer']
#         p_fertilizer_needed = self.fertilizer_sim.output['p_fertilizer']
#         k_fertilizer_needed = self.fertilizer_sim.output['k_fertilizer']

#         return n_fertilizer_needed, p_fertilizer_needed, k_fertilizer_needed

#     def get_npk_needs(self, growth_stage):
#         # Get the NPK needs based on the growth stage
#         return self.growth_stages[growth_stage]['NPK']

#     def calculate_fertilizer_amounts(self, n_fertilizer_needed, p_fertilizer_needed, k_fertilizer_needed):
#         # Calculate the amount of each fertilizer needed while considering interactions
#         amounts = {}
#         total_n_applied = total_p_applied = total_k_applied = 0

#         for fertilizer, nutrients in self.fertilizers.items():
#             n_content = nutrients["N"]
#             p_content = nutrients["P"]
#             k_content = nutrients["K"]

#             # Adjust remaining needs by subtracting already applied nutrients
#             n_needed_remaining = max(0, n_fertilizer_needed - total_n_applied)
#             p_needed_remaining = max(0, p_fertilizer_needed - total_p_applied)
#             k_needed_remaining = max(0, k_fertilizer_needed - total_k_applied)

#             # Calculate how much of the current fertilizer is required
#             n_amount = n_needed_remaining / n_content if n_content > 0 else 0
#             p_amount = p_needed_remaining / p_content if p_content > 0 else 0
#             k_amount = k_needed_remaining / k_content if k_content > 0 else 0

#             # Use the maximum amount required based on N, P, or K content
#             amount_to_apply = max(n_amount, p_amount, k_amount)
#             amounts[fertilizer] = amount_to_apply

#             # Update the total applied nutrients
#             total_n_applied += amount_to_apply * n_content
#             total_p_applied += amount_to_apply * p_content
#             total_k_applied += amount_to_apply * k_content

#         return amounts

#     def display_fertilizer_plan(self):
#         # Initialize a list to store fertilizer plans for each growth stage
#         fertilizer_plan_list = []
    
#         print(f"\nFertilizer plan for {self.crop_name}:")
#         for phase, stage_data in self.growth_stages.items():
#             # Get fertilizer amounts using fuzzy logic
#             n_fertilizer, p_fertilizer, k_fertilizer = self.fuzzy_logic(phase)
#             fertilizer_amounts = self.calculate_fertilizer_amounts(n_fertilizer, p_fertilizer, k_fertilizer)
    
#             # Display the data
#             print(f"{phase} (Days: {stage_data['days'][0]} to {stage_data['days'][1]}):")
#             print(f"  N fertilizer needed: {n_fertilizer:.2f} kg/ha")
#             print(f"  P fertilizer needed: {p_fertilizer:.2f} kg/ha")
#             print(f"  K fertilizer needed: {k_fertilizer:.2f} kg/ha")
    
#             for fertilizer, amount in fertilizer_amounts.items():
#                 print(f"    {fertilizer}: {amount:.2f} kg/ha")
    
#             print()
    
#             # Store the data for this phase in a dictionary
#             phase_data = {
#                 'phase': phase,
#                 'days': stage_data['days'],
#                 'n_fertilizer_needed': n_fertilizer,
#                 'p_fertilizer_needed': p_fertilizer,
#                 'k_fertilizer_needed': k_fertilizer,
#                 'specific_fertilizer_amounts': fertilizer_amounts  # Dictionary with the specific fertilizer amounts
#             }
    
#             # Append the dictionary to the list
#             fertilizer_plan_list.append(phase_data)
    
#         # Return the list containing all phases' data
#         return fertilizer_plan_list
#       # Blank line for readability

# # Example usage
# calculator = NPKComplexFertilizerCalculator(crop_name="Sugarcane", soil_n=50, soil_p=20, soil_k=30)
# calculator.display_fertilizer_plan()


# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl

# class NPKComplexFertilizerCalculator:
#     def __init__(self, crop_name, soil_n, soil_p, soil_k):
#         self.crop_name = crop_name
#         self.soil_n = soil_n
#         self.soil_p = soil_p
#         self.soil_k = soil_k

#         # Updated Recommended NPK needs based on the image
#         self.crop_n_needs = 150  # Recommended Nitrogen (kg/ha)
#         self.crop_p_needs = 70   # Recommended Phosphorus (kg/ha)
#         self.crop_k_needs = 70   # Recommended Potassium (kg/ha)

#         # Initialize fuzzy variables
#         self._initialize_fuzzy_system()

#         # Updated growth stages based on the image
#         self.growth_stages = {
#             "Planting": {"weeks": (0, 2), "NPK": (1.5, 0.7, 0.7)},
#             "Early Growth": {"weeks": (2, 6), "NPK": (18.0, 4.2, 4.2)},
#             "Rapid Growth": {"weeks": (6, 14), "NPK": (60.0, 22.4, 18.9)},
#             "Mid-Season": {"weeks": (14, 22), "NPK": (51.0, 25.2, 25.9)},
#             "Late Season": {"weeks": (22, 36), "NPK": (19.5, 17.5, 20.3)}
#         }

#         # NPK complex fertilizers and individual fertilizers
#         self.fertilizers = {
#             "10:26:26": {"N": 0.10, "P": 0.26, "K": 0.26},
#             "12:32:16": {"N": 0.12, "P": 0.32, "K": 0.16},
#             "15:15:15": {"N": 0.15, "P": 0.15, "K": 0.15},
#             "Urea (46-0-0)": {"N": 0.46, "P": 0.0, "K": 0.0},
#             "DAP (18-46-0)": {"N": 0.18, "P": 0.46, "K": 0.0},
#             "MOP (0-0-60)": {"N": 0.0, "P": 0.0, "K": 0.60},
#             "Ammonium Sulfate (21-0-0)": {"N": 0.21, "P": 0.0, "K": 0.0},
#             "CAN (26-0-0)": {"N": 0.26, "P": 0.0, "K": 0.0},
#             "SSP (0-16-0)": {"N": 0.0, "P": 0.16, "K": 0.0},
#             "TSP (0-44-0)": {"N": 0.0, "P": 0.44, "K": 0.0},
#             "SOP (0-0-50)": {"N": 0.0, "P": 0.0, "K": 0.50},
#         }

#     def _initialize_fuzzy_system(self):
#         self.weeks = ctrl.Antecedent(np.arange(0, 37, 1), 'weeks')
#         self.n_fertilizer = ctrl.Consequent(np.arange(0, 16, 0.1), 'n_fertilizer')
#         self.p_fertilizer = ctrl.Consequent(np.arange(0, 8, 0.1), 'p_fertilizer')
#         self.k_fertilizer = ctrl.Consequent(np.arange(0, 8, 0.1), 'k_fertilizer')

#         # Membership functions for weeks
#         self.weeks['planting'] = fuzz.trimf(self.weeks.universe, [0, 0, 2])
#         self.weeks['early_growth'] = fuzz.trimf(self.weeks.universe, [2, 4, 6])
#         self.weeks['rapid_growth'] = fuzz.trimf(self.weeks.universe, [6, 10, 14])
#         self.weeks['mid_season'] = fuzz.trimf(self.weeks.universe, [14, 18, 22])
#         self.weeks['late_season'] = fuzz.trimf(self.weeks.universe, [22, 29, 36])

#         # Membership functions for fertilizers
#         self.n_fertilizer['very_low'] = fuzz.trimf(self.n_fertilizer.universe, [0, 0, 3])
#         self.n_fertilizer['low'] = fuzz.trimf(self.n_fertilizer.universe, [1.5, 4.5, 7.5])
#         self.n_fertilizer['medium'] = fuzz.trimf(self.n_fertilizer.universe, [6, 9, 12])
#         self.n_fertilizer['high'] = fuzz.trimf(self.n_fertilizer.universe, [10.5, 13.5, 15])

#         self.p_fertilizer['very_low'] = fuzz.trimf(self.p_fertilizer.universe, [0, 0, 1.4])
#         self.p_fertilizer['low'] = fuzz.trimf(self.p_fertilizer.universe, [0.7, 2.1, 3.5])
#         self.p_fertilizer['medium'] = fuzz.trimf(self.p_fertilizer.universe, [2.8, 4.2, 5.6])
#         self.p_fertilizer['high'] = fuzz.trimf(self.p_fertilizer.universe, [4.9, 6.3, 7])

#         self.k_fertilizer['very_low'] = fuzz.trimf(self.k_fertilizer.universe, [0, 0, 1.4])
#         self.k_fertilizer['low'] = fuzz.trimf(self.k_fertilizer.universe, [0.7, 2.1, 3.5])
#         self.k_fertilizer['medium'] = fuzz.trimf(self.k_fertilizer.universe, [2.8, 4.2, 5.6])
#         self.k_fertilizer['high'] = fuzz.trimf(self.k_fertilizer.universe, [4.9, 6.3, 7])

#         # Define fuzzy rules
#         self.rules = [
#             ctrl.Rule(self.weeks['planting'], (self.n_fertilizer['very_low'], self.p_fertilizer['very_low'], self.k_fertilizer['very_low'])),
#             ctrl.Rule(self.weeks['early_growth'], (self.n_fertilizer['low'], self.p_fertilizer['low'], self.k_fertilizer['low'])),
#             ctrl.Rule(self.weeks['rapid_growth'], (self.n_fertilizer['high'], self.p_fertilizer['medium'], self.k_fertilizer['medium'])),
#             ctrl.Rule(self.weeks['mid_season'], (self.n_fertilizer['medium'], self.p_fertilizer['high'], self.k_fertilizer['high'])),
#             ctrl.Rule(self.weeks['late_season'], (self.n_fertilizer['low'], self.p_fertilizer['medium'], self.k_fertilizer['medium']))
#         ]

#         # Create control system
#         self.fertilizer_ctrl = ctrl.ControlSystem(self.rules)
#         self.fertilizer_sim = ctrl.ControlSystemSimulation(self.fertilizer_ctrl)

#     def calculate_fertilizer(self, week):
#         self.fertilizer_sim.input['weeks'] = week
#         self.fertilizer_sim.compute()
#         return (
#             self.fertilizer_sim.output['n_fertilizer'],
#             self.fertilizer_sim.output['p_fertilizer'],
#             self.fertilizer_sim.output['k_fertilizer']
#         )

#     def calculate_fertilizer_amounts(self, n_needed, p_needed, k_needed):
#         amounts = {}
#         remaining_n = n_needed
#         remaining_p = p_needed
#         remaining_k = k_needed

#         # First, try to satisfy as much as possible with complex fertilizers
#         for fertilizer in ["15:15:15", "12:32:16", "10:26:26"]:
#             n_ratio, p_ratio, k_ratio = self.fertilizers[fertilizer]["N"], self.fertilizers[fertilizer]["P"], self.fertilizers[fertilizer]["K"]
#             amount = min(remaining_n / n_ratio, remaining_p / p_ratio, remaining_k / k_ratio)
#             if amount > 0:
#                 amounts[fertilizer] = amount
#                 remaining_n -= amount * n_ratio
#                 remaining_p -= amount * p_ratio
#                 remaining_k -= amount * k_ratio

#         # Then, use individual fertilizers for any remaining nutrients
#         if remaining_n > 0:
#             amounts["Urea (46-0-0)"] = remaining_n / 0.46
#         if remaining_p > 0:
#             amounts["TSP (0-44-0)"] = remaining_p / 0.44
#         if remaining_k > 0:
#             amounts["MOP (0-0-60)"] = remaining_k / 0.60

#         return amounts

#     def display_fertilizer_plan(self):
#         print(f"\nWeekly Fertilizer plan for {self.crop_name}:")
#         for week in range(37):  # 0 to 36 weeks
#             n, p, k = self.calculate_fertilizer(week)
#             print(f"\nWeek {week}:")
#             print(f"  NPK requirements: N: {n:.2f} kg/ha, P: {p:.2f} kg/ha, K: {k:.2f} kg/ha")
            
#             fertilizer_amounts = self.calculate_fertilizer_amounts(n, p, k)
#             print("  Recommended fertilizers:")
#             for fertilizer, amount in fertilizer_amounts.items():
#                 print(f"    {fertilizer}: {amount:.2f} kg/ha")

# # Example usage
# calculator = NPKComplexFertilizerCalculator(crop_name="Sugarcane", soil_n=50, soil_p=20, soil_k=30)
# calculator.display_fertilizer_plan()

import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class NPKComplexFertilizerCalculator:
    def __init__(self, crop_name, soil_n, soil_p, soil_k):
        self.crop_name = crop_name  # Name of the crop
        self.soil_n = soil_n  # Current Nitrogen level (kg/ha)
        self.soil_p = soil_p  # Current Phosphorus level (kg/ha)
        self.soil_k = soil_k  # Current Potassium level (kg/ha)

        # Updated Recommended NPK needs based on research
        self.crop_n_needs = 190  # Recommended Nitrogen (kg/ha)
        self.crop_p_needs = 96   # Recommended Phosphorus (kg/ha)
        self.crop_k_needs = 124  # Recommended Potassium (kg/ha)

        # Initialize fuzzy variables
        self._initialize_fuzzy_system()

        # Updated growth stages for Suru sugarcane
        self.growth_stages = {
            "Sowing": {"days": (0, 50), "NPK": (0, 96, 62)},
            "50 DAS": {"days": (51, 90), "NPK": (63, 0, 62)},
            "90 DAS": {"days": (91, 130), "NPK": (63, 0, 62)},
            "130 DAS": {"days": (131, 160), "NPK": (63, 0, 0)}
        }

        # NPK complex fertilizers and individual fertilizers
        self.fertilizers = {
            "10:26:26": {"N": 0.10, "P": 0.26, "K": 0.26},
            "12:32:16": {"N": 0.12, "P": 0.32, "K": 0.16},
            "15:15:15": {"N": 0.15, "P": 0.15, "K": 0.15},
            "Urea (46-0-0)": {"N": 0.46, "P": 0.0, "K": 0.0},
            "DAP (18-46-0)": {"N": 0.18, "P": 0.46, "K": 0.0},
            "MOP (0-0-60)": {"N": 0.0, "P": 0.0, "K": 0.60},
            "Ammonium Sulfate (21-0-0)": {"N": 0.21, "P": 0.0, "K": 0.0},
            "CAN (26-0-0)": {"N": 0.26, "P": 0.0, "K": 0.0},
            "SSP (0-16-0)": {"N": 0.0, "P": 0.16, "K": 0.0},
            "TSP (0-44-0)": {"N": 0.0, "P": 0.44, "K": 0.0},
            "SOP (0-0-50)": {"N": 0.0, "P": 0.0, "K": 0.50},
        }

    def _initialize_fuzzy_system(self):
        # Define fuzzy variables
        self.n_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'n_needed')
        self.p_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'p_needed')
        self.k_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'k_needed')

        self.n_fertilizer = ctrl.Consequent(np.arange(0, 131, 1), 'n_fertilizer')
        self.p_fertilizer = ctrl.Consequent(np.arange(0, 101, 1), 'p_fertilizer')
        self.k_fertilizer = ctrl.Consequent(np.arange(0, 51, 1), 'k_fertilizer')

        # Membership functions for inputs (N, P, K needs)
        self.n_needed['low'] = fuzz.trimf(self.n_needed.universe, [0, 0, 100])
        self.n_needed['medium'] = fuzz.trimf(self.n_needed.universe, [50, 100, 150])
        self.n_needed['high'] = fuzz.trimf(self.n_needed.universe, [100, 200, 200])

        self.p_needed['low'] = fuzz.trimf(self.p_needed.universe, [0, 0, 50])
        self.p_needed['medium'] = fuzz.trimf(self.p_needed.universe, [25, 50, 75])
        self.p_needed['high'] = fuzz.trimf(self.p_needed.universe, [50, 100, 100])

        self.k_needed['low'] = fuzz.trimf(self.k_needed.universe, [0, 0, 50])
        self.k_needed['medium'] = fuzz.trimf(self.k_needed.universe, [25, 40, 50])
        self.k_needed['high'] = fuzz.trimf(self.k_needed.universe, [40, 50, 50])

        # Define membership functions for outputs
        self.n_fertilizer['low'] = fuzz.trimf(self.n_fertilizer.universe, [0, 0, 65])
        self.n_fertilizer['medium'] = fuzz.trimf(self.n_fertilizer.universe, [30, 65, 100])
        self.n_fertilizer['high'] = fuzz.trimf(self.n_fertilizer.universe, [65, 130, 130])

        self.p_fertilizer['low'] = fuzz.trimf(self.p_fertilizer.universe, [0, 0, 30])
        self.p_fertilizer['medium'] = fuzz.trimf(self.p_fertilizer.universe, [15, 30, 60])
        self.p_fertilizer['high'] = fuzz.trimf(self.p_fertilizer.universe, [30, 100, 100])

        self.k_fertilizer['low'] = fuzz.trimf(self.k_fertilizer.universe, [0, 0, 25])
        self.k_fertilizer['medium'] = fuzz.trimf(self.k_fertilizer.universe, [10, 25, 30])
        self.k_fertilizer['high'] = fuzz.trimf(self.k_fertilizer.universe, [25, 50, 50])

        # Define fuzzy rules
        self.rules = [
            ctrl.Rule(self.n_needed['low'] & self.p_needed['low'] & self.k_needed['low'],
                      (self.n_fertilizer['high'], self.p_fertilizer['high'], self.k_fertilizer['high'])),
            ctrl.Rule(self.n_needed['medium'] & self.p_needed['medium'] & self.k_needed['medium'],
                      (self.n_fertilizer['medium'], self.p_fertilizer['medium'], self.k_fertilizer['medium'])),
            ctrl.Rule(self.n_needed['high'] & self.p_needed['high'] & self.k_needed['high'],
                      (self.n_fertilizer['low'], self.p_fertilizer['low'], self.k_fertilizer['low'])),
            ctrl.Rule(self.n_needed['low'] & self.p_needed['high'] & self.k_needed['medium'],
                      (self.n_fertilizer['high'], self.p_fertilizer['medium'], self.k_fertilizer['low'])),
        ]

        # Create control system
        self.fertilizer_ctrl = ctrl.ControlSystem(self.rules)
        self.fertilizer_sim = ctrl.ControlSystemSimulation(self.fertilizer_ctrl)

    def fuzzy_logic(self, growth_stage):
        # Get NPK needs based on growth stage
        n_needed_target, p_needed_target, k_needed_target = self.get_npk_needs(growth_stage)

        # Fuzzy logic to calculate fertilizer required
        n_needed = max(0, n_needed_target - self.soil_n)
        p_needed = max(0, p_needed_target - self.soil_p)
        k_needed = max(0, k_needed_target - self.soil_k)

        # Set inputs to the fuzzy logic system
        self.fertilizer_sim.input['n_needed'] = n_needed
        self.fertilizer_sim.input['p_needed'] = p_needed
        self.fertilizer_sim.input['k_needed'] = k_needed

        # Compute the fuzzy logic output
        self.fertilizer_sim.compute()

        # Get the fertilizer amounts needed
        n_fertilizer_needed = self.fertilizer_sim.output['n_fertilizer']
        p_fertilizer_needed = self.fertilizer_sim.output['p_fertilizer']
        k_fertilizer_needed = self.fertilizer_sim.output['k_fertilizer']

        return n_fertilizer_needed, p_fertilizer_needed, k_fertilizer_needed

    def get_npk_needs(self, growth_stage):
        # Get the NPK needs based on the growth stage
        return self.growth_stages[growth_stage]['NPK']

    def calculate_fertilizer_amounts(self, n_fertilizer_needed, p_fertilizer_needed, k_fertilizer_needed):
        # Calculate the amount of each fertilizer needed while considering interactions
        amounts = {}
        total_n_applied = total_p_applied = total_k_applied = 0

        for fertilizer, nutrients in self.fertilizers.items():
            n_content = nutrients["N"]
            p_content = nutrients["P"]
            k_content = nutrients["K"]

            # Adjust remaining needs by subtracting already applied nutrients
            n_needed_remaining = max(0, n_fertilizer_needed - total_n_applied)
            p_needed_remaining = max(0, p_fertilizer_needed - total_p_applied)
            k_needed_remaining = max(0, k_fertilizer_needed - total_k_applied)

            # Calculate how much of the current fertilizer is required
            n_amount = n_needed_remaining / n_content if n_content > 0 else 0
            p_amount = p_needed_remaining / p_content if p_content > 0 else 0
            k_amount = k_needed_remaining / k_content if k_content > 0 else 0

            # Use the maximum amount required based on N, P, or K content
            amount_to_apply = max(n_amount, p_amount, k_amount)
            amounts[fertilizer] = amount_to_apply

            # Update the total applied nutrients
            total_n_applied += amount_to_apply * n_content
            total_p_applied += amount_to_apply * p_content
            total_k_applied += amount_to_apply * k_content

        return amounts

    def display_fertilizer_plan(self):
        # Initialize a list to store fertilizer plans for each growth stage
        fertilizer_plan_list = []

        print(f"\nFertilizer plan for {self.crop_name}:")
        for phase, stage_data in self.growth_stages.items():
            # Get fertilizer amounts using fuzzy logic
            n_fertilizer, p_fertilizer, k_fertilizer = self.fuzzy_logic(phase)
            fertilizer_amounts = self.calculate_fertilizer_amounts(n_fertilizer, p_fertilizer, k_fertilizer)

            # Display the data
            print(f"{phase} (Days: {stage_data['days'][0]} to {stage_data['days'][1]}):")
            print(f"  N fertilizer needed: {n_fertilizer:.2f} kg/ha")
            print(f"  P fertilizer needed: {p_fertilizer:.2f} kg/ha")
            print(f"  K fertilizer needed: {k_fertilizer:.2f} kg/ha")

            for fertilizer, amount in fertilizer_amounts.items():
                print(f"    {fertilizer}: {amount:.2f} kg/ha")

            print()

            # Store the data for this phase in a dictionary
            phase_data = {
                'phase': phase,
                'days': stage_data['days'],
                'n_fertilizer_needed': n_fertilizer,
                'p_fertilizer_needed': p_fertilizer,
                'k_fertilizer_needed': k_fertilizer,
                'specific_fertilizer_amounts': fertilizer_amounts  # Dictionary with the specific fertilizer amounts
            }

            # Append the dictionary to the list
            fertilizer_plan_list.append(phase_data)

        # Return the list containing all phases' data
        return fertilizer_plan_list


# Example usage
calculator = NPKComplexFertilizerCalculator(crop_name="Sugarcane", soil_n=50, soil_p=20, soil_k=30)
calculator.display_fertilizer_plan()
