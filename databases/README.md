# Database Schema: Food Recommendation System

Dokumen ini menjelaskan struktur database untuk **Food Recommendation System**, termasuk tabel-tabel dan hubungan antar tabelnya.

## Tables

### 1. `favorite_food_name`

Tabel ini menyimpan informasi nama makanan favorit pengguna.

| Column Name | Data Type | Constraints |
| --- | --- | --- |
| `ffn_id` | VARCHAR(36) | Primary Key |
| `ffn_name` | VARCHAR(255) | NOT NULL |
| `ffn_created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| `ffn_updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

---

### 2. `favorite_food_preference`

Tabel ini menyimpan preferensi makanan favorit pengguna.

| Column Name | Data Type | Constraints |
| --- | --- | --- |
| `ffp_id` | VARCHAR(36) | Primary Key |
| `ffn_id` | VARCHAR(36) | Foreign Key -> `favorite_food_name(ffn_id)` |
| `ffp_name` | VARCHAR(255) | NOT NULL |
| `ffp_created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| `ffp_updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

---

### 3. `recommended_food_preference`

Tabel ini menyimpan makanan yang direkomendasikan berdasarkan preferensi pengguna.

| Column Name | Data Type | Constraints |
| --- | --- | --- |
| `rfp_id` | VARCHAR(36) | Primary Key |
| `rfboc_id` | VARCHAR(36) | Foreign Key -> `recommended_food_based_on_calories(rfboc_id)` |
| `rfp_name` | VARCHAR(255) | NOT NULL |
| `rfp_created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| `rfp_updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

---

### 4. `recommended_food_based_on_calories`

Tabel ini menyimpan informasi rekomendasi makanan berdasarkan kebutuhan kalori pengguna.

| Column Name | Data Type | Constraints |
| --- | --- | --- |
| `rfboc_id` | VARCHAR(36) | Primary Key |
| `user_id` | VARCHAR(36) | Foreign Key -> `user(user_id)` |
| `rfboc_diet_type` | VARCHAR(255) | NOT NULL |
| `rfboc_history_of_gastritis_or_gerd` | VARCHAR(10) | NOT NULL |
| `rfboc_age` | INT | NOT NULL |
| `rfboc_height_cm` | FLOAT | NOT NULL |
| `rfboc_weight_kg` | FLOAT | NOT NULL |
| `rfboc_gender` | VARCHAR(10) | NOT NULL |
| `rfboc_activity_level` | VARCHAR(255) | NOT NULL |
| `rfboc_meal_schedule_day` | VARCHAR(50) | NOT NULL |
| `rfboc_daily_calorie_needs` | FLOAT | NOT NULL |
| `rfboc_bmr` | FLOAT | NOT NULL |
| `rfboc_bmi` | FLOAT | NOT NULL |
| `rfboc_ideal_weight` | FLOAT | NOT NULL |
| `rfboc_ideal_bmi` | FLOAT | NOT NULL |
| `rfboc_weight_difference` | FLOAT | NOT NULL |
| `rfboc_total_calories_by_recommendation` | FLOAT | NOT NULL |
| `rfboc_total_protein_g` | FLOAT | NOT NULL |
| `rfboc_total_fat_g` | FLOAT | NOT NULL |
| `rfboc_total_carbohydrate_g` | FLOAT | NOT NULL |
| `rfboc_total_fiber_g` | FLOAT | NOT NULL |
| `rfboc_total_cholesterol_mg` | FLOAT | NOT NULL |
| `rfboc_total_sodium_mg` | FLOAT | NOT NULL |
| `rfboc_total_sugar_g` | FLOAT | NOT NULL |
| `rfboc_total_saturated_fat_g` | FLOAT | NOT NULL |
| `rfboc_created_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP |
| `rfboc_updated_at` | DATETIME | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

---

## Relationships

1. **`favorite_food_preference` -> `favorite_food_name`**
    - Kolom `ffn_id` di `favorite_food_preference` merujuk ke kolom `ffn_id` di `favorite_food_name`.
2. **`recommended_food_preference` -> `recommended_food_based_on_calories`**
    - Kolom `rfboc_id` di `recommended_food_preference` merujuk ke kolom `rfboc_id` di `recommended_food_based_on_calories`.

## ERD Diagram (Illustration)
The following is a simplified Entity-Relationship Diagram (ERD) for the database schema:

```plaintext
recommended_food_based_on_calories
       |
       |---< rfboc_id >--- recommended_food_preference
       |                          |
       |                          |---< ffp_id >--- favorite_food_preference
       |                                               |
       |                                               |---< ffn_id >--- favorite_food_name
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

---

### Key Notes:

- When using the browser for GET requests, list items for `food_preference` by appending multiple `food_preference` parameters.
- For POST requests, ensure that the JSON structure matches the input requirements of the backend code.