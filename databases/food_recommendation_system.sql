-- Create the database
CREATE DATABASE food_recommendation_system;

-- Use the database
USE food_recommendation_system;

-- Tabel favorite_food_name
CREATE TABLE favorite_food_name (
    ffn_id INT PRIMARY KEY AUTO_INCREMENT,
    ffn_name VARCHAR(255) NOT NULL,
    ffn_created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ffn_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Tabel favorite_food_preference
CREATE TABLE favorite_food_preference (
    ffp_id INT PRIMARY KEY AUTO_INCREMENT,
    ffn_id INT,
    ffp_name VARCHAR(255) NOT NULL,
    ffp_created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    ffp_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (ffn_id) REFERENCES favorite_food_name(ffn_id)
);

-- Tabel recommended_food_based_on_calories
CREATE TABLE recommended_food_based_on_calories (
    rfboc_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    rfboc_diet_type VARCHAR(255) NOT NULL,
    rfboc_history_of_gastritis_or_gerd BOOLEAN NOT NULL,
    rfboc_age INT NOT NULL,
    rfboc_height_cm FLOAT NOT NULL,
    rfboc_weight_kg FLOAT NOT NULL,
    rfboc_gender BOOLEAN NOT NULL,
    rfboc_activity_level INT NOT NULL,
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
    rfboc_id INT,
    ffp_id INT,
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
    hrfpd_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    age INT,
    body_weight DECIMAL(10, 2),
    height DECIMAL(10, 2),
    diet_time DATETIME,
    created_at DATETIME,
    rfboc_activity_level INT,
    rfboc_meal_schedule_day INT,
    rfboc_diet_type VARCHAR(50),
    rfboc_gender BOOLEAN,
    rfboc_history_of_gastritis BOOLEAN
);

-- Tabel history_food_recommendation
CREATE TABLE history_food_recommendation (
    hfr_id INT AUTO_INCREMENT PRIMARY KEY,
    hfr_name VARCHAR(255),
    hfr_calories DECIMAL(10, 2),
    hfr_carbohydrate DECIMAL(10, 2),
    hfr_fat DECIMAL(10, 2),
    hfr_protein DECIMAL(10, 2),
    hrfpd_id INT,
    rfp_id VARCHAR(255),
    FOREIGN KEY (hrfpd_id) REFERENCES history_recommendation_food_per_day(hrfpd_id),
    FOREIGN KEY (rfp_id) REFERENCES recommended_food_preference(rfp_id)
);
