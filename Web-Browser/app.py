import pandas as pd
from flask import Flask, request, render_template, jsonify
import tensorflow as tf
import numpy as np
import joblib

# Load scaler dan model
scaler1 = joblib.load('models/scaler1.pkl')
scaler2 = joblib.load('models/scaler2.pkl')
model1 = tf.keras.models.load_model('models/model1.h5')
model2 = tf.keras.models.load_model('models/model2.h5')

# Load dataset makanan
food_data = pd.read_csv('../data/combine-dataset.csv')

# Inisialisasi Flask
app = Flask(__name__)

@app.route('/')
def index():
    """
    Halaman utama aplikasi.
    """
    return render_template('index.html')

def get_recommended_food(total_calories, food_data, food_preference, tolerance=50):
    """
    Mencari makanan dengan jumlah kalori kumulatif yang mendekati target.
    """
    # Filter berdasarkan preferensi makanan
    filtered_food = food_data[food_data['Name'].str.contains(food_preference, case=False, na=False)]
    if filtered_food.empty:
        return []

    # Urutkan berdasarkan kalori dalam urutan naik
    filtered_food = filtered_food.sort_values(by='Calories')

    # Inisialisasi kumulatif
    cumulative_calories = 0
    recommended_food = []

    for _, row in filtered_food.iterrows():
        if cumulative_calories + row['Calories'] <= total_calories:
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
                'SaturatedFat(g)': row['SaturatedFat(g)']
            })
            cumulative_calories += row['Calories']
        else:
            break

    return recommended_food

@app.route('/predictjson', methods=['POST'])
def predictjson():
    try:
        # Input data dari pengguna
        age = float(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        gender = int(request.form['gender'])
        activity_level = float(request.form['activity_level'])
        food_preference = request.form['food_preference']

        # Hitung BMI
        BMI = weight / ((height / 100) ** 2)

        # Prediksi BMR
        BMR_input = np.array([[age, height, weight, gender]])
        BMR_scaled = scaler2.transform(BMR_input)
        BMR = float(model2.predict(BMR_scaled)[0][0])

        # Prediksi kebutuhan kalori harian
        input_data = np.array([[age, height, weight, gender, BMI, BMR, activity_level]])
        scaled_input1 = scaler1.transform(input_data)
        daily_calorie_needs = float(model1.predict(scaled_input1)[0][0])

        # Rekomendasi makanan
        recommended_food_bmr = get_recommended_food(BMR, food_data, food_preference)
        recommended_food_calories = get_recommended_food(daily_calorie_needs, food_data, food_preference)

        # Format hasil
        results = {
            "Daily Calorie Needs": f"{daily_calorie_needs:.2f}",
            "BMR": f"{BMR:.2f}",
            "Food Preference Analysis": f"User prefers {food_preference}. Suggested recipes include healthy options tailored for this preference.",
            f"Recommended Food Based on Calories By BMR {sum(item['Calories'] for item in recommended_food_bmr):.2f}": recommended_food_bmr,
            "Total Calories By BMR": sum(item['Calories'] for item in recommended_food_bmr),
            f"Recommended Food Based on Calories By Daily Calorie Needs {sum(item['Calories'] for item in recommended_food_calories):.2f}": recommended_food_calories,
            "Total Calories By Daily Calorie Needs": sum(item['Calories'] for item in recommended_food_calories)
        }

        return jsonify(results)

    except Exception as e:
        return jsonify({"error": str(e)})
    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Input data dari pengguna
        age = float(request.form['age'])
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        gender = int(request.form['gender'])
        activity_level = float(request.form['activity_level'])
        food_preference = request.form['food_preference']

        # Hitung BMI
        BMI = weight / ((height / 100) ** 2)

        # Prediksi BMR
        BMR_input = np.array([[age, height, weight, gender]])
        BMR_scaled = scaler2.transform(BMR_input)
        BMR = float(model2.predict(BMR_scaled)[0][0])

        # Prediksi kebutuhan kalori harian
        input_data = np.array([[age, height, weight, gender, BMI, BMR, activity_level]])
        scaled_input1 = scaler1.transform(input_data)
        daily_calorie_needs = float(model1.predict(scaled_input1)[0][0])

        # Rekomendasi makanan
        recommended_food_bmr = get_recommended_food(BMR, food_data, food_preference)
        recommended_food_calories = get_recommended_food(daily_calorie_needs, food_data, food_preference)

        # Render result.html dengan data hasil
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
            recommended_food_bmr=recommended_food_bmr,
            recommended_food_calories=recommended_food_calories,
        )

    except Exception as e:
        return jsonify({"error": str(e)})


if __name__ == '__main__':
    app.run(debug=True)
