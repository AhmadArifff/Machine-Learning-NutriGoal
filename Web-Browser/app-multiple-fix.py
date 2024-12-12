import pandas as pd
from flask import Flask, request, render_template, jsonify
import tensorflow as tf
import numpy as np
import joblib
import re
import uuid
from datetime import datetime

tf.config.set_visible_devices([], 'GPU')  # Disable GPU jika terdeteksi

print("Available devices:", tf.config.list_physical_devices('CPU'))


# Load scaler and models
scaler1 = joblib.load('models/scaler1.pkl')
scaler2 = joblib.load('models/scaler2.pkl')
model1 = tf.keras.models.load_model('models/model1.h5')
model2 = tf.keras.models.load_model('models/model2.h5')

# Load food dataset
food_data = pd.read_csv('../data/combine-dataset-kategori.csv')

# Initialize Flask
app = Flask(__name__)

ffn_counter = 1
ffp_counter = 1
rfboc_counter = 1
# Main function without accuracy_model1 and accuracy_model2 parameters
def output_model(age, height, weight, gender, activity_level, food_preference, diet_category, has_gastric_issue):
    try:
        threshold = 0.4  # Ambang batas 40%
        cols_to_check = food_data.columns[1:]  # Kecuali kolom "Name"
        proportion_empty = (food_data[cols_to_check] == 0).sum(axis=1) / len(cols_to_check)

        # Filter data dengan proporsi nilai kosong atau 0 <= 40%
        filtered_food_data = food_data[proportion_empty <= threshold]
        filtered_food_data['Name'] = filtered_food_data['Name'].apply(lambda x: re.sub(r'[^\w\s]', ' ', str(x)))
        filtered_food_data['Name'] = filtered_food_data['Name'].str.replace(r'\s+', ' ', regex=True)
        filtered_food_data = filtered_food_data.dropna(subset=['Calories'])
        filtered_food_data['Calories'] = pd.to_numeric(filtered_food_data['Calories'], errors='coerce').fillna(0)
        filtered_food_data = filtered_food_data.fillna(0)

        BMI = weight / ((height / 100) ** 2)
        ideal_weight = (height - 100) - (0.10 * (height - 100)) if gender == 0 else (height - 100) + (0.15 * (height - 100))
        ideal_BMI = ideal_weight / ((height / 100) ** 2)
        weight_difference = weight - ideal_weight

        BMR_input = pd.DataFrame({'age': [age], 'height(cm)': [height], 'weight(kg)': [weight], 'gender': [gender]})
        BMR_scaled = scaler2.transform(BMR_input)
        BMR = model2.predict(BMR_scaled)[0][0]

        activity_level_convert = {
            1 : 1.2,
            2 : 1.3,
            3 : 1.5,
            4 : 1.7,
            5 : 1.9
        }
        activity_convert = activity_level_convert.get(activity_level, "Unknown")
        input_data = pd.DataFrame({
            'age': [age],
            'height(cm)': [height],
            'weight(kg)': [weight],
            'gender': [gender],
            'BMI': [BMI],
            'BMR': [BMR],
            'activity_level': [activity_convert]
        })
        scaled_input1 = scaler1.transform(input_data)
        daily_calorie_needs = model1.predict(scaled_input1)[0][0]  # Ensure this line is reached

        # Filter food based on preference
        if food_preference:
            filtered_food = filtered_food_data[
                filtered_food_data['Name'].str.contains('|'.join(food_preference), case=False, na=False)
            ]
        else:
            return {"error": "No food preferences provided."}

        if filtered_food.empty:
            return {"error": f"No data found for food preference {food_preference}."}

        if diet_category.lower() == "vegan":
            filtered_food = filtered_food[filtered_food['Diet_Type'].str.contains("Vegan", case=False, na=False)]

        if has_gastric_issue:
            filtered_food = filtered_food[
                (filtered_food['Fat(g)'] < 10) & 
                (filtered_food['Carbohydrate(g)'] < 50) |
                (filtered_food['Protein(g)'] >= 50) & 
                (filtered_food['Cholesterol(mg)'] <= 300) & 
                (filtered_food['Sodium(mg)'] <= 2300) & 
                (filtered_food['Fiber(g)'] >= (25 if gender == 1 else 38)) & 
                (filtered_food['Sugar(g)'] <= 40) & 
                (~filtered_food['Name'].str.contains("spicy|acidic|citrus|orange|lemon|pineapple|tomato|onion|chocolate|cheese|nuts|tart|coffee|Alcohol|beer|wine|vodka", case=False, na=False))
            ]

        filtered_food = filtered_food[filtered_food['Calories'] <= (daily_calorie_needs / 10)]
        filtered_food = filtered_food.sort_values(by='Calories', ascending=False)
        cumulative_calories = 0
        cumulative_Protein = 0
        cumulative_Fat = 0
        cumulative_Carbohydrate = 0
        cumulative_Fiber = 0
        cumulative_Cholesterol = 0
        cumulative_Sodium = 0
        cumulative_Sugar = 0
        cumulative_SaturatedFat = 0
        recommended_food = []  # Use a list to collect food recommendations
        for _, row in filtered_food.iterrows():
            if len(recommended_food) < 10 and (cumulative_calories + row['Calories'] <= daily_calorie_needs):
                # recommended_food.append(row.to_dict())  # Append row as dictionary
                matched_preference = next((pref for pref in food_preference if pref.lower() in row['Name'].lower()), None)

                recommended_food.append({
                    'Name': row['Name'],
                    'Calories': row['Calories'],
                    'Protein(g)': row['Protein(g)'],
                    'Fat(g)': row['Fat(g)'],
                    'Carbohydrate(g)': row['Carbohydrate(g)'],
                    'Fiber(g)': row['Fiber(g)'],
                    'Cholesterol(mg)': row['Cholesterol(mg)'],
                    'Sodium(mg)': row['Sodium(mg)'],
                    'Sugar(g)': row['Sugar(g)'],
                    'SaturatedFat(g)': row['SaturatedFat(g)'],
                    'User Input': matched_preference if matched_preference else "Unknown"
                })
                cumulative_calories += row['Calories']
                cumulative_Protein += row['Protein(g)']
                cumulative_Fat += row['Fat(g)']
                cumulative_Carbohydrate += row['Carbohydrate(g)']
                cumulative_Fiber += row['Fiber(g)']
                cumulative_Cholesterol += row['Cholesterol(mg)']
                cumulative_Sodium += row['Sodium(mg)']
                cumulative_Sugar += row['Sugar(g)']
                cumulative_SaturatedFat += row['SaturatedFat(g)']
                if len(recommended_food) >= 10:
                    break

        if not recommended_food:
            return {"error": f"No recommended food meets the criteria for {food_preference}."}

        eating_pattern = 3 if activity_level > 2 else 2
        
        # Activity Level
        activity_level_mapping = {
            1: 1,
            2: 2,
            3: 3,
            4: 4,
            5: 5
        }
        activity_description = activity_level_mapping.get(activity_level, "Unknown")
        timestamp = datetime.now().isoformat()
        
        # Handle multiple food preferences
        favorite_food_names = []
        favorite_food_preferences = []
        rfp_id = 0
        user_id = 1
        global ffn_counter, ffp_counter, rfboc_counter  # Deklarasi variabel global
        # Assign unique IDs using counters
        ffn_id = ffn_counter
        ffp_id = ffp_counter
        rfboc_id = rfboc_counter
        
        # Increment counters
        ffn_counter += 1
        ffp_counter += 1
        rfboc_counter += 1
        # Loop through food preferences and generate favorite food entries
        for idx, name in enumerate(food_preference):
            favorite_food_names.append({
                "ffn_id": idx+1,  # Unique ID for each favorite food name
                "ffn_name": name,
                "ffn_created_at": timestamp,
                "ffn_updated_at": timestamp,
            })
            favorite_food_preferences.append({
                "ffp_id": idx+1,  # Unique ID for each favorite food preference
                "ffn_id": favorite_food_names[-1]["ffn_id"],  # Link to the corresponding favorite food name
                "ffp_name": name,
                "ffp_created_at": timestamp,
                "ffp_updated_at": timestamp,
            })
        
            # Prepare the response
            # "favorite_food_name": {
            #     "ffn_id": str(uuid.uuid4()),
            #     "ffn_name": food_preference,
            #     "ffn_created_at": timestamp,
            #     "ffn_updated_at": timestamp,
            # },
            # "favorite_food_preference": {
            #     "ffp_id": str(uuid.uuid4()),
            #     "ffn_id": str(uuid.uuid4()),
            #     "ffp_name": food_preference,
            #     "ffp_created_at": timestamp,
            #     "ffp_updated_at": timestamp,
            # },
            # Match recommended food with favorite food preferences
            # "recommended_food_preference": [
            #     {
            #         "rfp_id": str(uuid.uuid4()),
            #         "ffp_id": favorite_food_preferences[-1]["ffn_id"],  # Unique ID for each favorite food preference
            #         "rfboc_id": 1,
            #         **{k: v for k, v in row.items() if k in filtered_food.columns},
            #         "rfp_created_at": timestamp,
            #         "rfp_updated_at": timestamp,
            #     } for row in recommended_food
            # ],
            matched_recommended_food = []
            for row in recommended_food:
                # Check if recommended food matches any favorite food preference
                matched_preference = next(
                    (ffp for ffp in favorite_food_preferences if ffp["ffp_name"].lower() in row["Name"].lower()), None
                )
                if matched_preference:
                    rfp_id += 1 
                    matched_recommended_food.append({
                        "rfp_id": rfp_id,  # Unique ID for recommended food preference
                        # "ffp_id": matched_preference["ffp_id"],  # Link to the matched favorite food preference
                        "ffp_id": ffp_id,  # Link to the matched favorite food preference
                        "rfboc_id": 1,  # Example constant value
                        **{k: v for k, v in row.items() if k in filtered_food.columns},  # Copy relevant food columns
                        "rfp_created_at": timestamp,
                        "rfp_updated_at": timestamp,
                    })
        return {
            # "favorite_food_name": favorite_food_names,
            "favorite_food_name": {
                "ffn_id": ffn_id,
                "ffn_name": food_preference,
                "ffn_created_at": timestamp,
                "ffn_updated_at": timestamp,
            },
            # "favorite_food_preference": favorite_food_preferences,
            "favorite_food_preference": {
                "ffp_id": ffp_id,
                "ffn_id": ffn_id,
                "ffp_name": food_preference,
                "ffp_created_at": timestamp,
                "ffp_updated_at": timestamp,
            },
            "recommended_food_preference": matched_recommended_food,
            
            "recommended_food_based_on_calories": {
                "rfboc_id": rfboc_id,
                "user_id": user_id,
                "rfboc_diet_type": diet_category,
                "rfboc_history_of_gastritis_or_gerd": has_gastric_issue,
                "rfboc_age": age,
                "rfboc_height_(cm)": height,
                "rfboc_weight_(kg)": weight,
                "rfboc_gender": True if gender == 1 else False,
                "rfboc_activity_level": activity_description,
                "rfboc_meal_schedule_(day)": eating_pattern,
                "rfboc_daily_calorie_needs": f"{daily_calorie_needs:.2f}",
                "rfboc_bmr": f"{BMR:.2f}",
                "rfboc_bmi": f"{BMI:.2f}",
                "rfboc_ideal_weight": f"{ideal_weight:.2f}",
                "rfboc_ideal_bmi": f"{ideal_BMI:.2f}",
                "rfboc_weight_difference": f"{weight_difference:.2f}",
                "rfboc_total_calories_by_recommendation": f"{float(cumulative_calories):.2f}",  # Convert to float
                "rfboc_weight_difference": f"{float(weight_difference):.2f}",  # Convert to float
                "rfboc_total_protein_(g)": f"{cumulative_Protein:.2f}",
                "rfboc_total_fat_(g)": f"{cumulative_Fat:.2f}",
                "rfboc_total_carbohydrate_(g)": f"{cumulative_Carbohydrate:.2f}",
                "rfboc_total_fiber_(g)": f"{cumulative_Fiber:.2f}",
                "rfboc_total_cholesterol_(mg)": f"{cumulative_Cholesterol:.2f}",
                "rfboc_total_sodium_(mg)": f"{cumulative_Sodium:.2f}",
                "rfboc_total_sugar_(g)": f"{cumulative_Sugar:.2f}",
                "rfboc_total_saturated_fat_(g)": f"{cumulative_SaturatedFat:.2f}",  # Adjusted key to remove spaces
                "rfboc_created_at": timestamp,
                "rfboc_updated_at": timestamp,
            }
        }
    except Exception as e:
        return {"error": str(e)}

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    try:
        data = request.args if request.method == 'GET' else request.form

        # Ambil preferensi makanan
        food_preferences = data.getlist('food_preference') if request.method == 'GET' else data.getlist('food_preference[]')
        if not food_preferences:
            return jsonify({"error": "Missing food preference."}), 400

        # Ambil dan validasi input data
        age = int(data.get('age', 0))
        height = float(data.get('height', 0))
        weight = float(data.get('weight', 0))
        activity_level = int(data.get('activity_level', 0))
        diet_category = data.get('diet_category', '').strip()
        gender = data.get('rfboc_gender', '').lower() == 'true'
        has_gastric_issue = data.get('has_gastric_issue', '').lower() == 'true'

        # Pastikan input valid
        if not all([age, height, weight, activity_level, diet_category]):
            return jsonify({"error": "Incomplete input data."}), 400

        # Panggil model prediksi
        result = output_model(
            age, height, weight, gender, activity_level, food_preferences,
            diet_category, has_gastric_issue
        )

        return render_template(
            'result-multiple-fix.html',
            favorite_food_name=result['favorite_food_name'],
            favorite_food_preference=result['favorite_food_preference'],
            recommended_food_preference=result['recommended_food_preference'],
            recommended_food_based_on_calories=result['recommended_food_based_on_calories']
        )

    except Exception as e:
        return jsonify({"error": str(e)}), 500





