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
from fertilizer_calculator import NPKComplexFertilizerCalculator

app = Flask(__name__)
CORS(app)

# Define a function to calculate the fertilizer plan
def calculate_fertilizer_plan(crop_name, soil_n, soil_p, soil_k):
    calculator = NPKComplexFertilizerCalculator(crop_name, soil_n, soil_p, soil_k)
    fertilizer_plan = calculator.display_fertilizer_plan()
    return fertilizer_plan

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get data from the request
        data = request.get_json()
        crop_name = data.get('crop_name')
        soil_n = int(data.get('soil_n', 0))
        soil_p = int(data.get('soil_p', 0))
        soil_k = int(data.get('soil_k', 0))

        # Calculate the fertilizer plan
        fertilizer_plan = calculate_fertilizer_plan(crop_name, soil_n, soil_p, soil_k)

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
    app.run(debug=True)
