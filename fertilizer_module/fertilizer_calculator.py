# import numpy as np
# import skfuzzy as fuzz
# from skfuzzy import control as ctrl

# class NPKComplexFertilizerCalculator_sugarcane:
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
# calculator = NPKComplexFertilizerCalculator_sugarcane(crop_name="Sugarcane", soil_n=50, soil_p=20, soil_k=30)
# calculator.display_fertilizer_plan()


# # import numpy as np
# # import skfuzzy as fuzz
# # from skfuzzy import control as ctrl

# # class NPKComplexFertilizerCalculator:
# #     def __init__(self, crop_name, soil_n, soil_p, soil_k):
# #         self.crop_name = crop_name
# #         self.soil_n = soil_n
# #         self.soil_p = soil_p
# #         self.soil_k = soil_k

# #         # Updated Recommended NPK needs based on the image
# #         self.crop_n_needs = 150  # Recommended Nitrogen (kg/ha)
# #         self.crop_p_needs = 70   # Recommended Phosphorus (kg/ha)
# #         self.crop_k_needs = 70   # Recommended Potassium (kg/ha)

# #         # Initialize fuzzy variables
# #         self._initialize_fuzzy_system()

# #         # Updated growth stages based on the image
# #         self.growth_stages = {
# #             "Planting": {"weeks": (0, 2), "NPK": (1.5, 0.7, 0.7)},
# #             "Early Growth": {"weeks": (2, 6), "NPK": (18.0, 4.2, 4.2)},
# #             "Rapid Growth": {"weeks": (6, 14), "NPK": (60.0, 22.4, 18.9)},
# #             "Mid-Season": {"weeks": (14, 22), "NPK": (51.0, 25.2, 25.9)},
# #             "Late Season": {"weeks": (22, 36), "NPK": (19.5, 17.5, 20.3)}
# #         }

# #         # NPK complex fertilizers and individual fertilizers
# #         self.fertilizers = {
# #             "10:26:26": {"N": 0.10, "P": 0.26, "K": 0.26},
# #             "12:32:16": {"N": 0.12, "P": 0.32, "K": 0.16},
# #             "15:15:15": {"N": 0.15, "P": 0.15, "K": 0.15},
# #             "Urea (46-0-0)": {"N": 0.46, "P": 0.0, "K": 0.0},
# #             "DAP (18-46-0)": {"N": 0.18, "P": 0.46, "K": 0.0},
# #             "MOP (0-0-60)": {"N": 0.0, "P": 0.0, "K": 0.60},
# #             "Ammonium Sulfate (21-0-0)": {"N": 0.21, "P": 0.0, "K": 0.0},
# #             "CAN (26-0-0)": {"N": 0.26, "P": 0.0, "K": 0.0},
# #             "SSP (0-16-0)": {"N": 0.0, "P": 0.16, "K": 0.0},
# #             "TSP (0-44-0)": {"N": 0.0, "P": 0.44, "K": 0.0},
# #             "SOP (0-0-50)": {"N": 0.0, "P": 0.0, "K": 0.50},
# #         }

# #     def _initialize_fuzzy_system(self):
# #         self.weeks = ctrl.Antecedent(np.arange(0, 37, 1), 'weeks')
# #         self.n_fertilizer = ctrl.Consequent(np.arange(0, 16, 0.1), 'n_fertilizer')
# #         self.p_fertilizer = ctrl.Consequent(np.arange(0, 8, 0.1), 'p_fertilizer')
# #         self.k_fertilizer = ctrl.Consequent(np.arange(0, 8, 0.1), 'k_fertilizer')

# #         # Membership functions for weeks
# #         self.weeks['planting'] = fuzz.trimf(self.weeks.universe, [0, 0, 2])
# #         self.weeks['early_growth'] = fuzz.trimf(self.weeks.universe, [2, 4, 6])
# #         self.weeks['rapid_growth'] = fuzz.trimf(self.weeks.universe, [6, 10, 14])
# #         self.weeks['mid_season'] = fuzz.trimf(self.weeks.universe, [14, 18, 22])
# #         self.weeks['late_season'] = fuzz.trimf(self.weeks.universe, [22, 29, 36])

# #         # Membership functions for fertilizers
# #         self.n_fertilizer['very_low'] = fuzz.trimf(self.n_fertilizer.universe, [0, 0, 3])
# #         self.n_fertilizer['low'] = fuzz.trimf(self.n_fertilizer.universe, [1.5, 4.5, 7.5])
# #         self.n_fertilizer['medium'] = fuzz.trimf(self.n_fertilizer.universe, [6, 9, 12])
# #         self.n_fertilizer['high'] = fuzz.trimf(self.n_fertilizer.universe, [10.5, 13.5, 15])

# #         self.p_fertilizer['very_low'] = fuzz.trimf(self.p_fertilizer.universe, [0, 0, 1.4])
# #         self.p_fertilizer['low'] = fuzz.trimf(self.p_fertilizer.universe, [0.7, 2.1, 3.5])
# #         self.p_fertilizer['medium'] = fuzz.trimf(self.p_fertilizer.universe, [2.8, 4.2, 5.6])
# #         self.p_fertilizer['high'] = fuzz.trimf(self.p_fertilizer.universe, [4.9, 6.3, 7])

# #         self.k_fertilizer['very_low'] = fuzz.trimf(self.k_fertilizer.universe, [0, 0, 1.4])
# #         self.k_fertilizer['low'] = fuzz.trimf(self.k_fertilizer.universe, [0.7, 2.1, 3.5])
# #         self.k_fertilizer['medium'] = fuzz.trimf(self.k_fertilizer.universe, [2.8, 4.2, 5.6])
# #         self.k_fertilizer['high'] = fuzz.trimf(self.k_fertilizer.universe, [4.9, 6.3, 7])

# #         # Define fuzzy rules
# #         self.rules = [
# #             ctrl.Rule(self.weeks['planting'], (self.n_fertilizer['very_low'], self.p_fertilizer['very_low'], self.k_fertilizer['very_low'])),
# #             ctrl.Rule(self.weeks['early_growth'], (self.n_fertilizer['low'], self.p_fertilizer['low'], self.k_fertilizer['low'])),
# #             ctrl.Rule(self.weeks['rapid_growth'], (self.n_fertilizer['high'], self.p_fertilizer['medium'], self.k_fertilizer['medium'])),
# #             ctrl.Rule(self.weeks['mid_season'], (self.n_fertilizer['medium'], self.p_fertilizer['high'], self.k_fertilizer['high'])),
# #             ctrl.Rule(self.weeks['late_season'], (self.n_fertilizer['low'], self.p_fertilizer['medium'], self.k_fertilizer['medium']))
# #         ]

# #         # Create control system
# #         self.fertilizer_ctrl = ctrl.ControlSystem(self.rules)
# #         self.fertilizer_sim = ctrl.ControlSystemSimulation(self.fertilizer_ctrl)

# #     def calculate_fertilizer(self, week):
# #         self.fertilizer_sim.input['weeks'] = week
# #         self.fertilizer_sim.compute()
# #         return (
# #             self.fertilizer_sim.output['n_fertilizer'],
# #             self.fertilizer_sim.output['p_fertilizer'],
# #             self.fertilizer_sim.output['k_fertilizer']
# #         )

