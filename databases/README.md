# Database Schema: Food Recommendation System

This document provides an overview of the database schema for the **Food Recommendation System**, including the table structures and their relationships.

## Tables

### 1. `food_preference_analysis`
This table stores food preference data linked to a specific calorie recommendation.

| Column Name     | Data Type       | Constraints                   |
|------------------|----------------|--------------------------------|
| `fra_id`        | INT            | Primary Key, Auto Increment    |
| `rfboc_id`      | INT            | Foreign Key -> `recommended_food_based_on_calories(rfboc_id)` |
| `fra_name`      | VARCHAR(255)   | NOT NULL                      |
| `fra_created_at`| DATETIME       | DEFAULT CURRENT_TIMESTAMP      |
| `fra_updated_at`| DATETIME       | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

### 2. `recommended_food`
This table stores detailed information about recommended foods, including nutritional values and user inputs.

| Column Name         | Data Type       | Constraints                   |
|----------------------|----------------|--------------------------------|
| `rf_id`             | INT            | Primary Key, Auto Increment    |
| `rfboc_id`          | INT            | Foreign Key -> `recommended_food_based_on_calories(rfboc_id)` |
| `fra_id`            | INT            | Foreign Key -> `food_preference_analysis(fra_id)` |
| `rf_name`           | VARCHAR(255)   | NOT NULL                      |
| `rf_calories`       | FLOAT          | NOT NULL                      |
| `rf_carbohydrate`   | FLOAT          | NOT NULL                      |
| `rf_cholesterol`    | FLOAT          | NOT NULL                      |
| `rf_fat`            | FLOAT          | NOT NULL                      |
| `rf_fiber`          | FLOAT          | NOT NULL                      |
| `rf_protein`        | FLOAT          | NOT NULL                      |
| `rf_saturated_fat`  | FLOAT          | NOT NULL                      |
| `rf_sodium`         | FLOAT          | NOT NULL                      |
| `rf_sugar`          | FLOAT          | NOT NULL                      |
| `rf_user_input`     | VARCHAR(255)   | NOT NULL                      |
| `rf_created_at`     | DATETIME       | DEFAULT CURRENT_TIMESTAMP      |
| `rf_updated_at`     | DATETIME       | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

### 3. `recommended_food_based_on_calories`
This table contains information about recommended calorie intake based on user-specific details such as age, gender, and activity level.

| Column Name                           | Data Type       | Constraints                   |
|---------------------------------------|----------------|--------------------------------|
| `rfboc_id`                            | INT            | Primary Key, Auto Increment    |
| `rfboc_activity_level`                | VARCHAR(255)   | NOT NULL                      |
| `rfboc_age`                           | INT            | NOT NULL                      |
| `rfboc_gender`                        | VARCHAR(50)    | NOT NULL                      |
| `rfboc_height_cm`                     | FLOAT          | NOT NULL                      |
| `rfboc_weight_kg`                     | FLOAT          | NOT NULL                      |
| `rfboc_predicted_daily_calorie_needs` | FLOAT          | NOT NULL                      |
| `rfboc_total_calories`                | FLOAT          | NOT NULL                      |
| `rfboc_total_carbohydrate`            | FLOAT          | NOT NULL                      |
| `rfboc_total_cholesterol`             | FLOAT          | NOT NULL                      |
| `rfboc_total_fat`                     | FLOAT          | NOT NULL                      |
| `rfboc_total_fiber`                   | FLOAT          | NOT NULL                      |
| `rfboc_total_protein`                 | FLOAT          | NOT NULL                      |
| `rfboc_total_saturated_fat`           | FLOAT          | NOT NULL                      |
| `rfboc_total_sodium`                  | FLOAT          | NOT NULL                      |
| `rfboc_total_sugar`                   | FLOAT          | NOT NULL                      |
| `rfboc_created_at`                    | DATETIME       | DEFAULT CURRENT_TIMESTAMP      |
| `rfboc_updated_at`                    | DATETIME       | DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP |

## Relationships