@app.route('/history', methods=['GET', 'POST'])
def history():
    try:
        # Check Content-Type from the request
        if request.content_type == 'application/json':
            # Parsing data from JSON body
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid or missing JSON body."}), 400
            
            food_preferences = data.get('food_preference_recommendation', [])
            favorite_food_preference = data.get('favorite_food_preference', [])
        else:
            data = request.form  # Use form data
            print("Received form data:", data)  # Debug print
            return jsonify({"error": "Content-Type must be application/json"}), 400
        
        # Validate food preferences
        if not food_preferences:
            return jsonify({"error": "Missing food preference."}), 400
        
        # Extract data from JSON
        weight = float(data.get('weight')) if data.get('weight') else None
        age = int(data.get('age')) if data.get('age') else None
        height = int(data.get('height')) if data.get('height') else None
        selected_ids = food_preferences  # List of selected food preferences

        # Extract additional data from JSON
        all_rfp_ids = data.get('rfp_id', [])
        all_names = data.get('name', [])
        all_calories = data.get('calories', [])
        all_carbohydrate = data.get('carbohydrate(g)', [])
        all_protein = data.get('protein(g)', [])
        all_fat = data.get('fat(g)', [])
        rfboc_gender = data.get('rfboc_gender', False)
        user_id = data.get('user_id')
        
        # Extract nested JSON for recommended_food_based_on_calories
        recommended_food = data.get('recommended_food_based_on_calories', {})
        if not isinstance(recommended_food, dict):
            return jsonify({"error": "Invalid format for 'recommended_food_based_on_calories'"}), 400
        rfboc_meal_schedule_day = recommended_food.get('rfboc_meal_schedule_(day)', 0)  # Default to False
        rfboc_activity_level = recommended_food.get('rfboc_activity_level', 0)  # Default to 0
        rfboc_diet_type = recommended_food.get('rfboc_diet_type', 'unknown')  # Default to 'unknown'
        rfboc_history_of_gastritis_or_gerd = recommended_food.get('history_of_gastritis_or_gerd', False)  # Default to False
        
        # Validate input
        if not (weight and age and height and selected_ids):
            return jsonify({"error": "Missing or invalid input data"}), 400
        
        # Handle 'rfboc_history_of_gastritis_or_gerd' correctly
        rfboc_history_of_gastritis_or_gerd = data.get('rfboc_history_of_gastritis_or_gerd', False)

        # Filter foods based on selected IDs
        food_recommendation = []
        for i in range(len(all_rfp_ids)):
            if all_rfp_ids[i] in food_preferences:
                food = {
                    "hfr_id": i,
                    "hrfpd_id": 1,
                    "rfp_id": all_rfp_ids[i],
                    "hfr_name": all_names[i],
                    "hfr_calories": all_calories[i] if i < len(all_calories) else None,
                    "hfr_carbohydrate(g)": all_carbohydrate[i] if i < len(all_carbohydrate) else None,
                    "hfr_protein(g)": all_protein[i] if i < len(all_protein) else None,
                    "hfr_fat(g)": all_fat[i] if i < len(all_fat) else None
                }
                food_recommendation.append(food)

        # Create timestamp
        timestamp = datetime.utcnow().isoformat()

        # JSON output structure
        result = {
            "history_recommendation_food_per_day": {
                "hrfpd_id": 1,
                "user_id": user_id,
                "created_at": timestamp,
                "body_weight": weight,
                "age": age,
                "height": height,
                "rfboc_gender": rfboc_gender,
                "rfboc_activity_level": rfboc_activity_level,
                "rfboc_diet_type": rfboc_diet_type,
                "rfboc_history_of_gastritis_or_gerd": rfboc_history_of_gastritis_or_gerd,
                "rfboc_meal_schedule_day": rfboc_meal_schedule_day,
                "diet_time": timestamp
            },
            "history_food_recommendation": food_recommendation,
            "food_preference": favorite_food_preference,
        }

        return jsonify(result), 200

    except KeyError as e:
        return jsonify({"error": f"Missing key: {str(e)}"}), 400

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