# #     def calculate_fertilizer_amounts(self, n_needed, p_needed, k_needed):
# #         amounts = {}
# #         remaining_n = n_needed
# #         remaining_p = p_needed
# #         remaining_k = k_needed

# #         # First, try to satisfy as much as possible with complex fertilizers
# #         for fertilizer in ["15:15:15", "12:32:16", "10:26:26"]:
# #             n_ratio, p_ratio, k_ratio = self.fertilizers[fertilizer]["N"], self.fertilizers[fertilizer]["P"], self.fertilizers[fertilizer]["K"]
# #             amount = min(remaining_n / n_ratio, remaining_p / p_ratio, remaining_k / k_ratio)
# #             if amount > 0:
# #                 amounts[fertilizer] = amount
# #                 remaining_n -= amount * n_ratio
# #                 remaining_p -= amount * p_ratio
# #                 remaining_k -= amount * k_ratio

# #         # Then, use individual fertilizers for any remaining nutrients
# #         if remaining_n > 0:
# #             amounts["Urea (46-0-0)"] = remaining_n / 0.46
# #         if remaining_p > 0:
# #             amounts["TSP (0-44-0)"] = remaining_p / 0.44
# #         if remaining_k > 0:
# #             amounts["MOP (0-0-60)"] = remaining_k / 0.60

# #         return amounts

# #     def display_fertilizer_plan(self):
# #         print(f"\nWeekly Fertilizer plan for {self.crop_name}:")
# #         for week in range(37):  # 0 to 36 weeks
# #             n, p, k = self.calculate_fertilizer(week)
# #             print(f"\nWeek {week}:")
# #             print(f"  NPK requirements: N: {n:.2f} kg/ha, P: {p:.2f} kg/ha, K: {k:.2f} kg/ha")
            
# #             fertilizer_amounts = self.calculate_fertilizer_amounts(n, p, k)
# #             print("  Recommended fertilizers:")
# #             for fertilizer, amount in fertilizer_amounts.items():
# #                 print(f"    {fertilizer}: {amount:.2f} kg/ha")

# # Example usage
# # calculator = NPKComplexFertilizerCalculator(crop_name="Sugarcane", soil_n=50, soil_p=20, soil_k=30)
# # calculator.display_fertilizer_plan()

# # import numpy as np
# # import skfuzzy as fuzz
# # from skfuzzy import control as ctrl

# # class NPKComplexFertilizerCalculator_sugarcane:
# #     def __init__(self, crop_name, soil_n, soil_p, soil_k):
# #         self.crop_name = crop_name  # Name of the crop
# #         self.soil_n = soil_n  # Current Nitrogen level (kg/ha)
# #         self.soil_p = soil_p  # Current Phosphorus level (kg/ha)
# #         self.soil_k = soil_k  # Current Potassium level (kg/ha)

# #         # Updated Recommended NPK needs based on research
# #         self.crop_n_needs = 190  # Recommended Nitrogen (kg/ha)
# #         self.crop_p_needs = 96   # Recommended Phosphorus (kg/ha)
# #         self.crop_k_needs = 124  # Recommended Potassium (kg/ha)

# #         # Initialize fuzzy variables
# #         self._initialize_fuzzy_system()

# #         # Updated growth stages for Suru sugarcane
# #         self.growth_stages = {
# #             "Sowing": {"days": (0, 50), "NPK": (0, 96, 62)},
# #             "50 DAS": {"days": (51, 90), "NPK": (63, 0, 62)},
# #             "90 DAS": {"days": (91, 130), "NPK": (63, 0, 62)},
# #             "130 DAS": {"days": (131, 160), "NPK": (63, 0, 0)}
# #         }

# #         # NPK complex fertilizers and individual fertilizers
# #         self.fertilizers = {
# #             "10:26:26": {"N": 0.10, "P": 0.26, "K": 0.26},
# #             "12:32:16": {"N": 0.12, "P": 0.32, "K": 0.16},
# #             "15:15:15": {"N": 0.15, "P": 0.15, "K": 0.15},
# #             "Urea (46-0-0)": {"N": 0.46, "P": 0.0, "K": 0.0},
# #             "DAP (18-46-0)": {"N": 0.18, "P": 0.46, "K": 0.0},
# #             "MOP (0-0-60)": {"N": 0.0, "P": 0.0, "K": 0.60},
# #             "Ammonium Sulfate (21-0-0)": {"N": 0.21, "P": 0.0, "K": 0.0},
# #             "CAN (26-0-0)": {"N": 0.26, "P": 0.0, "K": 0.0},
# #             "SSP (0-16-0)": {"N": 0.0, "P": 0.16, "K": 0.0},
# #             "TSP (0-44-0)": {"N": 0.0, "P": 0.44, "K": 0.0},
# #             "SOP (0-0-50)": {"N": 0.0, "P": 0.0, "K": 0.50},
# #         }

# #     def _initialize_fuzzy_system(self):
# #         # Define fuzzy variables
# #         self.n_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'n_needed')
# #         self.p_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'p_needed')
# #         self.k_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'k_needed')

# #         self.n_fertilizer = ctrl.Consequent(np.arange(0, 131, 1), 'n_fertilizer')
# #         self.p_fertilizer = ctrl.Consequent(np.arange(0, 101, 1), 'p_fertilizer')
# #         self.k_fertilizer = ctrl.Consequent(np.arange(0, 51, 1), 'k_fertilizer')

# #         # Membership functions for inputs (N, P, K needs)
# #         self.n_needed['low'] = fuzz.trimf(self.n_needed.universe, [0, 0, 100])
# #         self.n_needed['medium'] = fuzz.trimf(self.n_needed.universe, [50, 100, 150])
# #         self.n_needed['high'] = fuzz.trimf(self.n_needed.universe, [100, 200, 200])

# #         self.p_needed['low'] = fuzz.trimf(self.p_needed.universe, [0, 0, 50])
# #         self.p_needed['medium'] = fuzz.trimf(self.p_needed.universe, [25, 50, 75])
# #         self.p_needed['high'] = fuzz.trimf(self.p_needed.universe, [50, 100, 100])

# #         self.k_needed['low'] = fuzz.trimf(self.k_needed.universe, [0, 0, 50])
# #         self.k_needed['medium'] = fuzz.trimf(self.k_needed.universe, [25, 40, 50])
# #         self.k_needed['high'] = fuzz.trimf(self.k_needed.universe, [40, 50, 50])

# #         # Define membership functions for outputs
# #         self.n_fertilizer['low'] = fuzz.trimf(self.n_fertilizer.universe, [0, 0, 65])
# #         self.n_fertilizer['medium'] = fuzz.trimf(self.n_fertilizer.universe, [30, 65, 100])
# #         self.n_fertilizer['high'] = fuzz.trimf(self.n_fertilizer.universe, [65, 130, 130])

