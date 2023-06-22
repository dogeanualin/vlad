from flask import Flask, render_template, request,send_from_directory

import eda


app = Flask(__name__)


@app.route('/')
def hello_world():  # put application's code here
    return render_template('main.html',static_url_path='/static')


@app.route('/eda/reorder_percentage')
def serve_static():
    image_base64 = eda.add_reorder_percentage_visualization()
    return render_template('eda/reorder_percentage.html', image=image_base64,static_url_path='/static')
@app.route('/eda/orders_by_hour')
def orders_by_hour():
    image_base64 = eda.plot_orders_by_hour()
    return render_template('eda/orders_by_hour.html', image=image_base64)

if __name__ == '__main__':
    app.run()