# @app.route('/history', methods=['GET', 'POST'])
# def history():
#     if request.method == 'GET':
#         return jsonify({"message": "Endpoint history dapat menerima data melalui POST"}), 200
    
#     else:
#         data = request.form  # Use form data
#         print("Received form data:", data)  # Debug print
        
#         try:
#             # Ambil data dari form
#             weight = data.get('weight', type=float)
#             age = data.get('age', type=int)
#             height = data.get('height', type=int)
#             # Ambil ID makanan yang dipilih dari elemen select multiple
#             selected_ids = data.getlist('food_preference_recommendation[]')
            
#             # Ambil daftar semua rekomendasi makanan dari form
#             all_rfp_ids = data.getlist('rfp_id')
#             all_names = data.getlist('name')
#             all_calories = data.getlist('calories', type=float)
#             all_carbohydrate = data.getlist('carbohydrate(g)', type=float)
#             all_protein = data.getlist('protein(g)', type=float)
#             all_fat = data.getlist('fat(g)', type=float)
#             rfboc_gender = data.get('rfboc_gender')
#             rfboc_activity_level = data.get('rfboc_activity_level')
#             rfboc_diet_type = data.get('rfboc_diet_type')
#             user_id = data.get('user_id')
            
#             # Validasi input
#             if not (weight and age and height and selected_ids):
#                 return jsonify({"error": "Missing or invalid input data"}), 400
        