# #         self.p_fertilizer['low'] = fuzz.trimf(self.p_fertilizer.universe, [0, 0, 30])
# #         self.p_fertilizer['medium'] = fuzz.trimf(self.p_fertilizer.universe, [15, 30, 60])
# #         self.p_fertilizer['high'] = fuzz.trimf(self.p_fertilizer.universe, [30, 100, 100])

# #         self.k_fertilizer['low'] = fuzz.trimf(self.k_fertilizer.universe, [0, 0, 25])
# #         self.k_fertilizer['medium'] = fuzz.trimf(self.k_fertilizer.universe, [10, 25, 30])
# #         self.k_fertilizer['high'] = fuzz.trimf(self.k_fertilizer.universe, [25, 50, 50])

# #         # Define fuzzy rules
# #         self.rules = [
# #             ctrl.Rule(self.n_needed['low'] & self.p_needed['low'] & self.k_needed['low'],
# #                       (self.n_fertilizer['high'], self.p_fertilizer['high'], self.k_fertilizer['high'])),
# #             ctrl.Rule(self.n_needed['medium'] & self.p_needed['medium'] & self.k_needed['medium'],
# #                       (self.n_fertilizer['medium'], self.p_fertilizer['medium'], self.k_fertilizer['medium'])),
# #             ctrl.Rule(self.n_needed['high'] & self.p_needed['high'] & self.k_needed['high'],
# #                       (self.n_fertilizer['low'], self.p_fertilizer['low'], self.k_fertilizer['low'])),
# #             ctrl.Rule(self.n_needed['low'] & self.p_needed['high'] & self.k_needed['medium'],
# #                       (self.n_fertilizer['high'], self.p_fertilizer['medium'], self.k_fertilizer['low'])),
# #         ]

# #         # Create control system
# #         self.fertilizer_ctrl = ctrl.ControlSystem(self.rules)
# #         self.fertilizer_sim = ctrl.ControlSystemSimulation(self.fertilizer_ctrl)

# #     def fuzzy_logic(self, growth_stage):
# #         # Get NPK needs based on growth stage
# #         n_needed_target, p_needed_target, k_needed_target = self.get_npk_needs(growth_stage)

# #         # Fuzzy logic to calculate fertilizer required
# #         n_needed = max(0, n_needed_target - self.soil_n)
# #         p_needed = max(0, p_needed_target - self.soil_p)
# #         k_needed = max(0, k_needed_target - self.soil_k)

# #         # Set inputs to the fuzzy logic system
# #         self.fertilizer_sim.input['n_needed'] = n_needed
# #         self.fertilizer_sim.input['p_needed'] = p_needed
# #         self.fertilizer_sim.input['k_needed'] = k_needed

# #         # Compute the fuzzy logic output
# #         self.fertilizer_sim.compute()

# #         # Get the fertilizer amounts needed
# #         n_fertilizer_needed = self.fertilizer_sim.output['n_fertilizer']
# #         p_fertilizer_needed = self.fertilizer_sim.output['p_fertilizer']
# #         k_fertilizer_needed = self.fertilizer_sim.output['k_fertilizer']

# #         return n_fertilizer_needed, p_fertilizer_needed, k_fertilizer_needed

# #     def get_npk_needs(self, growth_stage):
# #         # Get the NPK needs based on the growth stage
# #         return self.growth_stages[growth_stage]['NPK']

# #     def calculate_fertilizer_amounts(self, n_fertilizer_needed, p_fertilizer_needed, k_fertilizer_needed):
# #         # Calculate the amount of each fertilizer needed while considering interactions
# #         amounts = {}
# #         total_n_applied = total_p_applied = total_k_applied = 0

# #         for fertilizer, nutrients in self.fertilizers.items():
# #             n_content = nutrients["N"]
# #             p_content = nutrients["P"]
# #             k_content = nutrients["K"]

# #             # Adjust remaining needs by subtracting already applied nutrients
# #             n_needed_remaining = max(0, n_fertilizer_needed - total_n_applied)
# #             p_needed_remaining = max(0, p_fertilizer_needed - total_p_applied)
# #             k_needed_remaining = max(0, k_fertilizer_needed - total_k_applied)

# #             # Calculate how much of the current fertilizer is required
# #             n_amount = n_needed_remaining / n_content if n_content > 0 else 0
# #             p_amount = p_needed_remaining / p_content if p_content > 0 else 0
# #             k_amount = k_needed_remaining / k_content if k_content > 0 else 0

# #             # Use the maximum amount required based on N, P, or K content
# #             amount_to_apply = max(n_amount, p_amount, k_amount)
# #             amounts[fertilizer] = amount_to_apply

# #             # Update the total applied nutrients
# #             total_n_applied += amount_to_apply * n_content
# #             total_p_applied += amount_to_apply * p_content
# #             total_k_applied += amount_to_apply * k_content

# #         return amounts

# #     def display_fertilizer_plan(self):
# #         # Initialize a list to store fertilizer plans for each growth stage
# #         fertilizer_plan_list = []

# #         print(f"\nFertilizer plan for {self.crop_name}:")
# #         for phase, stage_data in self.growth_stages.items():
# #             # Get fertilizer amounts using fuzzy logic
# #             n_fertilizer, p_fertilizer, k_fertilizer = self.fuzzy_logic(phase)
# #             fertilizer_amounts = self.calculate_fertilizer_amounts(n_fertilizer, p_fertilizer, k_fertilizer)

# #             # Display the data
# #             print(f"{phase} (Days: {stage_data['days'][0]} to {stage_data['days'][1]}):")
# #             print(f"  N fertilizer needed: {n_fertilizer:.2f} kg/ha")
# #             print(f"  P fertilizer needed: {p_fertilizer:.2f} kg/ha")
# #             print(f"  K fertilizer needed: {k_fertilizer:.2f} kg/ha")

# #             for fertilizer, amount in fertilizer_amounts.items():
# #                 print(f"    {fertilizer}: {amount:.2f} kg/ha")

# #             print()

# #             # Store the data for this phase in a dictionary
# #             phase_data = {
# #                 'phase': phase,
# #                 'days': stage_data['days'],
# #                 'n_fertilizer_needed': n_fertilizer,
# #                 'p_fertilizer_needed': p_fertilizer,
# #                 'k_fertilizer_needed': k_fertilizer,
# #                 'specific_fertilizer_amounts': fertilizer_amounts  # Dictionary with the specific fertilizer amounts
# #             }

# #             # Append the dictionary to the list
# #             fertilizer_plan_list.append(phase_data)

# #         # Return the list containing all phases' data
# #         return fertilizer_plan_list


