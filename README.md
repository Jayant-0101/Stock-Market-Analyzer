# Stock Market Analyzer

A premium, real-time stock market analysis dashboard built with Python, Dash, and Plotly. This application provides comprehensive insights into stock performance, technical indicators, and AI-driven price forecasts in a sleek, modern interface.

## 🚀 Features

*   **Real-Time Data**: Fetches live stock data using `yfinance`.
*   **Interactive Dashboard**:
    *   **Main Chart**: Candlestick charts with moving averages.
    *   **Technical Indicators**: RSI (Relative Strength Index) and MACD (Moving Average Convergence Divergence).
    *   **Volume Analysis**: Daily and monthly volume trends.
    *   **Seasonality**: Analysis of monthly and yearly performance trends.
    *   **Sector Performance**: Comparative analysis of major sector peers.
*   **AI Price Forecast**: Basic machine learning model to predict short-term price movements.
*   **Live News Feed**: Latest news articles related to the searched stock.
*   **Terminal Mode**: A "hacker-style" terminal output in the console using `rich` for quick data summaries.
*   **Premium UI**: Dark mode, glassmorphism effects, and responsive design using Dash Bootstrap Components.

## 🛠️ Technologies Used

*   **Frontend**: [Dash](https://dash.plotly.com/), [Dash Bootstrap Components](https://dash-bootstrap-components.opensource.faculty.ai/)
*   **Visualization**: [Plotly](https://plotly.com/python/)
*   **Data Source**: [yfinance](https://pypi.org/project/yfinance/)
*   **Data Processing**: [Pandas](https://pandas.pydata.org/), [NumPy](https://numpy.org/)
*   **Machine Learning**: [Scikit-learn](https://scikit-learn.org/)
*   **CLI UI**: [Rich](https://github.com/Textualize/rich)

## 📦 Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Jayant-0101/Stock-Market-Analyzer.git
    cd Stock-Market-Analyzer
    ```

2.  **Create a virtual environment (optional but recommended):**
    ```bash
    python -m venv .venv
    source .venv/bin/activate  # On Windows: .venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

## 🏃‍♂️ Usage

1.  **Run the application:**
    ```bash
    python src/app.py
    ```

2.  **Open your browser:**
    Navigate to `http://127.0.0.1:8050/` to view the dashboard.

3.  **Analyze a Stock:**
    *   Enter a ticker symbol (e.g., `RELIANCE.NS`, `AAPL`, `TSLA`) in the sidebar input.
    *   Click **GO**.
    *   View the charts, metrics, and AI predictions.
    *   Check your terminal for a quick summary report.

## 📂 Project Structure

```
Stock-Market-Analyzer/
├── assets/             # CSS and static files
├── src/                # Source code
│   ├── app.py          # Main Dash application entry point
│   ├── analysis.py     # Data processing and technical indicators
│   ├── components.py   # Dash UI components and chart generators
│   └── data_loader.py  # Data fetching logic (yfinance)
├── tests/              # Unit tests
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).