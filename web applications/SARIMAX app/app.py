from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn.metrics import mean_squared_error
from statsmodels.tsa.statespace.sarimax import SARIMAX
import io
import base64

app = Flask(__name__)
df2 = pd.read_csv('train_data_grocery.csv')
# Convert the 'product_sales' column to a time series for each dataframe
sales_ts1 = pd.Series(df2['product_sales'].values, index=df2.index)
sales_ts2 = pd.Series(df2['sales_per_week'].values, index=df2.index)
sales_ts3 = pd.Series(df2['sales_per_day'].values, index=df2.index)

# Split the data into train and test sets for each sales type
train_size1 = int(len(sales_ts1) * 0.8)  # 80% train, 20% test
train_data1, test_data1 = sales_ts1[:train_size1], sales_ts1[train_size1:]

train_size2 = int(len(sales_ts2) * 0.8)
train_data2, test_data2 = sales_ts2[:train_size2], sales_ts2[train_size2:]

train_size3 = int(len(sales_ts3) * 0.8)
train_data3, test_data3 = sales_ts3[:train_size3], sales_ts3[train_size3:]

# Define the route for the index page
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        sales_type = request.form['sales_type']
        return predict_and_visualize(sales_type)
    return render_template('index.html')

# Function to predict and visualize the sales data
def predict_and_visualize(sales_type):
    # Define the SARIMA model and data for the selected sales type
    if sales_type == 'Total':
        train_data, test_data = train_data1, test_data1
    elif sales_type == 'Weekly':
        train_data, test_data = train_data2, test_data2
    elif sales_type == 'Hourly':
        train_data, test_data = train_data3, test_data3

    # Define the SARIMA model for the selected sales type
    order = (1, 1, 1)  # (p, d, q) - ARIMA order
    seasonal_order = (0, 1, 1, 7)  # (P, D, Q, S) - seasonal order
    model = SARIMAX(train_data, order=order, seasonal_order=seasonal_order)

    # Fit the model to the training data
    model_fit = model.fit()

    # Make predictions on the test data
    predictions = model_fit.forecast(steps=len(test_data))

    # Evaluate the model's accuracy
    mse = mean_squared_error(test_data, predictions)

    # Visualize the actual sales and predicted sales
    fig = plt.figure(figsize=(10, 6))
    plt.plot(test_data.index, test_data, label='Actual Sales')
    plt.plot(test_data.index, predictions, label='Forecasted Sales')
    plt.xlabel('Time')
    plt.ylabel('Product Sales')
    plt.title(f'Actual vs Forecasted Sales ({sales_type})')
    plt.legend()

    # Convert the figure to a base64-encoded string
    output = io.BytesIO()
    plt.savefig(output, format='png')
    plt.close(fig)
    output.seek(0)
    image_base64 = base64.b64encode(output.getvalue()).decode('utf-8')

    return render_template('results.html', image=image_base64, mse=mse)

# Run the Flask app
if __name__ == '__main__':
    app.run()