# # # # Example usage
# # # calculator = NPKComplexFertilizerCalculator_sugarcane(crop_name="Sugarcane", soil_n=50, soil_p=20, soil_k=30)
# # # calculator.display_fertilizer_plan()
import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class NPKComplexFertilizerCalculator_sugarcane:
    def __init__(self, crop_name, soil_n,soil_p,soil_k):
        self.crop_name = crop_name  # Name of the crop
        self.soil_n=soil_n
        self.soil_p=soil_p
        self.soil_k = soil_k  # Current NPK ratio in the soil
        self.ideal_soil_n, self.ideal_soil_p, self.ideal_soil_k = (1.0, 0.067, 0.25 ) # Ideal NPK ratio in the soil

        # Calculate the recommended NPK needs based on the difference between the current and ideal soil NPK levels
        self.crop_n_needs = self.ideal_soil_n * (1 - (self.soil_n / self.ideal_soil_n))
        self.crop_p_needs = self.ideal_soil_p * (1 - (self.soil_p / self.ideal_soil_p))
        self.crop_k_needs = self.ideal_soil_k * (1 - (self.soil_k / self.ideal_soil_k))

        # Initialize fuzzy variables
        self._initialize_fuzzy_system()

        # Growth stages with fertilizer recommendations for sugarcane
        self.growth_stages = {
            "Planting": {"days": (0, 30), "NPK_ratio": (20, 40, 10), "biofertilizer": True},
            "Tillering": {"days": (31, 90), "NPK_ratio": (100, 30, 50), "biofertilizer": True},
            "Grand Growth": {"days": (91, 210), "NPK_ratio": (100, 35, 55), "biofertilizer": True},
            "Maturity": {"days": (211, 365), "NPK_ratio": (20, 20, 30)},
            "Harvesting": {"days": (366, 380), "NPK_ratio": (10, 50, 10)}
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

        # Micronutrient management
        self.micronutrients = {
            "Zinc sulphate": {"dose": 37.5, "condition": "zinc_deficient"},
            "Ferrous sulphate": {"dose": 100, "condition": "iron_deficient"},
            "Copper sulphate": {"dose": 5, "condition": "copper_deficient"}
        }

    def _initialize_fuzzy_system(self):
        # Define fuzzy variables
        self.n_needed = ctrl.Antecedent(np.arange(0, 301, 1), 'n_needed')
        self.p_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'p_needed')
        self.k_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'k_needed')

        self.n_fertilizer = ctrl.Consequent(np.arange(0, 301, 1), 'n_fertilizer')
        self.p_fertilizer = ctrl.Consequent(np.arange(0, 101, 1), 'p_fertilizer')
        self.k_fertilizer = ctrl.Consequent(np.arange(0, 201, 1), 'k_fertilizer')

        # Membership functions for inputs (N, P, K needs)
        self.n_needed['low'] = fuzz.trimf(self.n_needed.universe, [0, 0, 150])
        self.n_needed['medium'] = fuzz.trimf(self.n_needed.universe, [100, 150, 200])
        self.n_needed['high'] = fuzz.trimf(self.n_needed.universe, [150, 300, 300])

        self.p_needed['low'] = fuzz.trimf(self.p_needed.universe, [0, 0, 50])
        self.p_needed['medium'] = fuzz.trimf(self.p_needed.universe, [30, 50, 80])
        self.p_needed['high'] = fuzz.trimf(self.p_needed.universe, [50, 100, 100])

        self.k_needed['low'] = fuzz.trimf(self.k_needed.universe, [0, 0, 100])
        self.k_needed['medium'] = fuzz.trimf(self.k_needed.universe, [50, 100, 150])
        self.k_needed['high'] = fuzz.trimf(self.k_needed.universe, [100, 200, 200])

        # Membership functions for outputs (fertilizer)
        self.n_fertilizer['low'] = fuzz.trimf(self.n_fertilizer.universe, [0, 0, 100])
        self.n_fertilizer['medium'] = fuzz.trimf(self.n_fertilizer.universe, [50, 150, 250])
        self.n_fertilizer['high'] = fuzz.trimf(self.n_fertilizer.universe, [150, 300, 300])

        self.p_fertilizer['low'] = fuzz.trimf(self.p_fertilizer.universe, [0, 0, 40])
        self.p_fertilizer['medium'] = fuzz.trimf(self.p_fertilizer.universe, [20, 50, 70])
        self.p_fertilizer['high'] = fuzz.trimf(self.p_fertilizer.universe, [50, 100, 100])

        self.k_fertilizer['low'] = fuzz.trimf(self.k_fertilizer.universe, [0, 0, 50])
        self.k_fertilizer['medium'] = fuzz.trimf(self.k_fertilizer.universe, [30, 100, 150])
        self.k_fertilizer['high'] = fuzz.trimf(self.k_fertilizer.universe, [100, 200, 200])

        # Define fuzzy rules
        self.rules = [
            ctrl.Rule(self.n_needed['low'] & self.p_needed['low'] & self.k_needed['low'],
                      (self.n_fertilizer['low'], self.p_fertilizer['low'], self.k_fertilizer['low'])),
            ctrl.Rule(self.n_needed['medium'] & self.p_needed['medium'] & self.k_needed['medium'],
                      (self.n_fertilizer['medium'], self.p_fertilizer['medium'], self.k_fertilizer['medium'])),
            ctrl.Rule(self.n_needed['high'] & self.p_needed['high'] & self.k_needed['high'],
                      (self.n_fertilizer['high'], self.p_fertilizer['high'], self.k_fertilizer['high'])),
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

        # Adjust the NPK needs based on the difference between the current and ideal soil NPK levels
        n_fertilizer_needed = n_needed * (1 - (self.soil_n / self.ideal_soil_n))
        p_fertilizer_needed = p_needed * (1 - (self.soil_p / self.ideal_soil_p))
        k_fertilizer_needed = k_needed * (1 - (self.soil_k / self.ideal_soil_k))

        # Set inputs to the fuzzy logic system
        self.fertilizer_sim.input['n_needed'] = n_fertilizer_needed
        self.fertilizer_sim.input['p_needed'] = p_fertilizer_needed
        self.fertilizer_sim.input['k_needed'] = k_fertilizer_needed

        # Compute the fuzzy logic output
        self.fertilizer_sim.compute()

        # Get the fertilizer amounts needed
        n_fertilizer_needed = self.fertilizer_sim.output['n_fertilizer']
        p_fertilizer_needed = self.fertilizer_sim.output['p_fertilizer']
        k_fertilizer_needed = self.fertilizer_sim.output['k_fertilizer']

        return n_fertilizer_needed, p_fertilizer_needed, k_fertilizer_needed

    def get_npk_needs(self, growth_stage):
        # Get the NPK needs based on the growth stage
        n_ratio, p_ratio, k_ratio = self.growth_stages[growth_stage]['NPK_ratio']
        return n_ratio, p_ratio, k_ratio

    def calculate_fertilizer_amounts(self, n_fertilizer_needed, p_fertilizer_needed, k_fertilizer_needed):
        amounts = {}
        total_n_applied = total_p_applied = total_k_applied = 0

        # Count available fertilizers with N, P, and K to distribute evenly
        n_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["N"] > 0]
        p_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["P"] > 0]
        k_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["K"] > 0]

        # Distribute N evenly across all nitrogen-heavy and balanced fertilizers
        for fertilizer in n_fertilizers:
            n_content = self.fertilizers[fertilizer]["N"]
            n_share = n_fertilizer_needed / len(n_fertilizers)  # Split nitrogen need evenly
            n_amount = n_share / n_content if n_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + n_amount
            total_n_applied += n_amount * n_content

        # Distribute P evenly across all phosphorus-heavy and balanced fertilizers
        for fertilizer in p_fertilizers:
            p_content = self.fertilizers[fertilizer]["P"]
            p_share = p_fertilizer_needed / len(p_fertilizers)  # Split phosphorus need evenly
            p_amount = p_share / p_content if p_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + p_amount
            total_p_applied += p_amount * p_content

        # Distribute K evenly across all potassium-heavy and balanced fertilizers
        for fertilizer in k_fertilizers:
            k_content = self.fertilizers[fertilizer]["K"]
            k_share = k_fertilizer_needed / len(k_fertilizers)  # Split potassium need evenly
            k_amount = k_share / k_content if k_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + k_amount
            total_k_applied += k_amount * k_content

        # Rebalance amounts across all fertilizers
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
             print(f"  N fertilizer ratio: {stage_data['NPK_ratio'][0]}%")
             print(f"  P fertilizer ratio: {stage_data['NPK_ratio'][1]}%")
             print(f"  K fertilizer ratio: {stage_data['NPK_ratio'][2]}%")
     
             # Check if any fertilizer is needed
             if stage_data['NPK_ratio'][0] > 0 or stage_data['NPK_ratio'][1] > 0 or stage_data['NPK_ratio'][2] > 0:
                 print(f"  N fertilizer needed: {n_fertilizer:.2f} kg/ha")
                 print(f"  P fertilizer needed: {p_fertilizer:.2f} kg/ha")
                 print(f"  K fertilizer needed: {k_fertilizer:.2f} kg/ha")
     
                 for fertilizer, amount in fertilizer_amounts.items():
                     print(f"    {fertilizer}: {amount:.2f} kg/ha")
             else:
                 print("  No fertilizer required.")
     
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
     
             # Append the dictionary to the list, even if no fertilizer is required
             fertilizer_plan_list.append(phase_data)
         print(fertilizer_plan_list)
         # Return the list containing all phases' data
         return fertilizer_plan_list
     
     
     
     



