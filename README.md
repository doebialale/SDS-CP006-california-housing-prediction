# Welcome to the SuperDataScience Community Project!
Welcome to the California Housing Prediction repository! 🎉

This project is a collaborative initiative brought to you by SuperDataScience, a thriving community dedicated to advancing the fields of data science, machine learning, and AI. We are excited to have you join us in this journey of learning, experimentation, and growth.

## About This Project
In this repository, you’ll find the work carried out by our community members in completing an end-to-end machine learning project. Please note that the resources available here is not to be used or copied without referencing the appropriate authors.

## Project Objectives
The project aims to build a predictive model for housing prices in California based on various property characteristics. The goal is to provide insights into which features most impact house prices and deliver a model that can predict the price of a house based on these attributes. This project will help real estate agencies and buyers make informed decisions regarding property investments.

What specific questions will this project answer or what insights will it provide? The project will answer questions such as:
1. What are the key factors influencing house prices in California?
2. How can we predict house prices with high accuracy using available property data?
3. How will the results of this project generate value?

The model will help real estate agents and buyers by providing accurate price predictions and identifying critical price-driving features. This can improve market decision-making.

**Link to Dataset:** https://www.kaggle.com/datasets/yellowj4acket/real-estate-california

## Project Phases
**Data Cleaning & Analysis**
- Handling null values (e.g. imputation, deletion). 
- Identify columns to drop e.g 
- Exploratory Data Analysis (EDA) to understand distributions, outliers, and relationships of features like bedrooms, bathrooms, livingArea with price.
- Correlation analysis to determine multicollinearity or feature redundancy.

**Data Preprocessing & Feature Engineering**
- Creating new features such as price per square foot, age of property.
- One-hot encoding for categorical variables like homeType.
- Scaling features like livingArea and price.
- Handling outliers (e.g., unrealistic values for price, livingArea).

**Model Selection & Fine Tuning**
- Training multiple models like Linear Regression, Random Forest, and XGBoost.
- Evaluating model performance based on RMSE, R².
- Hyperparameter tuning using grid search or random search.

**Deployment**
- Building a streamlit app that takes inputs like bedrooms, bathrooms, livingArea, and predicts the housing price.
- Deploying the application to a cloud platform (e.g. AWS/streamlit)