1. **`food_preference_analysis` -> `recommended_food_based_on_calories`**
   - The column `rfboc_id` in `food_preference_analysis` references the column `rfboc_id` in `recommended_food_based_on_calories`.

2. **`recommended_food` -> `food_preference_analysis`**
   - The column `fra_id` in `recommended_food` references the column `fra_id` in `food_preference_analysis`.

3. **`recommended_food` -> `recommended_food_based_on_calories`**
   - The column `rfboc_id` in `recommended_food` references the column `rfboc_id` in `recommended_food_based_on_calories`.

## ERD Diagram (Illustration)
The following is a simplified Entity-Relationship Diagram (ERD) for the database schema:

```plaintext
recommended_food_based_on_calories
       |
       |---< rfboc_id >--- food_preference_analysis
       |                      |
       |                      |---< fra_id >--- recommended_food
```

# How to Run Test User Input in NutriGoal Project

This guide explains how to run and test user input in the **NutriGoal** project using HTTP POST and GET methods. While browsers only support the GET method when directly entering a URL into the address bar, you can test inputs as outlined below.

## Steps to Run the Project and Test Inputs

### 1. Open the Project in VS Code

- Navigate to the NutriGoal project folder.
- Open the project in **Visual Studio Code (VS Code)**.

### 2. Open the Terminal

- In VS Code, open the terminal by pressing **Ctrl+`* or navigating to` Terminal > New Terminal`.

### 3. Navigate to the Web-Browser Directory

- Use the following command to switch to the `Web-Browser` directory:
    
    ```bash
    cd Web-Browser
    
    ```
    Before :
    ![image.png](attachment:image.png)
    After:
    ![image-2.png](attachment:image-2.png)

### 4. Run the Project

- Start the application by running the following command in the terminal:
    
    ```bash
    python app-multiple.py
    
    ```
    ![image-3.png](attachment:image-3.png)
    
- This will start a local server. The terminal will display a URL like:
    
    ```bash
    Running on http://127.0.0.1:5000
    
    ```
    ![image-4.png](attachment:image-4.png)
    

### 5. Open the Project in a Browser

- Copy the URL from the terminal (e.g., `http://127.0.0.1:5000`) and paste it into your browser's address bar to open the application.

### 6. Test Inputs Using the Browser (GET Method)

- To test user inputs with the GET method (directly via the browser), use the following URL structure:
    
    ```bash
    http://127.0.0.1:5000/predictjson?age=25&height=175&weight=70&gender=1&activity_level=3&food_preference=Chicken&food_preference=Rice
    
    ```
    Before :
    ![image-5.png](attachment:image-5.png)
    After:
    ![image-6.png](attachment:image-6.png)
    ![image-7.png](attachment:image-7.png)
    
- Replace the query parameters (`age`, `height`, etc.) with the values you want to test. For example:
    - `age`: User's age (e.g., `25`).
    - `height`: User's height in centimeters (e.g., `175`).
    - `weight`: User's weight in kilograms (e.g., `70`).
    - `gender`: Gender of the user (`1` for male, `2` for female).
    - `activity_level`: Activity level (e.g., `3` for moderate activity).
    - `food_preference`: User's food preference (can include multiple values, e.g., `Chicken`, `Rice`).

### Example URL for Testing:

```bash
http://127.0.0.1:5000/predictjson?age=25&height=175&weight=70&gender=1&activity_level=3&food_preference=Chicken&food_preference=Rice

```

### 7. Testing with HTTP POST (Optional)

If you want to test inputs using the HTTP POST method:

- Use tools like **Postman** or **curl**.
- Make a POST request to the `/predictjson` endpoint with JSON data.

### Example JSON Body:

```json
{
  "age": 25,
  "height": 175,
  "weight": 70,
  "gender": 1,
  "activity_level": 3,
  "food_preference": ["Chicken", "Rice"]
}

```

### Using curl:

```bash
curl -X POST -H "Content-Type: application/json" -d '{"age": 25, "height": 175, "weight": 70, "gender": 1, "activity_level": 3, "food_preference": ["Chicken", "Rice"]}' http://127.0.0.1:5000/predictjson

```