class NPKComplexFertilizerCalculator_grapes:
    def __init__(self, crop_name, soil_n, soil_p, soil_k, vine_age=None, biofertilizer=False):
        self.crop_name = crop_name  # Name of the crop
        self.soil_n = soil_n  # Current N/itrogen level (kg/ha)
        self.soil_p = soil_p  # Current Phosphorus level (kg/ha)
        self.soil_k = soil_k  # Current Potassium level (kg/ha)
        self.vine_age = vine_age  # Age of vines in years
        self.biofertilizer = biofertilizer  # Whether biofertilizer is used

        # Base NPK recommendations for grapes (kg/ha)
        # These values are for mature vines (4+ years)
        self.crop_n_needs = 120  # Recommended Nitrogen
        self.crop_p_needs = 50   # Recommended Phosphorus
        self.crop_k_needs = 150  # Recommended Potassium

        # Adjust nutrients based on vine age
        if vine_age is not None:
            self._adjust_npk_for_vine_age()

        # If biofertilizer is used, reduce nitrogen by 25%
        if self.biofertilizer:
            self.crop_n_needs *= 0.75

        # Initialize fuzzy variables
        self._initialize_fuzzy_system()

        # Growth stages with fertilizer recommendations for grapes
        self.growth_stages = {
            "Bud Break": {
                "days": (0, 30),
                "NPK": (20, 30, 20),
                "biofertilizer": True,
                "notes": "Early spring application"
            },
            "Flowering": {
                "days": (31, 60),
                "NPK": (30, 10, 30),
                "biofertilizer": True,
                "notes": "Critical for fruit set"
            },
            "Fruit Set": {
                "days": (61, 90),
                "NPK": (25, 5, 40),
                "biofertilizer": False,
                "notes": "Higher K requirement"
            },
            "Berry Development": {
                "days": (91, 120),
                "NPK": (25, 5, 40),
                "biofertilizer": False,
                "notes": "Continue K application"
            },
            "Veraison": {
                "days": (121, 150),
                "NPK": (10, 0, 20),
                "biofertilizer": False,
                "notes": "Reduce N, maintain K"
            },
            "Harvest": {
                "days": (151, 180),
                "NPK": (10, 0, 0),
                "biofertilizer": False,
                "notes": "Minimal fertilization"
            }
        }

        # NPK complex fertilizers and individual fertilizers
        self.fertilizers = {
            "10:26:26": {"N": 0.10, "P": 0.26, "K": 0.26},
            "12:32:16": {"N": 0.12, "P": 0.32, "K": 0.16},
            "15:15:15": {"N": 0.15, "P": 0.15, "K": 0.15},
            "Urea (46-0-0)": {"N": 0.46, "P": 0.0, "K": 0.0},
            "DAP (18-46-0)": {"N": 0.18, "P": 0.46, "K": 0.0},
            "MOP (0-0-60)": {"N": 0.0, "P": 0.0, "K": 0.60},
            "SOP (0-0-50)": {"N": 0.0, "P": 0.0, "K": 0.50},  # Preferred K source for grapes
            "SSP (0-16-0)": {"N": 0.0, "P": 0.16, "K": 0.0},
            "Calcium Nitrate": {"N": 0.155, "P": 0.0, "K": 0.0},  # Added for grape nutrition
            "Magnesium Sulfate": {"N": 0.0, "P": 0.0, "K": 0.0}   # Secondary nutrient
        }

        # Micronutrient management specific to grapes
        self.micronutrients = {
            "Zinc sulphate": {"dose": 15, "condition": "zinc_deficient"},
            "Ferrous sulphate": {"dose": 25, "condition": "iron_deficient"},
            "Boron": {"dose": 3, "condition": "boron_deficient"},
            "Magnesium sulphate": {"dose": 20, "condition": "magnesium_deficient"}
        }

    def _adjust_npk_for_vine_age(self):
        """Adjust NPK needs based on vine age"""
        if self.vine_age < 1:
            # Young vines (< 1 year)
            self.crop_n_needs *= 0.3
            self.crop_p_needs *= 0.4
            self.crop_k_needs *= 0.3
        elif self.vine_age < 2:
            # 1-2 year old vines
            self.crop_n_needs *= 0.5
            self.crop_p_needs *= 0.6
            self.crop_k_needs *= 0.5
        elif self.vine_age < 4:
            # 2-4 year old vines
            self.crop_n_needs *= 0.75
            self.crop_p_needs *= 0.8
            self.crop_k_needs *= 0.75

    def _initialize_fuzzy_system(self):
        # Define fuzzy variables with ranges appropriate for grapes
        self.n_needed = ctrl.Antecedent(np.arange(0, 151, 1), 'n_needed')
        self.p_needed = ctrl.Antecedent(np.arange(0, 101, 1), 'p_needed')
        self.k_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'k_needed')

        self.n_fertilizer = ctrl.Consequent(np.arange(0, 151, 1), 'n_fertilizer')
        self.p_fertilizer = ctrl.Consequent(np.arange(0, 101, 1), 'p_fertilizer')
        self.k_fertilizer = ctrl.Consequent(np.arange(0, 201, 1), 'k_fertilizer')

        # Membership functions for inputs (N, P, K needs)
        self.n_needed['low'] = fuzz.trimf(self.n_needed.universe, [0, 0, 60])
        self.n_needed['medium'] = fuzz.trimf(self.n_needed.universe, [40, 80, 120])
        self.n_needed['high'] = fuzz.trimf(self.n_needed.universe, [80, 150, 150])

        self.p_needed['low'] = fuzz.trimf(self.p_needed.universe, [0, 0, 25])
        self.p_needed['medium'] = fuzz.trimf(self.p_needed.universe, [15, 35, 55])
        self.p_needed['high'] = fuzz.trimf(self.p_needed.universe, [35, 100, 100])

        self.k_needed['low'] = fuzz.trimf(self.k_needed.universe, [0, 0, 75])
        self.k_needed['medium'] = fuzz.trimf(self.k_needed.universe, [50, 100, 150])
        self.k_needed['high'] = fuzz.trimf(self.k_needed.universe, [100, 200, 200])

        # Membership functions for outputs (fertilizer)
        self.n_fertilizer['low'] = fuzz.trimf(self.n_fertilizer.universe, [0, 0, 40])
        self.n_fertilizer['medium'] = fuzz.trimf(self.n_fertilizer.universe, [20, 60, 100])
        self.n_fertilizer['high'] = fuzz.trimf(self.n_fertilizer.universe, [60, 150, 150])

        self.p_fertilizer['low'] = fuzz.trimf(self.p_fertilizer.universe, [0, 0, 20])
        self.p_fertilizer['medium'] = fuzz.trimf(self.p_fertilizer.universe, [10, 30, 50])
        self.p_fertilizer['high'] = fuzz.trimf(self.p_fertilizer.universe, [30, 100, 100])

        self.k_fertilizer['low'] = fuzz.trimf(self.k_fertilizer.universe, [0, 0, 50])
        self.k_fertilizer['medium'] = fuzz.trimf(self.k_fertilizer.universe, [30, 75, 120])
        self.k_fertilizer['high'] = fuzz.trimf(self.k_fertilizer.universe, [75, 200, 200])

        # Define fuzzy rules
        self.rules = [
            ctrl.Rule(self.n_needed['low'] & self.p_needed['low'] & self.k_needed['low'],
                      (self.n_fertilizer['low'], self.p_fertilizer['low'], self.k_fertilizer['low'])),
            ctrl.Rule(self.n_needed['medium'] & self.p_needed['medium'] & self.k_needed['medium'],
                      (self.n_fertilizer['medium'], self.p_fertilizer['medium'], self.k_fertilizer['medium'])),
            ctrl.Rule(self.n_needed['high'] & self.p_needed['high'] & self.k_needed['high'],
                      (self.n_fertilizer['high'], self.p_fertilizer['high'], self.k_fertilizer['high'])),
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
        amounts = {}
        total_n_applied = total_p_applied = total_k_applied = 0
    
        # Prioritize SOP over MOP for grapes
        k_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["K"] > 0]
        if "SOP (0-0-50)" in k_fertilizers:
            k_fertilizers.remove("SOP (0-0-50)")
            k_fertilizers.insert(0, "SOP (0-0-50)")  # Put SOP first
    
        # Count available fertilizers with N, P, and K
        n_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["N"] > 0]
        p_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["P"] > 0]
        
        # Distribute nutrients with preference for grape-friendly fertilizers
        for fertilizer in n_fertilizers:
            n_content = self.fertilizers[fertilizer]["N"]
            n_share = n_fertilizer_needed / len(n_fertilizers)
            n_amount = n_share / n_content if n_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + n_amount
            total_n_applied += n_amount * n_content
    
        for fertilizer in p_fertilizers:
            p_content = self.fertilizers[fertilizer]["P"]
            p_share = p_fertilizer_needed / len(p_fertilizers)
            p_amount = p_share / p_content if p_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + p_amount
            total_p_applied += p_amount * p_content
    
        for fertilizer in k_fertilizers:
            k_content = self.fertilizers[fertilizer]["K"]
            k_share = k_fertilizer_needed / len(k_fertilizers)
            k_amount = k_share / k_content if k_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + k_amount
            total_k_applied += k_amount * k_content
    
        return amounts

    def display_fertilizer_plan(self):
        fertilizer_plan_list = []
        print("in display fertilizer plan")
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

            print(stage_data)

            # Store the data for this phase
            phase_data = {
                'phase': phase,
                'days': stage_data['days'],
                'n_fertilizer_needed': n_fertilizer,
                'p_fertilizer_needed': p_fertilizer,
                'k_fertilizer_needed': k_fertilizer,
                'specific_fertilizer_amounts': fertilizer_amounts
            }

            fertilizer_plan_list.append(phase_data)
        print(fertilizer_plan_list)
        return fertilizer_plan_list
