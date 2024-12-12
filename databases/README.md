# Database Schema: Food Recommendation System

Dokumen ini menjelaskan struktur database untuk **Food Recommendation System**, termasuk tabel-tabel dan hubungan antar tabelnya.

## Tables

### 1. `favorite_food_name`
Tabel ini menyimpan informasi mengenai nama makanan favorit.

| Column Name      | Data Type     | Constraints                                  |
| ----------------- | -------------| ------------------------------------------- |
| `ffn_id`         | INT          | Primary Key, AUTO_INCREMENT                 |
| `ffn_name`       | VARCHAR(255) | NOT NULL                                    |
| `ffn_created_at` | DATETIME     | DEFAULT CURRENT_TIMESTAMP                   |
| `ffn_updated_at` | DATETIME     | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

---

### 2. `favorite_food_preference`
Tabel ini menyimpan informasi preferensi makanan favorit yang terkait dengan nama makanan.

| Column Name      | Data Type     | Constraints                                  |
| ----------------- | -------------| ------------------------------------------- |
| `ffp_id`         | INT          | Primary Key, AUTO_INCREMENT                 |
| `ffn_id`         | INT          | Foreign Key -> `favorite_food_name(ffn_id)` |
| `ffp_name`       | VARCHAR(255) | NOT NULL                                    |
| `ffp_created_at` | DATETIME     | DEFAULT CURRENT_TIMESTAMP                   |
| `ffp_updated_at` | DATETIME     | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

---

### 3. `recommended_food_based_on_calories`
Tabel ini menyimpan informasi rekomendasi makanan berdasarkan kebutuhan kalori pengguna.

| Column Name                          | Data Type     | Constraints                                  |
| ------------------------------------ | ------------- | ------------------------------------------- |
| `rfboc_id`                           | INT           | Primary Key, AUTO_INCREMENT                 |
| `user_id`                            | INT           |                                             |
| `rfboc_diet_type`                    | VARCHAR(255)  | NOT NULL                                    |
| `rfboc_history_of_gastritis_or_gerd` | BOOLEAN       | NOT NULL                                    |
| `rfboc_age`                          | INT           | NOT NULL                                    |
| `rfboc_height_cm`                    | FLOAT         | NOT NULL                                    |
| `rfboc_weight_kg`                    | FLOAT         | NOT NULL                                    |
| `rfboc_gender`                       | BOOLEAN       | NOT NULL                                    |
| `rfboc_activity_level`               | INT           | NOT NULL                                    |
| `rfboc_meal_schedule_day`            | INT           | NOT NULL                                    |
| `rfboc_daily_calorie_needs`          | FLOAT         | NOT NULL                                    |
| `rfboc_bmr`                          | FLOAT         | NOT NULL                                    |
| `rfboc_bmi`                          | FLOAT         | NOT NULL                                    |
| `rfboc_ideal_weight`                 | FLOAT         | NOT NULL                                    |
| `rfboc_ideal_bmi`                    | FLOAT         | NOT NULL                                    |
| `rfboc_weight_difference`            | FLOAT         | NOT NULL                                    |
| `rfboc_total_calories_by_recommendation` | FLOAT     | NOT NULL                                    |
| `rfboc_total_protein_g`              | FLOAT         | NOT NULL                                    |
| `rfboc_total_fat_g`                  | FLOAT         | NOT NULL                                    |
| `rfboc_total_carbohydrate_g`         | FLOAT         | NOT NULL                                    |
| `rfboc_total_fiber_g`                | FLOAT         | NOT NULL                                    |
| `rfboc_total_cholesterol_mg`         | FLOAT         | NOT NULL                                    |
| `rfboc_total_sodium_mg`              | FLOAT         | NOT NULL                                    |
| `rfboc_total_sugar_g`                | FLOAT         | NOT NULL                                    |
| `rfboc_total_saturated_fat_g`        | FLOAT         | NOT NULL                                    |
| `rfboc_created_at`                   | DATETIME      | DEFAULT CURRENT_TIMESTAMP                   |
| `rfboc_updated_at`                   | DATETIME      | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

---

### 4. `recommended_food_preference`
Tabel ini menyimpan makanan yang direkomendasikan berdasarkan preferensi pengguna.

