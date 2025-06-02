# Noise Prediction Model

As part of the project we had to develop a machine learning model to predict noise levels in various locations based on data collected from sensors. The model leverages Facebook's Prophet algorithm, which is robust to missing data and outliers, and can handle seasonality and trend components effectively.

## Project Overview

### Objectives
- Predict noise levels based on historical sensor data.
- Handle missing values, outliers, and seasonality in the data.
- Provide accurate forecasts to help manage and mitigate noise pollution.

### Model Choice

The Prophet model was chosen for several reasons:
- **Handling Missing Data and Outliers**: Prophet is robust to missing data and outliers, which is essential given the potential for sensor malfunctions and external interferences in noise data.
- **Seasonality and Trend Components**: Noise levels often exhibit daily, weekly, and seasonal patterns. Prophet is designed to automatically detect and model these patterns.
- **Ease of Use and Interpretability**: Prophet provides clear insights into trend and seasonality components, making it user-friendly and easy to interpret.
- **Automatic Change Point Detection**: Prophet can detect and handle abrupt changes in time series trends, making it suitable for dynamic environments.

## Data Preparation

1. **Fetch Data**: Retrieve noise data from sensors using the InfluxDB client. The data includes timestamps, noise levels, and location metadata.
2. **Cleaning and Formatting**: Convert timestamps to a uniform format, remove timezone information, and handle missing values and outliers to ensure high data quality for training.

## Model Training

1. **Initial Training with Kaggle Data**: The model was initially trained on a publicly available noise dataset from Kaggle to leverage transfer learning. This provided a baseline and helped the model understand general noise patterns before fine-tuning with specific sensor data.
2. **Fit the Model**: Train the Prophet model on historical noise data formatted with `ds` (dates) and `y` (values) columns.
3. **Seasonality and Trend Detection**: Automatically detect and incorporate daily and weekly seasonality patterns.
4. **Hyperparameter Tuning**: Implement cross-validation to test different hyperparameters and optimize the model's performance.
5. **Model Evaluation**: Use metrics such as Mean Absolute Error (MAE) and Root Mean Squared Error (RMSE) to assess accuracy and analyze residuals for patterns or biases.

## Adaptability and Continuous Learning

1. **Rolling Forecast Origin**: Regularly retrain the model using the latest data to adapt to new patterns and changes in the environment.
2. **Incremental Learning**: Update the model with new data without retraining from scratch, allowing it to stay updated with the latest trends.
3. **Data Augmentation**: Simulate additional data points based on existing patterns to enrich the training dataset and help the model generalize better.

## Repository Structure

- `noise_predictions.py`: Main script for fetching data, training the model, and making predictions.
- `requirements.txt`: List of dependencies required for the project.
- `README.md`: Project documentation (this file).


### Model Version 2

We made a different version of the model (NoiseModel.py) which saves the predicted results in a json format which could be used as backup in case there are issues incontered with the json endpoint. With this option you then have to upload the json file on azure storage blob in order to access it through the json endpoint on Grafana


## How to Run

1. **Install Dependencies**:
   ```sh
   pip install -r requirements.txt

   python noise_predictions.py



