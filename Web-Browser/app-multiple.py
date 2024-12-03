import pandas as pd
from flask import Flask, request, render_template, jsonify
import tensorflow as tf
import numpy as np
import joblib
import re

# Load scaler dan model
scaler1 = joblib.load('models/scaler1.pkl')
scaler2 = joblib.load('models/scaler2.pkl')
model1 = tf.keras.models.load_model('models/model1.h5')
model2 = tf.keras.models.load_model('models/model2.h5')

# Load dataset makanan
food_data = pd.read_csv('../data/combine-dataset-kategori.csv')

# Inisialisasi Flask
app = Flask(__name__)

def get_recommended_food(total_calories, food_data, food_preferences, max_results=10, sort_desc=False):
    """
    Mencari makanan dengan jumlah kalori kumulatif yang mendekati target.
    """
    threshold = 0.4  # Ambang batas 40%
    cols_to_check = food_data.columns[1:]  # Kecuali kolom "Name"
    proportion_empty = (food_data[cols_to_check] == 0).sum(axis=1) / len(cols_to_check)

    # Filter data dengan proporsi nilai kosong atau 0 <= 40%
    food_data = food_data[proportion_empty <= threshold]
    food_data['Name'] = food_data['Name'].apply(lambda x: re.sub(r'[^\w\s]', ' ', str(x)))
    food_data['Name'] = food_data['Name'].str.replace(r'\s+', ' ', regex=True)
    food_data = food_data.dropna(subset=['Calories'])
    food_data['Calories'] = pd.to_numeric(food_data['Calories'], errors='coerce').fillna(0)
    food_data = food_data.fillna(0)

    # Filter makanan berdasarkan preferensi
    filtered_food = food_data[
        food_data['Name'].str.contains('|'.join(food_preferences), case=False, na=False)
    ]

    if filtered_food.empty:
        return [], 0, 0, 0, 0, 0, 0, 0, 0, 0

    # Urutkan makanan berdasarkan kalori
    filtered_food = filtered_food.sort_values(by='Calories', ascending=not sort_desc)

    cumulative_calories = 0
    cumulative_Protein = 0
    cumulative_Fat = 0
    cumulative_Carbohydrate = 0
    cumulative_Fiber = 0
    cumulative_Cholesterol = 0
    cumulative_Sodium = 0
    cumulative_Sugar = 0
    cumulative_SaturatedFat = 0
    recommended_food = []

    for _, row in filtered_food.iterrows():
        if cumulative_calories + row['Calories'] <= total_calories:
            # Cari preferensi makanan pengguna yang sesuai dengan nama makanan
            matched_preference = next((pref for pref in food_preferences if pref.lower() in row['Name'].lower()), None)

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
        if len(recommended_food) == max_results:
            break

    return recommended_food, cumulative_calories, cumulative_Protein, cumulative_Fat, cumulative_Carbohydrate, cumulative_Fiber, cumulative_Cholesterol, cumulative_Sodium, cumulative_Sugar, cumulative_SaturatedFat