#             # # Pastikan 'rfboc_gender' di-handle dengan benar
#             # rfboc_gender = data.get('rfboc_gender', False)
#             # if isinstance(rfboc_gender, str):
#             #     rfboc_gender = rfboc_gender.lower() == 'true'
#             # elif not isinstance(rfboc_gender, bool):
#             #     rfboc_gender = False
            
            
#             # Pastikan 'has_gastric_issue' di-handle dengan benar
#             rfboc_history_of_gastritis_or_gerd = data.get('rfboc_history_of_gastritis_or_gerd', False)
#             if isinstance(rfboc_history_of_gastritis_or_gerd, str):
#                 rfboc_history_of_gastritis_or_gerd = rfboc_history_of_gastritis_or_gerd.lower() == 'true'
#             elif not isinstance(rfboc_history_of_gastritis_or_gerd, bool):
#                 rfboc_history_of_gastritis_or_gerd = False

#             # Filter makanan sesuai ID yang dipilih
#             food_recommendation = []
#             for i in range(len(all_rfp_ids)):
#                 if all_rfp_ids[i] in selected_ids:
#                     food = {
#                         "hfr_id": i,
#                         "hrfpd_id": 1,
#                         "rfp_id": all_rfp_ids[i],
#                         "hfr_name": all_names[i],
#                         "hfr_calories": all_calories[i] if i < len(all_calories) else None,
#                         "hfr_carbohydrate(g)": all_carbohydrate[i] if i < len(all_carbohydrate) else None,
#                         "hfr_protein(g)": all_protein[i] if i < len(all_protein) else None,
#                         "hfr_fat(g)": all_fat[i] if i < len(all_fat) else None
#                     }
#                     food_recommendation.append(food)

