from flask import Flask, render_template, request,redirect

import eda
from sarimax import predict_and_visualize
from xgboostpredict import predict
import LSTM
import databasegr

app = Flask(__name__)


@app.route('/')
def home():  # put application's code here
    return render_template('main.html', static_url_path='/static')


@app.route('/eda/reorder_percentage')
def reorder_percentage():
    menu = "reorder_percentage"
    image_base64 = eda.add_reorder_percentage_visualization()
    return render_template('eda/reorder_percentage.html', image=image_base64, menu = menu)
@app.route('/eda/orders_by_hour')
def orders_by_hour():
    menu = "orders_by_hour"
    image_base64 = eda.plot_orders_by_hour()
    return render_template('eda/orders_by_hour.html', image=image_base64, menu = menu)
@app.route('/eda/product_analysis')
def product_analysis():
    menu = "product_analysis"
    image_base64 = eda.plot_product_analysis()
    return render_template('eda/product_analysis.html', image=image_base64, menu = menu)

@app.route('/eda/correlation_heatmap')
def correlation_heatmap():
    menu = "correlation_heatmap"
    image_base64 = eda.add_correlation_heatmap_visualization()
    return render_template('eda/correlation_heatmap.html', image=image_base64, menu = menu)
@app.route('/eda/data_distribution')
def data_distribution():
    menu = "data_distribution"
    image_base64 = eda.plot_data_distribution()
    return render_template('eda/data_distribution.html', image=image_base64, menu = menu)

# Route for product analysis visualization
@app.route('/eda/order_analysis')
def order_analysis():
    menu = "order_analysis"
    image_base64 = eda.plot_order_analysis()
    return render_template('eda/order_analysis.html', image=image_base64, menu = menu)

# Route for product analysis visualization
@app.route('/eda/user_analysis')
def user_analysis():
    menu = "user_analysis"
    image_base64 = eda.plot_user_analysis()
    return render_template('eda/user_analysis.html', image=image_base64, menu = menu)

@app.route('/sarimax', methods=['GET', 'POST'])
def sarimax():
    menu = "sarimax"
    if request.method == 'POST':
        sales_type = request.form['sales_type']
        return predict_and_visualize(sales_type)
    return render_template('sarimax/sarimax.html', menu=menu)

@app.route('/xgboost', methods=['GET', 'POST'])
def xgboost():
    menu = "xgboost"
    if request.method == 'POST':
        sales_type = request.form['sales_type']
        return predict(sales_type)
    return render_template('xgboost/xgboost.html', menu=menu)


@app.route('/lstm')
def lstm():
    menu = "lstm"

    predictions1 = LSTM.forecast_sales(LSTM.scaled_data1, LSTM.scaler1, LSTM.model1)

    # Forecast weekly sales
    predictions2 = LSTM.forecast_sales(LSTM.scaled_data2, LSTM.scaler2, LSTM.model2)

    # Forecast daily sales
    predictions3 = LSTM.forecast_sales(LSTM.scaled_data3, LSTM.scaler3, LSTM.model3)

    # Convert the figures to base64 encoded strings
    fig1 = LSTM.Figure(figsize=(10, 6))
    ax1 = fig1.add_subplot(111)
    ax1.plot(LSTM.sales_ts1.index[LSTM.train_size + LSTM.n_steps:], LSTM.sales_ts1[LSTM.train_size + LSTM.n_steps:], label='Actual Sales')
    ax1.plot(LSTM.sales_ts1.index[LSTM.train_size + LSTM.n_steps:], predictions1, label='Forecasted Sales')
    ax1.set_xlabel('Time')
    ax1.set_ylabel('Product Sales')
    ax1.set_title('Actual vs Forecasted Sales (Total)')
    ax1.legend()
    image_base64_1 = LSTM.fig_to_base64(fig1)

    fig2 = LSTM.Figure(figsize=(10, 6))
    ax2 = fig2.add_subplot(111)
    ax2.plot(LSTM.sales_ts2.index[LSTM.train_size + LSTM.n_steps:], LSTM.sales_ts2[LSTM.train_size + LSTM.n_steps:], label='Actual Sales')
    ax2.plot(LSTM.sales_ts2.index[LSTM.train_size + LSTM.n_steps:], predictions2, label='Forecasted Sales')
    ax2.set_xlabel('Time')
    ax2.set_ylabel('Product Sales')
    ax2.set_title('Actual vs Forecasted Sales (Weekly)')
    ax2.legend()
    image_base64_2 = LSTM.fig_to_base64(fig2)

    fig3 = LSTM.Figure(figsize=(10, 6))
    ax3 = fig3.add_subplot(111)
    ax3.plot(LSTM.sales_ts3.index[LSTM.train_size + LSTM.n_steps:], LSTM.sales_ts3[LSTM.train_size + LSTM.n_steps:], label='Actual Sales')
    ax3.plot(LSTM.sales_ts3.index[LSTM.train_size + LSTM.n_steps:], predictions3, label='Forecasted Sales')
    ax3.set_xlabel('Time')
    ax3.set_ylabel('Product Sales')
    ax3.set_title('Actual vs Forecasted Sales (Daily)')
    ax3.legend()
    image_base64_3 = LSTM.fig_to_base64(fig3)

    return render_template('lstm/lstm.html', image1=image_base64_1, image2=image_base64_2, image3=image_base64_3,menu=menu)

@app.route('/database')
def database():
    # Fetch the table names from the database

    menu = "lstm"
    return render_template('database/database.html',menu=menu )
@app.route('/database/<database>')
def show_tables(database):
    # Fetch the table names from the database
    tables = databasegr.fetch_table_names(database)

    return render_template('database/tables.html', database=database, tables=tables)


@app.route('/database/<database>/<table_name>')
def show_table_columns(database, table_name):
    # Select the appropriate database based on the button click
    if database == "OLAP Database":
        cnx = databasegr.olap_cnx
        cursor = databasegr.olap_cursor
    elif database == "OLTP Database":
        cnx = databasegr.oltp_cnx
        cursor = databasegr.oltp_cursor
    else:
        return "Invalid database"

    # Fetch the column names from the selected table
    cursor.execute(f"SHOW COLUMNS FROM {table_name}")
    columns = cursor.fetchall()

    return render_template('database/columns.html', database=database, table_name=table_name, columns=columns)


if __name__ == '__main__':
    app.run()
    app.run(debug=True)
    databasegr.window.mainloop()
