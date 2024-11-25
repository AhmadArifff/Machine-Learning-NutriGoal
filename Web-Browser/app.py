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
food_data = pd.read_csv('../data/combine-dataset.csv')

# Inisialisasi Flask
app = Flask(__name__)

def get_recommended_food(total_calories, food_data, food_preference, max_results=10, sort_desc=False):
    """
    Mencari makanan dengan jumlah kalori kumulatif yang mendekati target.
    """
    # Menghitung proporsi nilai kosong atau 0
    threshold = 0.4  # Ambang batas 40%
    cols_to_check = food_data.columns[1:]  # Kecuali kolom "Name"
    proportion_empty = (food_data[cols_to_check] == 0).sum(axis=1) / len(cols_to_check)

    # Filter data dengan proporsi nilai kosong atau 0 <= 40%
    food_data = food_data[proportion_empty <= threshold]
    food_data['Name'] = food_data['Name'].apply(lambda x: re.sub(r'[^\w\s]', ' ', str(x)))
    # Normalisasi spasi ganda menjadi satu spasi di kolom 'Name'
    food_data['Name'] = food_data['Name'].str.replace(r'\s+', ' ', regex=True)
    
    # Pastikan kolom yang terlibat dalam perhitungan adalah numerik dan tidak kosong
    food_data = food_data.dropna(subset=['Calories'])
    food_data['Calories'] = pd.to_numeric(food_data['Calories'], errors='coerce').fillna(0)

    # Pastikan tidak ada nilai NaN atau 0 di kolom lainnya
    food_data = food_data.fillna(0)

    # Filter data berdasarkan preferensi
    filtered_food = food_data[food_data['Name'].str.contains(food_preference, case=False, na=False)]
    if filtered_food.empty:
        return [], 0

    # Urutkan berdasarkan kalori (naik atau turun)
    filtered_food = filtered_food.sort_values(by='Calories', ascending=not sort_desc)

    # Inisialisasi
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
        if len(recommended_food) == max_results:
            break

    return recommended_food, cumulative_calories




@app.route('/')
def index():
    """
    Halaman utama aplikasi.
    """
    return render_template('index.html')


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
        # recommended_food_bmr = get_recommended_food(BMR, food_data, food_preference)
        recommended_food_calories = get_recommended_food(daily_calorie_needs, food_data, food_preference)

        # Correct sum calculation for Calories
        total_calories_daily = sum(item['Calories'] for item in recommended_food_calories[0]) if recommended_food_calories[0] else 0

        # Format hasil
        results = {
            "BMR": f"{BMR:.2f}",
            "Daily Calorie Needs": f"{daily_calorie_needs:.2f}",
            "Food Preference Analysis": f"{food_preference}",
            f"Recommended Food Based on Calories By Daily Calorie Needs {total_calories_daily:.2f}": recommended_food_calories[0],
            "Total Calories By Daily Calorie Needs": total_calories_daily,
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




if __name__ == '__main__':
    app.run(debug=True)