#             # Buat timestamp
#             timestamp = datetime.utcnow().isoformat()

#             # Struktur JSON output
#             result = {
#                 "history_recommendation_food_per_day": {
#                     "hrfpd_id": 1,
#                     "user_id": user_id,  # User ID statis
#                     "created_at": timestamp,
#                     "body_weight": weight,
#                     "age": age,
#                     "height": height,
#                     "rfboc_gender": True if rfboc_gender == 1 else False,
#                     "rfboc_activity_level": rfboc_activity_level,
#                     "rfboc_diet_type": rfboc_diet_type,
#                     "rfboc_history_of_gastritis_or_gerd": False if rfboc_history_of_gastritis_or_gerd else True,
#                     "created_at": timestamp,
#                     "diet_time": timestamp
#                 },
#                 "history_food_recommendation": food_recommendation,
#             }

#             return jsonify(result), 200

#         except Exception as e:
#             # Tangkap error lain dan kembalikan respons error
#             return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


    
    
# @app.route('/historytest', methods=['GET', 'POST'])
# def historytest():
#     try:
#         # Check Content-Type from the request
#         if request.content_type == 'application/json':
#             # Parsing data from JSON body
#             data = request.get_json()
#             if not data:
#                 data = request.form  # Use form data
#                 return jsonify({"error": "Invalid or missing JSON body."}), 400
            
