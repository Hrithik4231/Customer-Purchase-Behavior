from flask import Flask, request, render_template, send_file, jsonify
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
VISUAL_FOLDER = 'visualizations'

# Ensure folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(VISUAL_FOLDER, exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['dataset']
    if file:
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        # Perform EDA
        eda_results = perform_eda(filepath)
        return jsonify(eda_results)

    return jsonify({"error": "No file uploaded"}), 400

def perform_eda(filepath):
    # Load dataset
    df = pd.read_csv(filepath)

    # Generate visualizations
    visuals = {}
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns

    if len(numeric_cols) > 0:
        # Distribution of the first numeric column
        dist_col = numeric_cols[0]
        dist_plot_path = os.path.join(VISUAL_FOLDER, 'dist_plot.png')
        sns.histplot(df[dist_col], kde=True, bins=10, color='blue')
        plt.title(f'Distribution of {dist_col}')
        plt.savefig(dist_plot_path)
        plt.close()
        visuals['dist_plot'] = dist_plot_path

        # Correlation heatmap
        if len(numeric_cols) > 1:
            heatmap_path = os.path.join(VISUAL_FOLDER, 'heatmap.png')
            plt.figure(figsize=(10, 6))
            sns.heatmap(df[numeric_cols].corr(), annot=True, cmap='coolwarm')
            plt.title('Correlation Matrix')
            plt.savefig(heatmap_path)
            plt.close()
            visuals['heatmap'] = heatmap_path

    return {"visuals": visuals}

@app.route('/visual/<filename>')
def serve_visual(filename):
    return send_file(os.path.join(VISUAL_FOLDER, filename), mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
