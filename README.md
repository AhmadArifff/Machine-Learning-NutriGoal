NutriGoal: A Machine Learning-Powered Health & Nutrition App
📋 Project Overview
NutriGoal is a health and wellness application designed to address the growing obesity rates in Indonesia, where 6.53% of men and 29.7% of women are currently classified as obese as of 2024. By leveraging the power of machine learning, NutriGoal aims to provide accessible nutritional guidance to users, especially those in communities with limited access to dietary support.

The app uses Body Mass Index (BMI) to assess weight status and offers personalized diet plans to encourage healthier lifestyles and reduce obesity-related health risks such as heart disease and diabetes.

🚀 Project Goals
NutriGoal empowers users to achieve their health goals by:

Providing customized dietary plans (keto, vegan, intermittent fasting) based on user profiles (age, gender, weight, height, pre-existing conditions).
Calculating daily caloric needs and suggesting optimal meal times.
Sending notifications for meal adherence and tracking progress through daily check-ins.
Utilizing machine learning models to offer dietary recommendations and progress tracking.
🔍 Machine Learning Models
The project uses three key machine learning models to enhance user experience and dietary outcomes:

1. Modeling Nutritional Intake
Objective: Cluster foods based on their nutritional values (e.g., calorie counts of 1000, 2000, etc.) to guide users in selecting meals that align with their daily intake goals.
Dataset: Indonesian Food and Drink Nutrition Dataset
Approach: Use clustering algorithms to categorize meals by nutritional content.
2. Dietary Recommendation System
Objective: Provide personalized meal recommendations based on user surveys of favorite foods.
Approach: Train a model using user preference data to suggest meals that fit the user's dietary plan and preferences.
3. Progress Tracking and Weight Management
Objective: Track user progress by analyzing weight loss over a period (e.g., 1 month).
Approach: Analyze historical dietary data to determine the caloric intake needed for effective weight reduction. This model helps understand how users respond to different caloric deficits.
📊 Dataset
The project uses the Indonesian Food and Drink Nutrition Dataset available on Kaggle, which includes detailed nutritional information for various foods and drinks commonly consumed in Indonesia.

Dataset link: Indonesian Food and Drink Nutrition Dataset
💡 Key Features
Personalized Diet Plans: Tailored to user profiles for effective weight management.
Caloric Intake Tracking: Calculate and monitor daily caloric needs.
Progress Reports: Track weight loss achievements over time.
Notifications: Timely reminders to support adherence to dietary plans.
🛠️ Technologies Used
Python: Core language for data processing and model training.
Machine Learning Libraries:
pandas, numpy, scikit-learn for data manipulation and modeling.
matplotlib, seaborn for data visualization.
Flask: Backend framework for building the web application.
MySQL: Database management.
🗂️ Project Structure
graphql
Salin kode
NutriGoal/
├── data/                   # Dataset and preprocessing scripts
├── models/                 # Machine learning models
├── api/                    # Backend API using Flask
├── static/                 # Frontend assets
├── templates/              # HTML templates
└── README.md               # Project documentation
