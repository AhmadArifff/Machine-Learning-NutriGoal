-- Create the database
CREATE DATABASE food_recommendation_system;

-- Use the database
USE food_recommendation_system;

-- Tabel favorite_food_name
CREATE TABLE favorite_food_name (
    ffn_id VARCHAR(255) PRIMARY KEY,
    ffn_name VARCHAR(255) NOT NULL,
    ffn_created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ffn_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabel favorite_food_preference
CREATE TABLE favorite_food_preference (
    ffp_id VARCHAR(255) PRIMARY KEY,
    ffn_id VARCHAR(255),
    ffp_name VARCHAR(255) NOT NULL,
    ffp_created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ffp_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ffn_id) REFERENCES favorite_food_name(ffn_id)
);

-- Tabel recommended_food_based_on_calories
CREATE TABLE recommended_food_based_on_calories (
    rfboc_id VARCHAR(255) PRIMARY KEY,
    user_id VARCHAR(255),
    rfboc_diet_type VARCHAR(255) NOT NULL,
    rfboc_history_of_gastritis_or_gerd VARCHAR(10) NOT NULL,
    rfboc_age INT NOT NULL,
    rfboc_height_cm FLOAT NOT NULL,
    rfboc_weight_kg FLOAT NOT NULL,
    rfboc_gender VARCHAR(10) NOT NULL,
    rfboc_activity_level VARCHAR(255) NOT NULL,
    rfboc_meal_schedule_day INT NOT NULL,
    rfboc_daily_calorie_needs FLOAT NOT NULL,
    rfboc_bmr FLOAT NOT NULL,
    rfboc_bmi FLOAT NOT NULL,
    rfboc_ideal_weight FLOAT NOT NULL,
    rfboc_ideal_bmi FLOAT NOT NULL,
    rfboc_weight_difference FLOAT NOT NULL,
    rfboc_total_calories_by_recommendation FLOAT NOT NULL,
    rfboc_total_protein_g FLOAT NOT NULL,
    rfboc_total_fat_g FLOAT NOT NULL,
    rfboc_total_carbohydrate_g FLOAT NOT NULL,
    rfboc_total_fiber_g FLOAT NOT NULL,
    rfboc_total_cholesterol_mg FLOAT NOT NULL,
    rfboc_total_sodium_mg FLOAT NOT NULL,
    rfboc_total_sugar_g FLOAT NOT NULL,
    rfboc_total_saturated_fat_g FLOAT NOT NULL,
    rfboc_created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    rfboc_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabel recommended_food_preference
CREATE TABLE recommended_food_preference (
    rfp_id VARCHAR(255) PRIMARY KEY,
    rfboc_id VARCHAR(255),
    ffp_id VARCHAR(255),
    name VARCHAR(255) NOT NULL,
    calories FLOAT NOT NULL,
    protein_g FLOAT NOT NULL,
    fat_g FLOAT NOT NULL,
    carbohydrate_g FLOAT NOT NULL,
    fiber_g FLOAT NOT NULL,
    cholesterol_mg FLOAT NOT NULL,
    sodium_mg FLOAT NOT NULL,
    sugar_g FLOAT NOT NULL,
    saturated_fat_g FLOAT NOT NULL,
    rfp_created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    rfp_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (rfboc_id) REFERENCES recommended_food_based_on_calories(rfboc_id),
    FOREIGN KEY (ffp_id) REFERENCES favorite_food_preference(ffp_id)
);

-- Tabel history_recommendation_food_per_day
CREATE TABLE history_recommendation_food_per_day (
    hrf_id INT PRIMARY KEY,
    user_id INT NOT NULL,
    age INT NOT NULL,
    body_weight FLOAT NOT NULL,
    height FLOAT NOT NULL,
    diet_time DATETIME NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabel history_food_recommendation
CREATE TABLE history_food_recommendation (
    hfr_id INT PRIMARY KEY,
    hfr_name VARCHAR(255) NOT NULL,
    hfr_calories FLOAT NOT NULL,
    hfr_carbohydrate_g FLOAT NOT NULL,
    hfr_fat_g FLOAT NOT NULL,
    hfr_protein_g FLOAT NOT NULL,
    hrf_id INT NOT NULL,
    rfp_id VARCHAR(255),
    FOREIGN KEY (hrf_id) REFERENCES history_recommendation_food_per_day(hrf_id),
    FOREIGN KEY (rfp_id) REFERENCES recommended_food_preference(rfp_id)
);
