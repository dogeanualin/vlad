from flask import Flask, render_template
import base64
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import numpy as np

app = Flask(__name__)

# Load the data
df2 = pd.read_csv('data/train_data_grocery.csv')

# Convert the 'product_sales' column to a time series for each dataframe
sales_ts1 = pd.Series(df2['product_sales'].values, index=df2.index)
sales_ts2 = pd.Series(df2['sales_per_week'].values, index=df2.index)
sales_ts3 = pd.Series(df2['sales_per_day'].values, index=df2.index)

# Normalize the data for each sales type
scaler1 = MinMaxScaler(feature_range=(0, 1))
scaler2 = MinMaxScaler(feature_range=(0, 1))
scaler3 = MinMaxScaler(feature_range=(0, 1))
scaled_data1 = scaler1.fit_transform(sales_ts1.values.reshape(-1, 1))
scaled_data2 = scaler2.fit_transform(sales_ts2.values.reshape(-1, 1))
scaled_data3 = scaler3.fit_transform(sales_ts3.values.reshape(-1, 1))

# Split the data into train and test sets for each sales type
train_size = int(len(scaled_data1) * 0.8)  # 80% train, 20% test
train_data1, test_data1 = scaled_data1[:train_size], scaled_data1[train_size:]
train_data2, test_data2 = scaled_data2[:train_size], scaled_data2[train_size:]
train_data3, test_data3 = scaled_data3[:train_size], scaled_data3[train_size:]

# Define the number of time steps for input
n_steps = 3  # You can adjust this based on the desired sequence length

# Create input sequences for each sales type
X_train1, y_train1 = [], []
X_train2, y_train2 = [], []
X_train3, y_train3 = [], []
for i in range(n_steps, len(train_data1)):
    X_train1.append(train_data1[i - n_steps:i, 0])
    y_train1.append(train_data1[i, 0])
    X_train2.append(train_data2[i - n_steps:i, 0])
    y_train2.append(train_data2[i, 0])
    X_train3.append(train_data3[i - n_steps:i, 0])
    y_train3.append(train_data3[i, 0])
X_train1, y_train1 = np.array(X_train1), np.array(y_train1)
X_train2, y_train2 = np.array(X_train2), np.array(y_train2)
X_train3, y_train3 = np.array(X_train3), np.array(y_train3)

# Reshape the input data to fit the LSTM model
X_train1 = np.reshape(X_train1, (X_train1.shape[0], X_train1.shape[1], 1))
X_train2 = np.reshape(X_train2, (X_train2.shape[0], X_train2.shape[1], 1))
X_train3 = np.reshape(X_train3, (X_train3.shape[0], X_train3.shape[1], 1))

# Build the LSTM model for each sales type
model1 = Sequential()
model1.add(LSTM(units=20, return_sequences=True, input_shape=(n_steps, 1)))
model1.add(LSTM(units=15, return_sequences=True))
model1.add(LSTM(units=30))
model1.add(Dense(units=40, activation='relu'))
model1.add(Dense(units=1))
model1.compile(optimizer='adam', loss='mean_squared_error')
model1.fit(X_train1, y_train1, epochs=50, batch_size=32)

model2 = Sequential()
model2.add(LSTM(units=20, return_sequences=True, input_shape=(n_steps, 1)))
model2.add(LSTM(units=15, return_sequences=True))
model2.add(LSTM(units=30))
model2.add(Dense(units=40, activation='relu'))
model2.add(Dense(units=1))
model2.compile(optimizer='adam', loss='mean_squared_error')
model2.fit(X_train2, y_train2, epochs=50, batch_size=32)

model3 = Sequential()
model3.add(LSTM(units=20, return_sequences=True, input_shape=(n_steps, 1)))
model3.add(LSTM(units=15, return_sequences=True))
model3.add(LSTM(units=30))
model3.add(Dense(units=40, activation='relu'))
model3.add(Dense(units=1))
model3.compile(optimizer='adam', loss='mean_squared_error')
model3.fit(X_train3, y_train3, epochs=50, batch_size=32)


def forecast_sales(sales_ts, scaler, model):
    # Prepare test data for the sales type
    X_test, y_test = [], []
    for i in range(n_steps, len(test_data1)):
        X_test.append(sales_ts[i - n_steps:i, 0])
        y_test.append(sales_ts[i, 0])
    X_test, y_test = np.array(X_test), np.array(y_test)

    # Reshape the test data for the sales type
    X_test = np.reshape(X_test, (X_test.shape[0], X_test.shape[1], 1))

    # Make predictions on the test data for the sales type
    predictions = model.predict(X_test)
    predictions = scaler.inverse_transform(predictions)

    return predictions





def fig_to_base64(fig):
    output = io.BytesIO()
    FigureCanvas(fig).print_png(output)
    image_base64 = base64.b64encode(output.getvalue()).decode('utf-8')
    return image_base64


if __name__ == '__main__':
    app.run(debug=True)
