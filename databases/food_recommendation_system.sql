-- Create the database
CREATE DATABASE food_recommendation_system;

-- Use the database
USE food_recommendation_system;

-- Create the table 'recommended_food_based_on_calories'
CREATE TABLE recommended_food_based_on_calories (
    rfboc_id INT AUTO_INCREMENT PRIMARY KEY,
    rfboc_activity_level VARCHAR(255) NOT NULL,
    rfboc_age INT NOT NULL,
    rfboc_gender VARCHAR(50) NOT NULL,
    rfboc_height_cm FLOAT NOT NULL,
    rfboc_weight_kg FLOAT NOT NULL,
    rfboc_predicted_daily_calorie_needs FLOAT NOT NULL,
    rfboc_total_calories FLOAT NOT NULL,
    rfboc_total_carbohydrate FLOAT NOT NULL,
    rfboc_total_cholesterol FLOAT NOT NULL,
    rfboc_total_fat FLOAT NOT NULL,
    rfboc_total_fiber FLOAT NOT NULL,
    rfboc_total_protein FLOAT NOT NULL,
    rfboc_total_saturated_fat FLOAT NOT NULL,
    rfboc_total_sodium FLOAT NOT NULL,
    rfboc_total_sugar FLOAT NOT NULL,
    rfboc_created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    rfboc_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Create the table 'food_preference_analysis'
CREATE TABLE food_preference_analysis (
    fra_id INT AUTO_INCREMENT PRIMARY KEY,
    rfboc_id INT,
    fra_name VARCHAR(255) NOT NULL,
    fra_created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    fra_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (rfboc_id) REFERENCES recommended_food_based_on_calories(rfboc_id)
);

-- Create the table 'recommended_food'
CREATE TABLE recommended_food (
    rf_id INT AUTO_INCREMENT PRIMARY KEY,
    rfboc_id INT,
    fra_id INT,
    rf_name VARCHAR(255) NOT NULL,
    rf_calories FLOAT NOT NULL,
    rf_carbohydrate FLOAT NOT NULL,
    rf_cholesterol FLOAT NOT NULL,
    rf_fat FLOAT NOT NULL,
    rf_fiber FLOAT NOT NULL,
    rf_protein FLOAT NOT NULL,
    rf_saturated_fat FLOAT NOT NULL,
    rf_sodium FLOAT NOT NULL,
    rf_sugar FLOAT NOT NULL,
    rf_user_input VARCHAR(255) NOT NULL,
    rf_created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    rf_updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (rfboc_id) REFERENCES recommended_food_based_on_calories(rfboc_id),
    FOREIGN KEY (fra_id) REFERENCES food_preference_analysis(fra_id)
);
