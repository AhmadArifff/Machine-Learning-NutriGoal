import pandas as pd
from flask import Flask, request, render_template, jsonify
import tensorflow as tf
import numpy as np
import joblib
import re
import uuid
from datetime import datetime

# Load scaler and models
scaler1 = joblib.load('models/scaler1.pkl')
scaler2 = joblib.load('models/scaler2.pkl')
model1 = tf.keras.models.load_model('models/model1.h5')
model2 = tf.keras.models.load_model('models/model2.h5')

# Load food dataset
food_data = pd.read_csv('../data/combine-dataset-kategori.csv')

# Initialize Flask
app = Flask(__name__)

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
            1: "1. Sedentary (little to no exercise)",
            2: "2. Lightly active (light exercise 1-3 days/week)",
            3: "3. Moderately active (moderate exercise 3-5 days/week)",
            4: "4. Very active (hard exercise 6-7 days/week)",
            5: "5. Super active (very hard exercise or physical job)"
        }
        activity_description = activity_level_mapping.get(activity_level, "Unknown")
        timestamp = datetime.now().isoformat()
        
        # Handle multiple food preferences
        favorite_food_names = []
        favorite_food_preferences = []
        
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
                    matched_recommended_food.append({
                        "rfp_id": str(uuid.uuid4()),  # Unique ID for recommended food preference
                        "ffp_id": matched_preference["ffp_id"],  # Link to the matched favorite food preference
                        "rfboc_id": 1,  # Example constant value
                        **{k: v for k, v in row.items() if k in filtered_food.columns},  # Copy relevant food columns
                        "rfp_created_at": timestamp,
                        "rfp_updated_at": timestamp,
                    })
        return {
            "favorite_food_name": favorite_food_names,
            "favorite_food_preference": favorite_food_preferences,
            "recommended_food_preference": matched_recommended_food,
            
            "recommended_food_based_on_calories": {
                "rfboc_id": 1,
                "user_id": 1,
                "rfboc_diet_type": diet_category,
                "rfboc_history_of_gastritis_or_gerd": "Yes" if has_gastric_issue else "No",
                "rfboc_age": age,
                "rfboc_height_(cm)": height,
                "rfboc_weight_(kg)": weight,
                "rfboc_gender": "Male" if gender == 1 else "Female",
                "rfboc_activity_level": activity_description,
                "rfboc_meal_schedule(day)": eating_pattern,
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
        if request.method == 'GET':
            data = request.args  # Use query parameters
            # Parse food preferences for GET
            food_preferences = data.getlist('food_preference')  # Handle multiple `food_preference` keys
        else:
            data = request.form  # Use form data
            # Parse food preferences for POST
            food_preferences = request.form.getlist('food_preference[]')  # Handle form list

        # Ensure food preferences exist
        if not food_preferences:
            return jsonify({"error": "Missing food preference."}), 400

        # Ensure all required data is available
        age = int(data['age'])
        height = float(data['height'])
        weight = float(data['weight'])
        gender = int(data['gender'])
        activity_level = int(data['activity_level'])
        diet_category = data['diet_category']  # Ensure this key is available
        has_gastric_issue = data.get('has_gastric_issue', 'false').lower() == 'true'

        # Call the main function with the correct parameters
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

    except KeyError as e:
        required_keys = ['age', 'height', 'weight', 'gender', 'activity_level', 'food_preference', 'diet_category']
        missing_keys = [key for key in required_keys if key not in data]
        if missing_keys:
            return jsonify({"error": f"Missing keys: {', '.join(missing_keys)}"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/history', methods=['POST'])
def history():
    try:
        # Ambil data dari form
        weight = request.form.get('weight', type=float)
        age = request.form.get('age', type=int)
        height = request.form.get('height', type=int)
        
        # Ambil ID makanan yang dipilih dari elemen select multiple
        selected_ids = request.form.getlist('food_preference_recommendation[]')
        
        # Ambil daftar semua rekomendasi makanan dari form
        all_rfp_ids = request.form.getlist('rfp_id')
        all_names = request.form.getlist('name')
        all_calories = request.form.getlist('calories', type=float)
        all_carbohydrate = request.form.getlist('carbohydrate(g)', type=float)
        all_protein = request.form.getlist('protein(g)', type=float)
        all_fat = request.form.getlist('fat(g)', type=float)

        # Validasi input
        if not (weight and age and height and selected_ids):
            return jsonify({"error": "Missing or invalid input data"}), 400

        # Filter makanan sesuai ID yang dipilih
        food_recommendation = []
        for i in range(len(all_rfp_ids)):
            if all_rfp_ids[i] in selected_ids:
                food = {
                    "hfr_id": i,
                    "hrf_id": 1,
                    "rfp_id": all_rfp_ids[i],
                    "hfr_name": all_names[i],
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
            "history_recommendation_food_per_day": {
                "hrf_id": 1,
                "user_id": 1,  # User ID statis
                "created_at": timestamp,
                "body_weight": weight,
                "age": age,
                "height": height,
                "created_at": timestamp,
                "diet_time": timestamp
            },
            "history_food_recommendation": food_recommendation,
        }

        return jsonify(result), 200

    except Exception as e:
        # Tangkap error lain dan kembalikan respons error
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500



    
    
@app.route('/predictjson', methods=['POST'])
def predictjson():
    try:
        # Parsing input data
        data = request.form

        # Get food preference as a list
        food_preferences = request.form.getlist('food_preference[]')  # Capture food preferences
        if not food_preferences:
            return jsonify({"error": "Missing food preference."}), 400
        
        # Ensure all required data is available
        age = int(data['age'])
        height = float(data['height'])
        weight = float(data['weight'])
        gender = int(data['gender'])
        activity_level = int(data['activity_level'])
        diet_category = data['diet_category']  # Ensure this key is available
        has_gastric_issue = data.get('has_gastric_issue', 'false').lower() == 'true'
        

        # Call the main function with the correct parameters
        result = output_model(
            age, height, weight, gender, activity_level, food_preferences,
            diet_category, has_gastric_issue
        )

        return jsonify(result)

    except KeyError as e:
        required_keys = ['age', 'height', 'weight', 'gender', 'activity_level', 'food_preference[]', 'diet_category']
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
    app.run(debug=True)