#             food_preferences = data.get('food_preference_recommendation', [])
#             favorite_food_preference = data.get('favorite_food_preference', [])
#         else:
#             data = request.form  # Use form data
#             return jsonify({"error": "Content-Type must be application/json"}), 400
        
#         # Validate food preferences
#         if not food_preferences:
#             return jsonify({"error": "Missing food preference."}), 400
        
#         if not favorite_food_preference:
#             return jsonify({"error": "Food preferences are missing in the input data."}), 400

        
#         # Extract data from JSON
#         weight = float(data.get('weight')) if data.get('weight') else None
#         age = int(data.get('age')) if data.get('age') else None
#         height = int(data.get('height')) if data.get('height') else None
#         selected_ids = food_preferences  # List of selected food preferences

#         # Extract additional data from JSON
#         all_rfp_ids = data.get('rfp_id', [])
#         all_names = data.get('name', [])
#         all_calories = data.get('calories', [])
#         all_carbohydrate = data.get('carbohydrate(g)', [])
#         all_protein = data.get('protein(g)', [])
#         all_fat = data.get('fat(g)', [])
#         rfboc_gender = data.get('rfboc_gender', False)
#         user_id = data.get('user_id')
        
#         # Extract nested JSON for recommended_food_based_on_calories
#         recommended_food = data.get('recommended_food_based_on_calories', {})
#         if not isinstance(recommended_food, dict):
#             return jsonify({"error": "Invalid format for 'recommended_food_based_on_calories'"}), 400
#         rfboc_meal_schedule_day = recommended_food.get('rfboc_meal_schedule_(day)', 0)  # Default to False
#         rfboc_activity_level = recommended_food.get('rfboc_activity_level', 0)  # Default to 0
#         rfboc_diet_type = recommended_food.get('rfboc_diet_type', 'unknown')  # Default to 'unknown'
#         rfboc_history_of_gastritis_or_gerd = recommended_food.get('history_of_gastritis_or_gerd', False)  # Default to False
        