calculator = NPKComplexFertilizerCalculator_grapes(
    crop_name="Maize", soil_n=40, soil_p=15, soil_k=20, biofertilizer=True
)

class NPKComplexFertilizerCalculator_maize:
    def __init__(self, crop_name, soil_n, soil_p, soil_k, biofertilizer=False):
        self.crop_name = crop_name  # Name of the crop
        self.soil_n = soil_n  # Current Nitrogen level (kg/ha)
        self.soil_p = soil_p  # Current Phosphorus level (kg/ha)
        self.soil_k = soil_k  # Current Potassium level (kg/ha)
        self.biofertilizer = biofertilizer  # Whether biofertilizer is used

        # Recommended NPK for maize from standard agricultural practices
        self.crop_n_needs = 150  # Recommended Nitrogen (kg/ha)
        self.crop_p_needs = 60   # Recommended Phosphorus (kg/ha)
        self.crop_k_needs = 80   # Recommended Potassium (kg/ha)

        # If biofertilizer is used, reduce nitrogen by 25%
        if self.biofertilizer:
            self.crop_n_needs *= 0.75

        # Initialize fuzzy variables
        self._initialize_fuzzy_system()

        # Growth stages with fertilizer recommendations for maize
        self.growth_stages = {
            "Seedling": {"days": (0, 20), "NPK": (30, 40, 20), "biofertilizer": True},  # Initial nutrients
            "Vegetative": {"days": (21, 55), "NPK": (60, 20, 30), "biofertilizer": True},  # Rapid growth phase
            "Tasseling": {"days": (56, 75), "NPK": (40, 0, 20), "biofertilizer": False},  # Critical stage
            "Grain Filling": {"days": (76, 105), "NPK": (20, 0, 10), "biofertilizer": False},  # Yield formation
            "Maturity": {"days": (106, 130), "NPK": (0, 0, 0)}  # No additional fertilizer
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
            "SSP (0-16-0)": {"N": 0.0, "P": 0.16, "K": 0.0},
            "TSP (0-44-0)": {"N": 0.0, "P": 0.44, "K": 0.0},
            "SOP (0-0-50)": {"N": 0.0, "P": 0.0, "K": 0.50}
        }

        # Micronutrient management specific to maize
        self.micronutrients = {
            "Zinc sulphate": {"dose": 25, "condition": "zinc_deficient"},
            "Ferrous sulphate": {"dose": 50, "condition": "iron_deficient"},
            "Boron": {"dose": 5, "condition": "boron_deficient"}
        }

    def _initialize_fuzzy_system(self):
        # Define fuzzy variables with ranges appropriate for maize
        self.n_needed = ctrl.Antecedent(np.arange(0, 201, 1), 'n_needed')
        self.p_needed = ctrl.Antecedent(np.arange(0, 101, 1), 'p_needed')
        self.k_needed = ctrl.Antecedent(np.arange(0, 101, 1), 'k_needed')

        self.n_fertilizer = ctrl.Consequent(np.arange(0, 201, 1), 'n_fertilizer')
        self.p_fertilizer = ctrl.Consequent(np.arange(0, 101, 1), 'p_fertilizer')
        self.k_fertilizer = ctrl.Consequent(np.arange(0, 101, 1), 'k_fertilizer')

        # Membership functions for inputs (N, P, K needs) - adjusted for maize
        self.n_needed['low'] = fuzz.trimf(self.n_needed.universe, [0, 0, 75])
        self.n_needed['medium'] = fuzz.trimf(self.n_needed.universe, [50, 100, 150])
        self.n_needed['high'] = fuzz.trimf(self.n_needed.universe, [100, 200, 200])

        self.p_needed['low'] = fuzz.trimf(self.p_needed.universe, [0, 0, 30])
        self.p_needed['medium'] = fuzz.trimf(self.p_needed.universe, [20, 40, 60])
        self.p_needed['high'] = fuzz.trimf(self.p_needed.universe, [40, 100, 100])

        self.k_needed['low'] = fuzz.trimf(self.k_needed.universe, [0, 0, 40])
        self.k_needed['medium'] = fuzz.trimf(self.k_needed.universe, [30, 50, 70])
        self.k_needed['high'] = fuzz.trimf(self.k_needed.universe, [50, 100, 100])

        # Membership functions for outputs (fertilizer) - adjusted for maize
        self.n_fertilizer['low'] = fuzz.trimf(self.n_fertilizer.universe, [0, 0, 50])
        self.n_fertilizer['medium'] = fuzz.trimf(self.n_fertilizer.universe, [30, 75, 125])
        self.n_fertilizer['high'] = fuzz.trimf(self.n_fertilizer.universe, [100, 200, 200])

        self.p_fertilizer['low'] = fuzz.trimf(self.p_fertilizer.universe, [0, 0, 20])
        self.p_fertilizer['medium'] = fuzz.trimf(self.p_fertilizer.universe, [15, 30, 45])
        self.p_fertilizer['high'] = fuzz.trimf(self.p_fertilizer.universe, [30, 100, 100])

        self.k_fertilizer['low'] = fuzz.trimf(self.k_fertilizer.universe, [0, 0, 30])
        self.k_fertilizer['medium'] = fuzz.trimf(self.k_fertilizer.universe, [20, 40, 60])
        self.k_fertilizer['high'] = fuzz.trimf(self.k_fertilizer.universe, [40, 100, 100])

        # Define fuzzy rules
        self.rules = [
            ctrl.Rule(self.n_needed['low'] & self.p_needed['low'] & self.k_needed['low'],
                      (self.n_fertilizer['low'], self.p_fertilizer['low'], self.k_fertilizer['low'])),
            ctrl.Rule(self.n_needed['medium'] & self.p_needed['medium'] & self.k_needed['medium'],
                      (self.n_fertilizer['medium'], self.p_fertilizer['medium'], self.k_fertilizer['medium'])),
            ctrl.Rule(self.n_needed['high'] & self.p_needed['high'] & self.k_needed['high'],
                      (self.n_fertilizer['high'], self.p_fertilizer['high'], self.k_fertilizer['high'])),
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
        amounts = {}
        total_n_applied = total_p_applied = total_k_applied = 0
    
        # Count available fertilizers with N, P, and K to distribute evenly
        n_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["N"] > 0]
        p_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["P"] > 0]
        k_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["K"] > 0]
        
        # Distribute N evenly across all nitrogen-heavy and balanced fertilizers
        for fertilizer in n_fertilizers:
            n_content = self.fertilizers[fertilizer]["N"]
            n_share = n_fertilizer_needed / len(n_fertilizers)  # Split nitrogen need evenly
            n_amount = n_share / n_content if n_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + n_amount
            total_n_applied += n_amount * n_content
    
        # Distribute P evenly across all phosphorus-heavy and balanced fertilizers
        for fertilizer in p_fertilizers:
            p_content = self.fertilizers[fertilizer]["P"]
            p_share = p_fertilizer_needed / len(p_fertilizers)  # Split phosphorus need evenly
            p_amount = p_share / p_content if p_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + p_amount
            total_p_applied += p_amount * p_content
    
        # Distribute K evenly across all potassium-heavy and balanced fertilizers
        for fertilizer in k_fertilizers:
            k_content = self.fertilizers[fertilizer]["K"]
            k_share = k_fertilizer_needed / len(k_fertilizers)  # Split potassium need evenly
            k_amount = k_share / k_content if k_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + k_amount
            total_k_applied += k_amount * k_content
    
        return amounts

    def display_fertilizer_plan(self):
        fertilizer_plan_list = []
        print("in display fertilizer plan")
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

            print(stage_data)

            # Store the data for this phase
            phase_data = {
                'phase': phase,
                'days': stage_data['days'],
                'n_fertilizer_needed': n_fertilizer,
                'p_fertilizer_needed': p_fertilizer,
                'k_fertilizer_needed': k_fertilizer,
                'specific_fertilizer_amounts': fertilizer_amounts
            }

            fertilizer_plan_list.append(phase_data)
        print(fertilizer_plan_list)
        return fertilizer_plan_list

