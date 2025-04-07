from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    
    files = request.files.getlist('file')
    all_data = []
    
    for file in files:
        try:
            if file.filename.lower().endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)
            
            # Smart column mapping using fuzzy matching and synonyms
            column_patterns = {
                'customer_id': ['user_id', 'customer_number', 'client_id', 'cust_id', 'customerid', 'userid', 'id'],
                'amount': ['purchase_amount', 'total_price', 'price', 'total', 'sales_amount', 'transaction_amount'],
                'purchase_date': ['date', 'transaction_date', 'order_date', 'sales_date', 'purchase_time']
            }
            
            # Function to find best matching column
            def find_matching_column(columns, patterns):
                for col in columns:
                    col_lower = col.lower().replace('_', '').replace(' ', '')
                    for pattern in patterns:
                        if pattern.lower().replace('_', '').replace(' ', '') in col_lower:
                            return col
                return None
            
            # Map columns based on patterns
            column_mapping = {}
            for standard_col, patterns in column_patterns.items():
                matched_col = find_matching_column(df.columns, patterns + [standard_col])
                if matched_col and matched_col != standard_col:
                    column_mapping[matched_col] = standard_col
            
            # Rename columns if matches found
            if column_mapping:
                df = df.rename(columns=column_mapping)
            
            # Add current date if purchase_date is missing
            if 'purchase_date' not in df.columns:
                df['purchase_date'] = datetime.now().strftime('%Y-%m-%d')
            
            # Basic data validation and mapping feedback
            required_columns = ['customer_id', 'purchase_date', 'amount']
            missing_columns = [col for col in required_columns if col.lower() not in 
                             [c.lower() for c in df.columns]]
            
            if missing_columns:
                # Provide suggestions for missing columns
                suggestions = {}
                for col in missing_columns:
                    potential_matches = [c for c in df.columns if any(pattern.lower().replace('_', '').replace(' ', '') in 
                                       c.lower().replace('_', '').replace(' ', '') for pattern in column_patterns[col])]
                    if potential_matches:
                        suggestions[col] = potential_matches
                
                error_message = {
                    'error': f'Missing required columns: {missing_columns}',
                    'suggestions': suggestions if suggestions else None,
                    'mapped_columns': column_mapping
                }
                return jsonify(error_message), 400
                
            all_data.append(df)
        except Exception as e:
            return jsonify({'error': f'Error processing file {file.filename}: {str(e)}'}), 400
    
    # Combine all dataframes
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        
        # Perform analysis
        analysis_results = analyze_customer_data(combined_df)
        return jsonify(analysis_results), 200
    
    return jsonify({'error': 'No valid data found'}), 400

def analyze_customer_data(df):
    # Customer Segmentation
    features = ['amount']
    X = df[features]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=3, random_state=42)
    df['segment'] = kmeans.fit_predict(X_scaled)
    
    # Purchase Patterns
    df['purchase_date'] = pd.to_datetime(df['purchase_date'])
    monthly_purchases = df.groupby(df['purchase_date'].dt.to_period('M')).agg({
        'amount': 'sum',
        'customer_id': 'nunique'
    }).reset_index()
    
    # Customer Metrics
    customer_metrics = df.groupby('customer_id').agg({
        'amount': ['count', 'sum', 'mean'],
        'purchase_date': ['min', 'max']
    }).reset_index()
    
    # Format results
    results = {
        'segmentation': {
            'segment_counts': df['segment'].value_counts().to_dict(),
            'segment_avg_purchase': df.groupby('segment')['amount'].mean().to_dict()
        },
        'purchase_patterns': {
            'monthly_revenue': monthly_purchases['amount'].tolist(),
            'monthly_active_customers': monthly_purchases['customer_id'].tolist(),
            'months': [str(period) for period in monthly_purchases['purchase_date']]
        },
        'customer_metrics': {
            'total_customers': len(customer_metrics),
            'avg_purchase_value': float(customer_metrics['amount']['mean'].mean()),
            'total_revenue': float(customer_metrics['amount']['sum'].sum())
        }
    }
    
    return results

@app.route('/api/recommendations', methods=['POST'])
def get_recommendations():
    data = request.get_json()
    customer_id = data.get('customer_id')
    
    if not customer_id:
        return jsonify({'error': 'Customer ID is required'}), 400
    
    # Implement recommendation logic here
    # This is a placeholder that returns dummy recommendations
    recommendations = {
        'similar_products': ['Product A', 'Product B', 'Product C'],
        'based_on_history': ['Product X', 'Product Y', 'Product Z']
    }
    
    return jsonify(recommendations), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)