#         # Pastikan 'has_gastric_issue' di-handle dengan benar
#         rfboc_history_of_gastritis_or_gerd = data.get('rfboc_history_of_gastritis_or_gerd', False)
#         if isinstance(rfboc_history_of_gastritis_or_gerd, str):
#             rfboc_history_of_gastritis_or_gerd = rfboc_history_of_gastritis_or_gerd.lower() == 'true'
#         elif not isinstance(rfboc_history_of_gastritis_or_gerd, bool):
#             rfboc_history_of_gastritis_or_gerd = False
        
#         # Ambil data 'preference' dari elemen yang dihasilkan dengan perulangan
#         favorite_food_preference = []
#         index = 1  # Inisialisasi indeks untuk elemen input
#         while True:
#             ffp_id_key = f"ffp_id_{index}"
#             ffp_name_key = f"ffp_name_{index}"
            
#             # Cek apakah elemen berikutnya ada
#             ffp_id = data.get(ffp_id_key)
#             ffp_name = data.get(ffp_name_key)
            
#             if not ffp_id or not ffp_name:  # Jika data tidak ditemukan, keluar dari loop
#                 break
            
#             # Tambahkan data ke daftar preference
#             favorite_food_preference.append({
#                 "id": ffp_id,
#                 "name": ffp_name
#             })
#             index += 1  # Tingkatkan indeks


#         # Validasi input
#         if not (weight and age and height and selected_ids):
#             return jsonify({"error": "Missing or invalid input data"}), 400

#         # Filter makanan sesuai ID yang dipilih
#         food_recommendation = []
#         for i in range(len(all_rfp_ids)):
#             if all_rfp_ids[i] in selected_ids:
#                 food = {
#                     "hfr_id": i+1,
#                     "hrfpd_id": 1,
#                     "rfp_id": all_rfp_ids[i],
#                     "hfr_name": all_names[i],
#                     "hfr_calories": all_calories[i] if i < len(all_calories) else None,
#                     "hfr_carbohydrate(g)": all_carbohydrate[i] if i < len(all_carbohydrate) else None,
#                     "hfr_protein(g)": all_protein[i] if i < len(all_protein) else None,
#                     "hfr_fat(g)": all_fat[i] if i < len(all_fat) else None
#                 }
#                 food_recommendation.append(food)

#         # Buat timestamp
#         timestamp = datetime.utcnow().isoformat()

#         # Struktur JSON output
#         result = {
#             "user_id": user_id,
#             "rfboc_gender": True if rfboc_gender == 1 else False,
#             "history_recommendation_food_per_day": {
#                 "hrfpd_id": 1,
#                 "history_food_recommendation": food_recommendation,
#                 "food_preference": favorite_food_preference,
#                 "body_weight": weight,
#                 "age": age,
#                 "height": height,
#                 "rfboc_activity_level": rfboc_activity_level,
#                 "rfboc_diet_type": rfboc_diet_type,
#                 "rfboc_history_of_gastritis_or_gerd": False if rfboc_history_of_gastritis_or_gerd else True,
#                 "rfboc_meal_schedule_day": rfboc_meal_schedule_day,
#                 "created_at": timestamp,
#                 "diet_time": timestamp
#             },
#         }

#         return jsonify(result), 200

#     except Exception as e:
#         # Tangkap error lain dan kembalikan respons error
#         return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500