# Example usage
# calculator = NPKComplexFertilizerCalculator_maize(
#     crop_name="Maize", soil_n=40, soil_p=15, soil_k=20, biofertilizer=True
# )
# calculator.display_fertilizer_plan()



class NPKComplexFertilizerCalculator_rice:
    def __init__(self, crop_name, soil_n, soil_p, soil_k, biofertilizer=False):
        self.crop_name = crop_name  # Name of the crop
        self.soil_n = soil_n  # Current Nitrogen level (kg/ha)
        self.soil_p = soil_p  # Current Phosphorus level (kg/ha)
        self.soil_k = soil_k  # Current Potassium level (kg/ha)
        self.biofertilizer = biofertilizer  # Whether biofertilizer is used

        # Recommended NPK for rice from standard agricultural practices
        self.crop_n_needs = 120  # Recommended Nitrogen (kg/ha)
        self.crop_p_needs = 40   # Recommended Phosphorus (kg/ha)
        self.crop_k_needs = 60   # Recommended Potassium (kg/ha)

        # If biofertilizer is used, reduce nitrogen by 25%
        if self.biofertilizer:
            self.crop_n_needs *= 0.75

        # Initialize fuzzy variables
        self._initialize_fuzzy_system()

        # Growth stages with fertilizer recommendations for rice
        self.growth_stages = {
            "Seedling": {"days": (0, 21), "NPK": (20, 50, 20), "biofertilizer": True},  # Initial nutrients
            "Tillering": {"days": (22, 45), "NPK": (40, 30, 20), "biofertilizer": True},  # Active tillering
            "Panicle Initiation": {"days": (46, 65), "NPK": (40, 20, 30), "biofertilizer": False},  # Critical stage
            "Heading": {"days": (66, 85), "NPK": (20, 0, 20), "biofertilizer": False},  # Grain formation
            "Ripening": {"days": (86, 110), "NPK": (0, 0, 10)}  # Maturity phase
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
            "SSP (0-16-0)": {"N": 0.0, "P": 0.16, "K": 0.0}
        }

        # Micronutrient management specific to rice
        self.micronutrients = {
            "Zinc sulphate": {"dose": 25, "condition": "zinc_deficient"},
            "Ferrous sulphate": {"dose": 50, "condition": "iron_deficient"},
            "Manganese sulphate": {"dose": 15, "condition": "manganese_deficient"}
        }

    def _initialize_fuzzy_system(self):
        # Define fuzzy variables with ranges appropriate for rice
        self.n_needed = ctrl.Antecedent(np.arange(0, 151, 1), 'n_needed')
        self.p_needed = ctrl.Antecedent(np.arange(0, 81, 1), 'p_needed')
        self.k_needed = ctrl.Antecedent(np.arange(0, 81, 1), 'k_needed')

        self.n_fertilizer = ctrl.Consequent(np.arange(0, 151, 1), 'n_fertilizer')
        self.p_fertilizer = ctrl.Consequent(np.arange(0, 81, 1), 'p_fertilizer')
        self.k_fertilizer = ctrl.Consequent(np.arange(0, 81, 1), 'k_fertilizer')

        # Membership functions for inputs (N, P, K needs) - adjusted for rice
        self.n_needed['low'] = fuzz.trimf(self.n_needed.universe, [0, 0, 60])
        self.n_needed['medium'] = fuzz.trimf(self.n_needed.universe, [40, 80, 120])
        self.n_needed['high'] = fuzz.trimf(self.n_needed.universe, [80, 150, 150])

        self.p_needed['low'] = fuzz.trimf(self.p_needed.universe, [0, 0, 20])
        self.p_needed['medium'] = fuzz.trimf(self.p_needed.universe, [15, 30, 45])
        self.p_needed['high'] = fuzz.trimf(self.p_needed.universe, [30, 80, 80])

        self.k_needed['low'] = fuzz.trimf(self.k_needed.universe, [0, 0, 30])
        self.k_needed['medium'] = fuzz.trimf(self.k_needed.universe, [20, 40, 60])
        self.k_needed['high'] = fuzz.trimf(self.k_needed.universe, [40, 80, 80])

        # Membership functions for outputs (fertilizer) - adjusted for rice
        self.n_fertilizer['low'] = fuzz.trimf(self.n_fertilizer.universe, [0, 0, 40])
        self.n_fertilizer['medium'] = fuzz.trimf(self.n_fertilizer.universe, [30, 60, 90])
        self.n_fertilizer['high'] = fuzz.trimf(self.n_fertilizer.universe, [70, 150, 150])

        self.p_fertilizer['low'] = fuzz.trimf(self.p_fertilizer.universe, [0, 0, 15])
        self.p_fertilizer['medium'] = fuzz.trimf(self.p_fertilizer.universe, [10, 25, 40])
        self.p_fertilizer['high'] = fuzz.trimf(self.p_fertilizer.universe, [30, 80, 80])

        self.k_fertilizer['low'] = fuzz.trimf(self.k_fertilizer.universe, [0, 0, 20])
        self.k_fertilizer['medium'] = fuzz.trimf(self.k_fertilizer.universe, [15, 30, 45])
        self.k_fertilizer['high'] = fuzz.trimf(self.k_fertilizer.universe, [35, 80, 80])

        # Define fuzzy rules
        self.rules = [
            ctrl.Rule(self.n_needed['low'] & self.p_needed['low'] & self.k_needed['low'],
              (self.n_fertilizer['low'], self.p_fertilizer['low'], self.k_fertilizer['low'])),
    ctrl.Rule(self.n_needed['medium'] & self.p_needed['medium'] & self.k_needed['medium'],
              (self.n_fertilizer['medium'], self.p_fertilizer['medium'], self.k_fertilizer['medium'])),
    ctrl.Rule(self.n_needed['high'] & self.p_needed['high'] & self.k_needed['high'],
              (self.n_fertilizer['high'], self.p_fertilizer['high'], self.k_fertilizer['high'])),

    # Catch-all rule for when inputs don't match any specific rule
    ctrl.Rule(self.n_needed['low'] | self.n_needed['medium'] | self.n_needed['high'],
              self.n_fertilizer['medium']),
    ctrl.Rule(self.p_needed['low'] | self.p_needed['medium'] | self.p_needed['high'],
              self.p_fertilizer['medium']),
    ctrl.Rule(self.k_needed['low'] | self.k_needed['medium'] | self.k_needed['high'],
              self.k_fertilizer['medium']),
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
        amounts = {}
        total_n_applied = total_p_applied = total_k_applied = 0
    
        # Count available fertilizers with N, P, and K to distribute evenly
        n_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["N"] > 0]
        p_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["P"] > 0]
        k_fertilizers = [fert for fert, nutr in self.fertilizers.items() if nutr["K"] > 0]
        
        # Distribute N evenly across all nitrogen-heavy and balanced fertilizers
        for fertilizer in n_fertilizers:
            n_content = self.fertilizers[fertilizer]["N"]
            n_share = n_fertilizer_needed / len(n_fertilizers)
            n_amount = n_share / n_content if n_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + n_amount
            total_n_applied += n_amount * n_content
    
        # Distribute P evenly across all phosphorus-heavy and balanced fertilizers
        for fertilizer in p_fertilizers:
            p_content = self.fertilizers[fertilizer]["P"]
            p_share = p_fertilizer_needed / len(p_fertilizers)
            p_amount = p_share / p_content if p_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + p_amount
            total_p_applied += p_amount * p_content
    
        # Distribute K evenly across all potassium-heavy and balanced fertilizers
        for fertilizer in k_fertilizers:
            k_content = self.fertilizers[fertilizer]["K"]
            k_share = k_fertilizer_needed / len(k_fertilizers)
            k_amount = k_share / k_content if k_content > 0 else 0
            amounts[fertilizer] = amounts.get(fertilizer, 0) + k_amount
            total_k_applied += k_amount * k_content
    
        return amounts

    def display_fertilizer_plan(self):
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

            # Store the data for this phase
            phase_data = {
                'phase': phase,
                'days': stage_data['days'],
                'n_fertilizer_needed': n_fertilizer,
                'p_fertilizer_needed': p_fertilizer,
                'k_fertilizer_needed': k_fertilizer,
                'specific_fertilizer_amounts': fertilizer_amounts
            }

            fertilizer_plan_list.append(phase_data)

        return fertilizer_plan_list

# # Example usage
# calculator = NPKComplexFertilizerCalculator_rice(
#     crop_name="Rice", soil_n=30, soil_p=10, soil_k=15, biofertilizer=True
# )
# calculator.display_fertilizer_plan()