| Column Name      | Data Type     | Constraints                                  |
| ----------------- | -------------| ------------------------------------------- |
| `rfp_id`         | VARCHAR(255) | Primary Key                                  |
| `rfboc_id`       | INT          | Foreign Key -> `recommended_food_based_on_calories(rfboc_id)` |
| `ffp_id`         | INT          | Foreign Key -> `favorite_food_preference(ffp_id)` |
| `name`           | VARCHAR(255) | NOT NULL                                    |
| `calories`       | FLOAT        | NOT NULL                                    |
| `protein_g`      | FLOAT        | NOT NULL                                    |
| `fat_g`          | FLOAT        | NOT NULL                                    |
| `carbohydrate_g` | FLOAT        | NOT NULL                                    |
| `fiber_g`        | FLOAT        | NOT NULL                                    |
| `cholesterol_mg` | FLOAT        | NOT NULL                                    |
| `sodium_mg`      | FLOAT        | NOT NULL                                    |
| `sugar_g`        | FLOAT        | NOT NULL                                    |
| `saturated_fat_g`| FLOAT        | NOT NULL                                    |
| `rfp_created_at` | DATETIME     | DEFAULT CURRENT_TIMESTAMP                   |
| `rfp_updated_at` | DATETIME     | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

---

### 5. `history_recommendation_food_per_day`
Tabel ini menyimpan riwayat rekomendasi makanan pengguna per hari.

| Column Name        | Data Type    | Constraints                                  |
| -------------------| -------------| ------------------------------------------- |
| `hrfpd_id`         | INT          | Primary Key, AUTO_INCREMENT                 |
| `user_id`          | INT          |                                             |
| `age`              | INT          | NOT NULL                                    |
| `body_weight`      | DECIMAL(10,2)| NOT NULL                                    |
| `height`           | DECIMAL(10,2)| NOT NULL                                    |
| `diet_time`        | DATETIME     |                                             |
| `created_at`       | DATETIME     | DEFAULT CURRENT_TIMESTAMP                   |
| `rfboc_activity_level` | INT      | NOT NULL                                    |
| `rfboc_diet_type`  | VARCHAR(50)  | NOT NULL                                    |
| `rfboc_gender`     | BOOLEAN      | NOT NULL                                    |
| `rfboc_history_of_gastritis` | BOOLEAN | NOT NULL                                  |
| `rfboc_meal_schedule_day` | INT | NOT NULL                                  |

---

### 6. `history_food_recommendation`
Tabel ini mencatat makanan yang direkomendasikan dari riwayat harian pengguna.

| Column Name      | Data Type     | Constraints                                  |
| -----------------| -------------| ------------------------------------------- |
| `hfr_id`         | INT          | Primary Key, AUTO_INCREMENT                 |
| `hfr_name`       | VARCHAR(255) | NOT NULL                                    |
| `hfr_calories`   | DECIMAL(10,2)| NOT NULL                                    |
| `hfr_carbohydrate`| DECIMAL(10,2)| NOT NULL                                   |
| `hfr_fat`        | DECIMAL(10,2)| NOT NULL                                    |
| `hfr_protein`    | DECIMAL(10,2)| NOT NULL                                    |
| `hrfpd_id`       | INT          | Foreign Key -> `history_recommendation_food_per_day(hrfpd_id)` |
| `rfp_id`         | VARCHAR(255) | Foreign Key -> `recommended_food_preference(rfp_id)` |

---

## Relationships
1. `favorite_food_preference` -> `favorite_food_name`
   - `ffn_id` di `favorite_food_preference` merujuk ke `favorite_food_name.ffn_id`.

2. `recommended_food_preference` -> `recommended_food_based_on_calories`
   - `rfboc_id` di `recommended_food_preference` merujuk ke `recommended_food_based_on_calories.rfboc_id`.

3. `history_food_recommendation` -> `history_recommendation_food_per_day`
   - `hrfpd_id` di `history_food_recommendation` merujuk ke `history_recommendation_food_per_day.hrfpd_id`.

4. `history_food_recommendation` -> `recommended_food_preference`
   - `rfp_id` di `history_food_recommendation` merujuk ke `recommended_food_preference.rfp_id`.

## Penjelasan Kolom Data

### 1. **rfboc_history_of_gastritis_or_gerd**

Kolom ini merepresentasikan apakah seseorang memiliki riwayat gastritis atau GERD.

- **Yes (True):** Jika pengguna menjawab *"Yes"* pada pertanyaan *"Do you have a history of gastritis or GERD?"*.
- **No (False):** Jika pengguna menjawab *"No"* pada pertanyaan yang sama.

