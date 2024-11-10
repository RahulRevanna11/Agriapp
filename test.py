import numpy as np
import skfuzzy as fuzz
from skfuzzy import control as ctrl

class NPKComplexFertilizerCalculator:
    def __init__(self, crop_name, soil_npk_ratio, ideal_soil_npk_ratio):
        self.crop_name = crop_name  # Name of the crop
        self.soil_n, self.soil_p, self.soil_k = soil_npk_ratio  # Current NPK ratio in the soil
        self.ideal_soil_n, self.ideal_soil_p, self.ideal_soil_k = ideal_soil_npk_ratio  # Ideal NPK ratio in the soil

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
            "Maturity": {"days": (211, 365), "NPK_ratio": (0, 0, 0)},
            "Harvesting": {"days": (366, 380), "NPK_ratio": (0, 0, 0)}
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
# Example of the update in action:
fertilizer_calculator = NPKComplexFertilizerCalculator(
    crop_name="Wheat", soil_npk_ratio=(0.1, 0.05, 0.12), ideal_soil_npk_ratio=(1.0, 0.067, 0.25)
)

fertilizer_calculator.display_fertilizer_plan()