@app.route('/predictjson', methods=['POST', 'GET'])
def predictjson():
    try:
        # Parsing input data
        if request.method == 'POST':
            data = request.form
        else:  # Handle GET request
            data = request.args

        age = int(data.get('age'))
        height = float(data.get('height'))
        weight = float(data.get('weight'))
        gender = int(data.get('gender'))
        activity_level = int(data.get('activity_level'))
        food_preferences = data.getlist('food_preference[]')  # Multiple select

        # Activity Level
        activity_level_mapping = {
            1: "Sedentary (little to no exercise)",
            2: "Lightly active (light exercise 1-3 days/week)",
            3: "Moderately active (moderate exercise 3-5 days/week)",
            4: "Very active (hard exercise 6-7 days/week)",
            5: "Super active (very hard exercise or physical job)"
        }
        activity_description = activity_level_mapping.get(activity_level, "Unknown")

        # Hitung BMI
        BMI = weight / ((height / 100) ** 2)

        # Prediksi BMR
        BMR_input = np.array([[age, height, weight, gender]])
        BMR_scaled = scaler2.transform(BMR_input)
        BMR = float(model2.predict(BMR_scaled)[0][0])

        # Prediksi kebutuhan kalori harian
        input_data = np.array([[age, height, weight, gender, BMI, BMR, activity_level]])
        scaled_input = scaler1.transform(input_data)
        predicted_calories = float(model1.predict(scaled_input)[0][0])

        # # Rekomendasi makanan
        # recommended_food_calories, total_calories_daily = get_recommended_food(
        #     total_calories=predicted_calories,
        #     food_data=food_data,
        #     food_preferences=food_preferences
        # )

        # # Format hasil
        # results = {
        #     "Food Preference Analysis": food_preferences,
        #     "Predicted Daily Calorie Needs": f"{predicted_calories:.2f}",
        #     f"Recommended Food Based on Calories {total_calories_daily:.2f}": recommended_food_calories,
        # }
        # Rekomendasi makanan
        recommended_food_calories, cumulative_calories, cumulative_Protein, cumulative_Fat, cumulative_Carbohydrate, cumulative_Fiber, cumulative_Cholesterol, cumulative_Sodium, cumulative_Sugar, cumulative_SaturatedFat = get_recommended_food(
            total_calories=predicted_calories,
            food_data=food_data,
            food_preferences=food_preferences
        )
        # Format hasil
        results = {
            "Recommended Food Based on Calories": {
                "Age": age,
                "Height (cm)": height,
                "Weight (kg)": weight,
                "Gender": "Male" if gender == 1 else "Female",
                "Activity Level": activity_description,
                "Predicted Daily Calorie Needs": f"{predicted_calories:.2f}",
                "Total Calories": f"{cumulative_calories:.2f}",
                "Total Protein (g)": f"{cumulative_Protein:.2f}",
                "Total Fat (g)": f"{cumulative_Fat:.2f}",
                "Total Carbohydrate (g)": f"{cumulative_Carbohydrate:.2f}",
                "Total Fiber (g)": f"{cumulative_Fiber:.2f}",
                "Total Cholesterol (mg)": f"{cumulative_Cholesterol:.2f}",
                "Total Sodium (mg)": f"{cumulative_Sodium:.2f}",
                "Total Sugar (g)": f"{cumulative_Sugar:.2f}",
                "Total Saturated Fat (g)": f"{cumulative_SaturatedFat:.2f}"
            },
            "Food Preference Analysis": food_preferences,
            "Recommended Food": recommended_food_calories,
            
            
        }


        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)})



    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Input data
        age = float(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        gender = int(request.form['gender'])
        activity_level = float(request.form['activity_level'])
        food_preference = request.form['food_preference']

        # Hitung BMI dan prediksi kalori
        BMI = weight / ((height / 100) ** 2)
        BMR_input = np.array([[age, height, weight, gender]])
        BMR_scaled = scaler2.transform(BMR_input)
        BMR = float(model2.predict(BMR_scaled)[0][0])
        input_data = np.array([[age, height, weight, gender, BMI, BMR, activity_level]])
        scaled_input1 = scaler1.transform(input_data)
        daily_calorie_needs = float(model1.predict(scaled_input1)[0][0])

        # Makanan berdasarkan kalori terbesar
        high_cal_food, total_high_cal = get_recommended_food(
            total_calories=daily_calorie_needs,
            food_data=food_data,
            food_preference=food_preference,
            sort_desc=True
        )

        # Render HTML
        return render_template(
            'result.html',
            age=age,
            height=height,
            weight=weight,
            gender="Male" if gender == 0 else "Female",
            activity_level=activity_level,
            food_preference=food_preference,
            BMR=BMR,
            daily_calorie_needs=daily_calorie_needs,
            high_cal_food=high_cal_food,
            total_high_cal=total_high_cal,
        )
    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/')
def index():
    """
    Halaman utama aplikasi.
    """
    return render_template('index-select-multiple.html')


if __name__ == '__main__':
    app.run(debug=True)
