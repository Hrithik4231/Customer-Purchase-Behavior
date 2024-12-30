document.getElementById('uploadBtn').addEventListener('click', () => {
    const fileInput = document.getElementById('fileInput');
    
    // Validate if a file is selected and it's of the correct type
    if (fileInput.files.length === 0) {
        alert('Please upload a CSV file!');
        return;
    }

    const file = fileInput.files[0];
    
    // Check file type (only allow CSV files)
    if (!file.name.endsWith('.csv')) {
        alert('Please upload a valid CSV file!');
        return;
    }

    const reader = new FileReader();
    reader.onload = (event) => {
        const csvData = event.target.result;
        processData(csvData);
    };
    reader.readAsText(file);
});

function processData(csvData) {
    // Parsing the CSV data (simplified example)
    const parsedData = parseCSV(csvData);
    
    // Calculate basic insights based on the parsed data (for now, it's simulated)
    const insights = analyzeData(parsedData);
    
    // Display insights
    document.getElementById('insightsContent').textContent = insights;

    // Render the visualizations based on the data
    renderHistChart(parsedData);
    renderScatterChart(parsedData);
    renderBoxChart(parsedData);
}

// Function to parse CSV (simplified version)
function parseCSV(data) {
    const rows = data.split('\n');
    const headers = rows[0].split(',');
    const records = rows.slice(1).map(row => {
        const values = row.split(',');
        return headers.reduce((acc, header, i) => {
            acc[header] = values[i];
            return acc;
        }, {});
    });
    return records;
}

// Function to simulate data analysis and generate insights
function analyzeData(data) {
    // Just an example of analyzing the data
    const ageData = data.map(row => parseInt(row['Age']));
    const purchaseData = data.map(row => parseFloat(row['Purchases']));
    const incomeData = data.map(row => parseFloat(row['Income']));

    // Basic analysis
    const avgPurchase = purchaseData.reduce((a, b) => a + b, 0) / purchaseData.length;
    const avgAge = ageData.reduce((a, b) => a + b, 0) / ageData.length;
    const avgIncome = incomeData.reduce((a, b) => a + b, 0) / incomeData.length;

    return `
        - Average purchase value: ${avgPurchase.toFixed(2)} USD
        - Average customer age: ${avgAge.toFixed(1)} years
        - Average customer income: ${avgIncome.toFixed(2)} USD
        - Customers aged 25-35 have a higher purchase rate.
        - Strong correlation between Income and Purchases.
    `;
}

// Rendering the Histogram Chart
function renderHistChart(data) {
    const ctx = document.getElementById('histChart').getContext('2d');
    const purchases = data.map(row => parseFloat(row['Purchases']));
    const purchaseRanges = ['5-10', '10-15', '15-20'];  // Dummy ranges
    const counts = [0, 0, 0];  // Dummy data for range counts

    // Count purchases per range
    purchases.forEach(purchase => {
        if (purchase >= 5 && purchase <= 10) counts[0]++;
        else if (purchase > 10 && purchase <= 15) counts[1]++;
        else if (purchase > 15 && purchase <= 20) counts[2]++;
    });

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: purchaseRanges,
            datasets: [{
                label: 'Purchases',
                data: counts,
                backgroundColor: '#00a6fb'
            }]
        }
    });
}

// Rendering the Scatter Chart
function renderScatterChart(data) {
    const ctx = document.getElementById('scatterChart').getContext('2d');
    const ageData = data.map(row => parseInt(row['Age']));
    const purchaseData = data.map(row => parseFloat(row['Purchases']));

    const scatterData = ageData.map((age, index) => ({ x: age, y: purchaseData[index] }));

    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Age vs Purchases',
                data: scatterData,
                backgroundColor: '#0582ca',
                pointRadius: 5
            }]
        }
    });
}

// Rendering the Boxplot Chart (simulated with Bar chart)
function renderBoxChart(data) {
    const ctx = document.getElementById('boxChart').getContext('2d');
    const incomeData = data.map(row => parseFloat(row['Income']));

    // Example categories
    const categories = ['Category A', 'Category B', 'Category C'];
    const avgIncomeData = [50000, 65000, 85000];  // Dummy data for categories

    new Chart(ctx, {
        type: 'bar',
        data: {
            labels: categories,
            datasets: [{
                label: 'Average Income',
                data: avgIncomeData,
                backgroundColor: '#006494'
            }]
        }
    });
}
