# from flask import Flask, request, jsonify
# from fertilizer_calculator import NPKComplexFertilizerCalculator

# app = Flask(__name__)

# @app.route('/', methods=['GET'])
# def hello():
#     return '<h1>hello</h>'
# # Fertilizer calculation route
# @app.route('/calculate_fertilizer', methods=['POST'])
# def calculate_fertilizer():
#     data = request.get_json()

#     # Check for required fields
#     required_fields = ['crop_name', 'soil_n', 'soil_p', 'soil_k']
#     for field in required_fields:
#         if field not in data:
#             return jsonify({"error": "Missing one or more required fields"}), 400

#     crop_name = data['crop_name']
#     soil_n = data['soil_n']
#     soil_p = data['soil_p']
#     soil_k = data['soil_k']

#     # Fertilizer requirement calculation logic
#     calculator = NPKComplexFertilizerCalculator(crop_name, soil_n, soil_p, soil_k)
    
#     # Calculate the fertilizer plan
#     fertilizer_plan = calculator.display_fertilizer_plan()

#     # Return the results as JSON
#     return jsonify({
#         "crop_name": crop_name,
#         "soil_n": soil_n,
#         "soil_p": soil_p,
#         "soil_k": soil_k,
#         "fertilizer_plan": fertilizer_plan
#     })


#     # Prepare response
   

# if __name__ == '__main__':
#     app.run(debug=True)
from flask import Flask, request, jsonify
from flask_cors import CORS
from fertilizer_calculator import NPKComplexFertilizerCalculator_sugarcane
from fertilizer_calculator import NPKComplexFertilizerCalculator_grapes
from fertilizer_calculator import NPKComplexFertilizerCalculator_maize
from fertilizer_calculator import NPKComplexFertilizerCalculator_rice

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
crops=['sugarcane','grape','maize','rice']

# Define a function to calculate the fertilizer plan
def calculate_fertilizer_plan(crop_name, soil_n, soil_p, soil_k):
    calculator = NPKComplexFertilizerCalculator_sugarcane(crop_name, soil_n, soil_p, soil_k)
    fertilizer_plan = calculator.display_fertilizer_plan()
    return fertilizer_plan


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the request
        data = request.get_json()
        crop_name = data.get('crop_name')
        if(crop_name not in crops):
            return jsonify({"message": "not valid "})
        soil_n = float(data.get('soil_n', 0))
        soil_p = float(data.get('soil_p', 0))
        soil_k = float(data.get('soil_k', 0))

        # Calculate the fertilizer plan
        global calculator
        global fertilizer_plan
        
        if( crop_name=='sugarcane'):
           calculator = NPKComplexFertilizerCalculator_sugarcane(crop_name, soil_n, soil_p, soil_k)
           print(crop_name)
           print(soil_n)
           print(soil_p)
           print(soil_k)

           fertilizer_plan = calculator.display_fertilizer_plan()
        elif crop_name=='grape':
           calculator = NPKComplexFertilizerCalculator_grapes(crop_name, soil_n, soil_p, soil_k)
           fertilizer_plan = calculator.display_fertilizer_plan()
           print(fertilizer_plan)
        elif crop_name=='maize':
              calculator = NPKComplexFertilizerCalculator_maize(crop_name, soil_n, soil_p, soil_k,biofertilizer=True)

              fertilizer_plan = calculator.display_fertilizer_plan()
        elif crop_name=='rice':
              calculator = NPKComplexFertilizerCalculator_rice(crop_name, soil_n, soil_p, soil_k,biofertilizer=True)

              fertilizer_plan = calculator.display_fertilizer_plan()
              
        

        # Return the fertilizer plan as JSON response
        return jsonify({
            'crop_name': crop_name,
            'soil_n': soil_n,
            'soil_p': soil_p,
            'soil_k': soil_k,
            'fertilizer_plan': fertilizer_plan
        })

    # Render a simple message for GET requests
    return jsonify({"message": "Welcome to the Fertilizer Calculator API. Please send a POST request with your data."})

if __name__ == '__main__':
    app.run(debug=True,port=5000)