### 2. **rfboc_history_of_gastritis**

Kolom ini mirip dengan `rfboc_history_of_gastritis_or_gerd`, tetapi fokusnya hanya pada riwayat gastritis.

- **Yes (True):** Jika pengguna memiliki riwayat gastritis.
- **No (False):** Jika pengguna tidak memiliki riwayat gastritis.

### 3. **rfboc_gender**

Kolom ini merepresentasikan jenis kelamin pengguna.

- **Male (True):** Jika pengguna adalah laki-laki.
- **Female (False):** Jika pengguna adalah perempuan.

## ERD Diagram (Illustration)

```plaintext
recommended_food_based_on_calories
       |
       |---< rfboc_id >--- recommended_food_preference
       |                          |
       |                          |---< ffp_id >--- favorite_food_preference
       |                                               |
       |                                               |---< ffn_id >--- favorite_food_name
       |
       |---< history_recommendation_food_per_day
                        |
                        |---< hrfpd_id >--- history_food_recommendation
```

# How to Run Test User Input in NutriGoal Project

This guide explains how to run and test user input in the **NutriGoal** project using HTTP POST and GET methods. While browsers only support the GET method when directly entering a URL into the address bar, this guide also covers using tools like **Postman** or **curl** to test inputs via the POST method.

## Steps to Run the Project and Test Inputs

### 1. Open the Project in VS Code

- Navigate to the NutriGoal project folder.
- Open the project in **Visual Studio Code (VS Code)**.

### 2. Open the Terminal

- In VS Code, open the terminal by pressing **Ctrl + `* or navigating to` Terminal > New Terminal`.

### 3. Navigate to the Project Directory

- Use the following command to switch to the project directory:
    
    ```bash
    cd Web-Browser
    
    ```
    

### 4. Run the Project

- Start the application by running the following command in the terminal:
    
    ```bash
    python app-multiple.py
    
    ```
    
- This will start a local server. The terminal will display a URL like:
    
    ```bash
    Running on http://127.0.0.1:5000
    
    ```
    

### 5. Open the Project in a Browser

- Copy the URL from the terminal (e.g., `http://127.0.0.1:5000`) and paste it into your browser's address bar to open the application.

---

## Simulating User Inputs

### 6. Test Inputs Using the Browser (GET Method)

To test user inputs with the GET method directly via the browser, use the following URL structure:

```bash
http://127.0.0.1:5000/predict?age=30&height=180&weight=75&gender=2&activity_level=4&diet_category=keto&has_gastric_issue=false&food_preference=Fish&food_preference=apple

```

- Replace the query parameters (**`age`**, **`height`**, etc.) with the values you want to test:
    - **`age`**: User's age (e.g., **`25`**).
    - **`height`**: User's height in centimeters (e.g., **`175`**).
    - **`weight`**: User's weight in kilograms (e.g., **`70`**).
    - **`gender`**: Gender of the user (**`1`** for male, **`2`** for female).
    - **`activity_level`**: User's activity level (**`1`** to **`5`**).
    - **`diet_category`**: User's diet category (e.g., **`vegan`**, **`keto`**, etc.).
    - **`has_gastric_issue`**: **`true`** if the user has a gastric issue, otherwise **`false`**.
    - **`food_preference`**: User's food preferences (can include multiple values, e.g., **`Chicken`**, **`Rice`**).

### Example URL for Testing:

```bash
http://127.0.0.1:5000/predict?age=30&height=180&weight=75&gender=2&activity_level=4&diet_category=keto&has_gastric_issue=false&food_preference=Fish&food_preference=apple

```

---

### 7. Testing with HTTP POST (Optional)

To test inputs using the HTTP POST method:

1. Use tools like **Postman**, **curl**, or any REST client.
2. Make a POST request to the `/predictjson` endpoint with the following JSON format:

### Example JSON Body:

```json
{
  "age": 25,
  "height": 175,
  "weight": 70,
  "gender": 1,
  "activity_level": 3,
  "diet_category": "vegan",
  "has_gastric_issue": true,
  "food_preference": ["Chicken", "Rice"]
}

```

### Using curl:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"age": 25, "height": 175, "weight": 70, "gender": 1, "activity_level": 3, "diet_category": "vegan", "has_gastric_issue": true, "food_preference": ["Chicken", "Rice"]}' \
http://127.0.0.1:5000/predict

