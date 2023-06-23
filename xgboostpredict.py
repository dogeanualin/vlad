from flask import Flask, render_template, request
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from sklearn.metrics import mean_squared_error
import io
import base64

# Load the dataset
df2 = pd.read_csv('data/train_data_grocery.csv')

# Convert the 'product_sales' column to a time series

sales_ts1 = pd.Series(df2['product_sales'].values, index=df2.index)
sales_ts2 = pd.Series(df2['sales_per_week'].values, index=df2.index)
sales_ts3 = pd.Series(df2['sales_per_day'].values, index=df2.index)

# Train-test split
train_size = int(len(df2) * 0.7)
train1, test1 = sales_ts1[:train_size], sales_ts1[train_size:]
train2, test2 = sales_ts2[:train_size], sales_ts2[train_size:]
train3, test3 = sales_ts3[:train_size], sales_ts3[train_size:]


# Route for prediction and visualization
def predict(sales_type):

    if sales_type == "Total Sales":
        train_data, test_data = train1, test1
    elif sales_type == "Weekly Sales":
        train_data, test_data = train2, test2
    elif sales_type == "Hourly Sales":
        train_data, test_data = train3, test3

    # Create and train the XGBoost regressor
    model = xgb.XGBRegressor(objective='reg:squarederror', random_state=0)
    model.fit(train_data, train_data.values)

    # Make predictions on the testing data
    predictions = model.predict(test_data)

    # Calculate the mean squared error
    mse = mean_squared_error(test_data, predictions)

    # Clear the previous figure
    plt.clf()

    # Visualize the actual sales and predicted sales
    fig = plt.figure(figsize=(10, 6))
    plt.plot(predictions, 'r', label="Predictions")
    plt.plot(test_data.index, test_data.values, 'b', label="Actual")
    plt.xlabel('Time')
    plt.ylabel('Sales')
    plt.title(f'{sales_type} - XGBoost Predicted vs Actual Sales')
    plt.legend()

    # Convert the figure to a base64 encoded string
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    image_base64 = base64.b64encode(output.getvalue()).decode('utf-8')

    return render_template('xgboost/result.html', image=image_base64, mse=mse)