@app.route('/historytest', methods=['GET', 'POST'])
def historytest():
    try:
        if request.content_type == 'application/json':
            # Parsing data dari JSON body
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid or missing JSON body."}), 400
            
            # Ambil data dari JSON input
            weight = data.get('weight')
            height = data.get('height')
            age = data.get('age')
            user_id = data.get('user_id')
            gender = data.get('gender', False)
            food_preferences = data.get('food_preference_recommendation', [])
            favorite_food_preference = data.get('favorite_food_preference', [])
            recommended_food = data.get('recommended_food_based_on_calories', {})

            # Validasi input wajib
            if not all([weight, height, age, food_preferences]):
                return jsonify({"error": "Missing or invalid input data."}), 400

            # Validasi tipe data pada `recommended_food`
            if not isinstance(recommended_food, dict):
                return jsonify({"error": "Invalid format for 'recommended_food_based_on_calories'"}), 400

            # Ambil data dari recommended_food_based_on_calories
            activity_level = recommended_food.get('rfboc_activity_level', 0)
            diet_type = recommended_food.get('rfboc_diet_type', 'unknown')
            meal_schedule_day = recommended_food.get('rfboc_meal_schedule_(day)', 0)
            has_gastric_issue = recommended_food.get('history_of_gastritis_or_gerd', False)

            # Filter makanan sesuai ID preferensi
            all_rfp_ids = data.get('rfp_id', [])
            all_names = data.get('name', [])
            all_calories = data.get('calories', [])
            all_carbohydrate = data.get('carbohydrate(g)', [])
            all_protein = data.get('protein(g)', [])
            all_fat = data.get('fat(g)', [])
            food_recommendation = []

            for i in range(len(all_rfp_ids)):
                if all_rfp_ids[i] in food_preferences:
                    food = {
                        "hfr_id": i + 1,
                        "hrfpd_id": 1,
                        "rfp_id": all_rfp_ids[i],
                        "hfr_name": all_names[i] if i < len(all_names) else None,
                        "hfr_calories": all_calories[i] if i < len(all_calories) else None,
                        "hfr_carbohydrate(g)": all_carbohydrate[i] if i < len(all_carbohydrate) else None,
                        "hfr_protein(g)": all_protein[i] if i < len(all_protein) else None,
                        "hfr_fat(g)": all_fat[i] if i < len(all_fat) else None
                    }
                    food_recommendation.append(food)

            # Buat timestamp
            timestamp = datetime.utcnow().isoformat()

            # Struktur JSON output
            result = {
                "user_id": user_id,
                "rfboc_gender": gender,
                "history_recommendation_food_per_day": {
                    "hrfpd_id": 1,
                    "history_food_recommendation": food_recommendation,
                    "food_preference": favorite_food_preference,
                    "body_weight": weight,
                    "age": age,
                    "height": height,
                    "rfboc_activity_level": activity_level,
                    "rfboc_diet_type": diet_type,
                    "rfboc_history_of_gastritis_or_gerd": has_gastric_issue,
                    "rfboc_meal_schedule_day": meal_schedule_day,
                    "created_at": timestamp,
                    "diet_time": timestamp
                },
            }

            return jsonify(result), 200
        else:
            return jsonify({"error": "Content-Type must be application/json"}), 400

    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



    
    
@app.route('/predictjson', methods=['POST'])
def predictjson():
    try:
        # Cek Content-Type dari request
        if request.content_type == 'application/json':
            # Parsing data dari JSON body
            data = request.get_json()
            if not data:
                return jsonify({"error": "Invalid or missing JSON body."}), 400
            
            food_preferences = data.get('food_preference', [])  # List dari JSON
        else:
            # Parsing data dari form-data
            data = request.form
            food_preferences = request.form.getlist('food_preference[]')  # List dari form-data
        
        # Validasi food preferences
        if not food_preferences:
            return jsonify({"error": "Missing food preference."}), 400
        
        # Ambil data lainnya
        age = int(data.get('age', 0))
        height = float(data.get('height', 0))
        weight = float(data.get('weight', 0))
        gender = int(data.get('gender', 0))
        activity_level = int(data.get('activity_level', 0))
        diet_category = data.get('diet_category', '')  # Pastikan key ada
        
        # Pastikan 'has_gastric_issue' di-handle dengan benar
        has_gastric_issue = data.get('has_gastric_issue', False)
        if isinstance(has_gastric_issue, str):
            has_gastric_issue = has_gastric_issue.lower() == 'true'
        elif not isinstance(has_gastric_issue, bool):
            has_gastric_issue = False

        # Panggil fungsi utama
        result = output_model(
            age, height, weight, gender, activity_level, food_preferences,
            diet_category, has_gastric_issue
        )

        return jsonify(result)

    except KeyError as e:
        # Tentukan key yang hilang
        required_keys = ['age', 'height', 'weight', 'gender', 'activity_level', 'food_preference', 'diet_category']
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            return jsonify({"error": f"Missing keys: {', '.join(missing_keys)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500




@app.route('/')
def index():
    """
    Main application page.
    """
    return render_template('index-select-multiple-fix.html')


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=5000, debug=True)