```

# API Documentation

## Overview

This API provides endpoints to manage food recommendation history based on user input. The two primary endpoints are:

- `/historytest`: Processes food preference recommendations.
- `/history`: Retrieves historical food recommendations based on user data.

## Base URL

The base URL for the API is:
```bash
http://0.0.0.0:5000

```

## Endpoints

### 1. `/historytest`

#### Method: `POST`

**Description**: This endpoint allows you to submit user data and receive food recommendations based on the provided preferences.

**Request URL**:
```bash
POST http://0.0.0.0:5000/historytest
```


**Headers**:
- `Content-Type: application/json`

**Request Body** (JSON):
```json
{
  "rfp_id": [1, 2, 3],
  "rfboc_id": 1,
  "name": [
    "rice cooker mexican rice",
    "party rice and noodles",
    "fruit and nut rice pilaf"
  ],
  "calories": [238.2, 238.0, 238.0],
  "carbohydrate(g)": [40.9, 33.6, 48.4],
  "protein(g)": [6.9, 5.6, 4.7],
  "fat(g)": [7.5, 8.9, 3.4],
  "height": 175,
  "weight": 70,
  "age": 25,
  "food_preference_recommendation": [1, 2, 3],
  "favorite_food_preference": [
    {
      "ffp_id": 1,
      "ffp_name": "Chicken"
    },
    {
      "ffp_id": 1,
      "ffp_name": "Rice"
    }
  ],
  "recommended_food_based_on_calories": {
    "rfboc_activity_level": 3,
    "rfboc_diet_type": "vegan",
    "rfboc_meal_schedule_(day)": 3,
    "history_of_gastritis_or_gerd": true
  },
  "user_id": 1,
  "gender": true
}

```

**Response**:

- `200 OK`: Returns food recommendations and user data.
- `400 Bad Request`: Returns error messages for invalid or missing fields.
- `500 Internal Server Error`: Returns unexpected error messages.

### Example using Postman:

1. Open Postman.
2. Set the request type to `POST`.
3. Enter the URL: `http://0.0.0.0:5000/historytest`.
4. In the "Headers" tab, add `Content-Type` with the value `application/json`.
5. In the "Body" tab, select `raw` and paste the JSON request body.
6. Click `Send` to submit the request.

### 2. `/history`

### Method: `POST`

**Description**: This endpoint allows you to submit user data and receive a history of food recommendations based on preferences.

**Request URL**:

```bash
POST http://0.0.0.0:5000/history

```

**Headers**:

- `Content-Type: application/json`

**Request Body** (JSON):

```json
{
  "rfp_id": [1, 2, 3],
  "rfboc_id": 1,
  "name": [
    "rice cooker mexican rice",
    "party rice and noodles",
    "fruit and nut rice pilaf"
  ],
  "calories": [238.2, 238.0, 238.0],
  "carbohydrate(g)": [40.9, 33.6, 48.4],
  "protein(g)": [6.9, 5.6, 4.7],
  "fat(g)": [7.5, 8.9, 3.4],
  "height": 175,
  "weight": 70,
  "age": 25,
  "food_preference_recommendation": [1, 2, 3],
  "favorite_food_preference": [
    {
      "ffp_id": 1,
      "ffp_name": "Chicken"
    },
    {
      "ffp_id": 1,
      "ffp_name": "Rice"
    }
  ],
  "recommended_food_based_on_calories": {
    "rfboc_activity_level": 3,
    "rfboc_diet_type": "vegan",
    "rfboc_meal_schedule_(day)": 3,
    "history_of_gastritis_or_gerd": true
  },
  "user_id": 1,
  "gender": true
}

```

**Response**:

- `200 OK`: Returns a history of food recommendations and user data.
- `400 Bad Request`: Returns error messages for invalid or missing fields.
- `500 Internal Server Error`: Returns unexpected error messages.

### Example using Postman:

1. Open Postman.
2. Set the request type to `POST`.
3. Enter the URL: `http://0.0.0.0:5000/history`.
4. In the "Headers" tab, add `Content-Type` with the value `application/json`.
5. In the "Body" tab, select `raw` and paste the JSON request body.
6. Click `Send` to submit the request.


---

### Key Notes:

- When using the browser for GET requests, list items for `food_preference` by appending multiple `food_preference` parameters.
- For POST requests, ensure that the JSON structure matches the input requirements of the backend code.