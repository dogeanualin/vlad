from flask import Flask, render_template
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

# Load the dataset
df= pd.read_csv("grocery_final_dataset.csv")
df=df[:100]

def clear_figure():
    plt.clf()

# Define a function to plot the data distribution visualization
def plot_data_distribution():
    # Clear the current figure
    clear_figure()

    # Create a figure and axes
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111)

    # Plot histogram for order_dow
    sns.histplot(df['order_dow'], bins=7, kde=True, ax=ax)

    # Set title and labels
    ax.set_title('Order Day of Week Distribution', fontsize=16)
    ax.set_xlabel('Day of Week', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_xticks(range(7))
    ax.set_xticklabels(['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'])

    # Save the figure to a BytesIO object
    image_stream = BytesIO()
    fig.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64

def plot_order_analysis():
    # Clear the current figure
    clear_figure()

    # Create a figure and axes
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    # Plot histogram for order_hour_of_day
    sns.histplot(df['order_hour_of_day'], bins=24, kde=True, ax=ax)

    # Set title and labels
    ax.set_title('Order Hour of Day Distribution', fontsize=16)
    ax.set_xlabel('Hour of Day', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)
    ax.set_xticks(range(24))
    # Save the figure to a BytesIO object
    image_stream = BytesIO()
    fig.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64

def plot_user_analysis():
    # Clear the current figure
    clear_figure()

    # Create a figure and axes
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    # Plot histogram for days_since_prior_order
    sns.histplot(df['days_since_prior_order'], bins=30, kde=True, ax=ax)

    # Set title and labels
    ax.set_title('Days Since Prior Order Distribution', fontsize=16)
    ax.set_xlabel('Days', fontsize=12)
    ax.set_ylabel('Frequency', fontsize=12)

    image_stream = BytesIO()
    fig.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64
  


# Define a function to plot the product analysis visualization
def plot_product_analysis():
    # Clear the current figure
    clear_figure()

    # Perform product analysis (example)
    product_counts = df['product_name'].value_counts().head(10)

    # Create a figure and axes
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    # Plot horizontal bar chart
    sns.barplot(y=product_counts.index, x=product_counts.values, ax=ax)

    # Set title and labels
    ax.set_title('Top 10 Ordered Products', fontsize=16)
    ax.set_xlabel('Order Count', fontsize=12)
    ax.set_ylabel('Product', fontsize=12)

    # Save the figure to a BytesIO object
    image_stream = BytesIO()
    fig.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64

def add_reorder_percentage_visualization():
    clear_figure()
    # Calculate the percentage of reordered items
    reorder_percentage = (df['reordered'].sum() / len(df)) * 100

    # Create a bar chart or pie chart to visualize the reorder percentage
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    ax.bar(['Reordered', 'Not Reordered'], [reorder_percentage, 100 - reorder_percentage])
    ax.set_title('Percentage of Reordered Items')
    ax.set_xlabel('Reordered')
    ax.set_ylabel('Percentage')
    image_stream = BytesIO()
    fig.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64

def plot_orders_by_hour():
    # Clear the current figure
    clear_figure()

    # Create a figure and axes
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    # Plot the distribution of orders by hour of the day
    df['order_hour_of_day'].value_counts().sort_index().plot(kind='bar', ax=ax)

    # Set the title and labels
    ax.set_title('Orders by Hour of the Day')
    ax.set_xlabel('Hour of the Day')
    ax.set_ylabel('Number of Orders')
    ax.set_xticklabels(ax.get_xticks(), rotation=0)

    image_stream = BytesIO()
    fig.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64

def add_correlation_heatmap_visualization():
    clear_figure()
    # Select numerical variables for correlation analysis
    numerical_vars = ['add_to_cart_order', 'reordered', 'total_orders']

    # Create a correlation matrix
    correlation_matrix = df[numerical_vars].corr()

    # Plot the correlation heatmap
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', linewidths=0.5, ax=ax)
    ax.set_title('Correlation Matrix')
    image_stream = BytesIO()
    fig.savefig(image_stream, format='png')
    image_stream.seek(0)
    image_base64 = base64.b64encode(image_stream.getvalue()).decode('utf-8')

    return image_base64
   

# Add more functions for other visualizations
add_reorder_percentage_visualization
# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for data distribution visualization
@app.route('/reorder_percentage')
def reorder_percentage():
    image_base64 = add_reorder_percentage_visualization()
    return render_template('reorder_percentage.html', image=image_base64)

@app.route('/orders_by_hour')
def orders_by_hour():
    image_base64 = plot_orders_by_hour()
    return render_template('orders_by_hour.html', image=image_base64)

@app.route('/correlation_heatmap')
def correlation_heatmap():
    image_base64 = add_correlation_heatmap_visualization()
    return render_template('correlation_heatmap.html', image=image_base64)

@app.route('/data_distribution')
def data_distribution():
    image_base64 = plot_data_distribution()
    return render_template('data_distribution.html', image=image_base64)

# Route for product analysis visualization
@app.route('/product_analysis')
def product_analysis():
    image_base64 = plot_product_analysis()
    return render_template('product_analysis.html', image=image_base64)


# Route for product analysis visualization
@app.route('/order_analysis')
def order_analysis():
    image_base64 = plot_order_analysis()
    return render_template('order_analysis.html', image=image_base64)

# Route for product analysis visualization
@app.route('/user_analysis')
def user_analysis():
    image_base64 = plot_user_analysis()
    return render_template('user_analysis.html', image=image_base64)

# Add more routes for other visualizations

if __name__ == '__main__':
    app.run(debug=True)
