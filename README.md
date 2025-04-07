# Customer Purchase Behavior Analysis System

A dynamic, data-driven project for analyzing customer purchase behavior, featuring interactive data upload capabilities, advanced analytics, and insightful visualizations.

## Features

- Multi-file Excel upload with drag-and-drop support
- Automated data processing and validation
- Customer segmentation analysis
- Purchase pattern visualization
- Interactive dashboards with real-time updates
- Flexible data format handling

## Tech Stack

### Frontend
- React 18
- Material-UI
- Recharts for data visualization
- React Dropzone for file uploads

### Backend
- Flask
- Pandas for data processing
- Scikit-learn for customer segmentation
- NumPy for numerical computations

## Setup Instructions

### Backend Setup

1. Create a Python virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # On Windows
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the Flask server:
   ```bash
   python app.py
   ```
   The backend server will run on http://localhost:5000

### Frontend Setup

1. Install Node.js dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm start
   ```
   The frontend application will run on http://localhost:3000

## Usage

1. Launch both the backend and frontend servers
2. Open http://localhost:3000 in your browser
3. Use the drag-and-drop interface to upload Excel files
4. The system will automatically process the data and display insights

## Data Format Requirements

The system expects Excel files (.xlsx or .xls) with the following columns:
- customer_id: Unique identifier for each customer
- purchase_date: Date of purchase
- amount: Purchase amount

Additional columns will be processed but are not required for basic analysis.

## Analysis Features

1. Customer Segmentation
   - Automated clustering based on purchase behavior
   - Segment visualization and analysis

2. Purchase Patterns
   - Monthly revenue trends
   - Customer activity analysis
   - Seasonal pattern detection

3. Key Metrics
   - Total customer count
   - Average purchase value
   - Total revenue
   - Customer lifetime value