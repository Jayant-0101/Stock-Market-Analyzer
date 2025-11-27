import dash
from dash import dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as go

from data_loader import fetch_stock_data, fetch_sector_data, fetch_stock_news, fetch_fundamentals, fetch_nifty50_ticker_data
from analysis import calculate_volatility, calculate_seasonal_trends, calculate_volume_analysis, calculate_sector_performance, predict_price, calculate_technical_indicators
from components import create_volatility_chart, create_seasonal_charts, create_volume_chart, create_sector_chart, create_main_chart, create_technical_charts

# Rich Console
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.layout import Layout
from rich import box

console = Console()

def print_terminal_report(ticker, info, df):
    """Prints a rich terminal report."""
    console.clear()
    
    # Header
    console.print(Panel(f"[bold cyan]STOCK ANALYSIS TERMINAL: {ticker}[/bold cyan]", box=box.DOUBLE))
    
    # Price Table
    price_table = Table(title="Price Data", box=box.SIMPLE)
    price_table.add_column("Metric", style="cyan")
    price_table.add_column("Value", style="white")
    
    price_table.add_row("Current Price", f"{info.get('currency', '')} {info.get('currentPrice', 'N/A')}")
    price_table.add_row("Open", str(info.get('open', 'N/A')))
    price_table.add_row("High", str(info.get('dayHigh', 'N/A')))
    price_table.add_row("Low", str(info.get('dayLow', 'N/A')))
    price_table.add_row("Volume", str(info.get('volume', 'N/A')))
    
    # Fundamentals Table
    fund_table = Table(title="Fundamentals", box=box.SIMPLE)
    fund_table.add_column("Metric", style="magenta")
    fund_table.add_column("Value", style="white")
    
    fund_table.add_row("Market Cap", str(info.get('marketCap', 'N/A')))
    fund_table.add_row("P/E Ratio", str(info.get('trailingPE', 'N/A')))
    fund_table.add_row("P/B Ratio", str(info.get('priceToBook', 'N/A')))
    fund_table.add_row("Div Yield", str(info.get('dividendYield', 'N/A')))
    
    # Print Tables
    console.print(price_table)
    console.print(fund_table)
    console.print(f"[bold green]Analysis Complete for {ticker}[/bold green]")

# Initialize App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])
server = app.server

# Fetch Nifty 50 Ticker Data on startup
print("Initializing ticker tape with Nifty 50 data...")
ticker_tape_data = fetch_nifty50_ticker_data()

def create_ticker_tape():
    items = []
    for item in ticker_tape_data:
        # Match new success/danger colors
        color = "#10b981" if "+" in item["change"] else "#ef4444"
        items.append(html.Span([
            html.Span(item["symbol"], className="text-white me-2"),
            html.Span(item["price"], className="me-2"),
            html.Span(item["change"], style={"color": color})
        ], className="ticker-item"))
    
    # Duplicate items for seamless loop
    items_duplicate = items.copy()
    
    return html.Div(
        html.Div(items + items_duplicate, className="ticker-content"), 
        className="ticker-tape"
    )

# Layout
app.layout = html.Div([
    # Ticker Tape
    create_ticker_tape(),
    
    # Main Dashboard Container
    html.Div([
        # Metrics Grid
        html.Div(id="metrics-grid", className="metrics-grid"),
        
        # Dashboard Grid (Charts + Sidebar)
        html.Div([
            # Main Content - Charts
            html.Div([
                dcc.Loading(
                    id="loading-charts",
                    type="cube",
                    color="#3b82f6", # Royal Blue
                    children=[html.Div(id="charts-container")]
                )
            ], className="main-content"),
            
            # Sidebar
            html.Div([
                # Search/Input Card
                html.Div([
                    html.H6("STOCK ANALYZER", className="terminal-header mb-3"),
                    html.Label("Ticker Symbol", className="text-secondary small mb-2"),
                    html.Div([
                        dbc.Input(
                            id="ticker-input", 
                            placeholder="RELIANCE.NS", 
                            type="text", 
                            value="RELIANCE.NS", 
                            className="me-2"
                        ),
                        dbc.Button("GO", id="analyze-btn", color="primary", style={"width": "80px"}),
                    ], className="d-flex mb-3"),
                ], className="sidebar-card"),
                
                # Terminal Panels
                html.Div(id="terminal-panels-container"),
                
                # Prediction Card
                html.Div(id="prediction-container"),
                
                # News Feed
                html.Div([
                    html.H6("LIVE NEWS", className="terminal-header mb-3"),
                    html.Div(id="news-feed-container", className="news-feed")
                ], className="sidebar-card")
            ], className="sidebar")
        ], className="dashboard-container")
    ])
])

@app.callback(
    [Output("metrics-grid", "children"),
     Output("charts-container", "children"),
     Output("news-feed-container", "children"),
     Output("prediction-container", "children"),
     Output("terminal-panels-container", "children")],
    Input("analyze-btn", "n_clicks"),
    State("ticker-input", "value")
)
def update_dashboard(n_clicks, ticker):
    if not ticker:
        return [], dbc.Alert("Enter Ticker", color="warning"), [], [], []
    
    try:
        # Fetch Data
        df = fetch_stock_data(ticker)
        if df.empty:
            return dbc.Alert(f"No data found for ticker symbol '{ticker}'. Please check the symbol and try again.", color="danger", className="glass-card"), [], [], []
        
        # Fetch Fundamentals
        fund_info = fetch_fundamentals(ticker)
        
        # Print to Console (Rich)
        print_terminal_report(ticker, fund_info, df)
        
        # 1. Analysis & Charts
        df = calculate_volatility(df)
        df = calculate_technical_indicators(df) # Add technicals
        trends = calculate_seasonal_trends(df)
        df, monthly_vol = calculate_volume_analysis(df)
        
        main_fig = create_main_chart(df)
        rsi_fig, macd_fig = create_technical_charts(df)
        vol_fig = create_volatility_chart(df)
        monthly_fig, day_fig, yearly_fig = create_seasonal_charts(trends)
        
        # Sector
        sector_tickers = ["TCS.NS", "INFY.NS", "WIPRO.NS", "TECHM.NS", "LTIM.NS"]
        sector_data = fetch_sector_data(sector_tickers)
        sector_fig = create_sector_chart(calculate_sector_performance(sector_data)) if not sector_data.empty else {}

        # 0. Metric Cards
        current_price = fund_info.get('currentPrice', 0)
        open_price = fund_info.get('open', current_price)
        day_change = current_price - open_price if current_price and open_price else 0
        day_change_pct = (day_change / open_price * 100) if open_price and open_price != 0 else 0
        
        volume = fund_info.get('volume', 0)
        market_cap = fund_info.get('marketCap', 0)
        
        # Format large numbers
        def format_number(num):
            if num >= 1e12:
                return f"₹{num/1e12:.2f}T"
            elif num >= 1e9:
                return f"₹{num/1e9:.2f}B"
            elif num >= 1e6:
                return f"₹{num/1e6:.2f}M"
            elif num >= 1e3:
                return f"₹{num/1e3:.2f}K"
            return f"₹{num:.2f}"
        
        metric_cards = [
            # Current Price Card
            html.Div([
                html.Div("Current Price", className="metric-label"),
                html.Div(f"₹{current_price:.2f}" if current_price else "N/A", className="metric-value"),
                html.Div([
                    html.Span("▲" if day_change >= 0 else "▼"),
                    html.Span(f"{abs(day_change_pct):.2f}%")
                ], className=f"metric-change {'positive' if day_change >= 0 else 'negative'}")
            ], className="metric-card animate-fade-in"),
            
            # Day Change Card
            html.Div([
                html.Div("Day Change", className="metric-label"),
                html.Div(f"₹{abs(day_change):.2f}" if day_change else "0.00", className="metric-value"),
                html.Div([
                    html.Span("Open: "),
                    html.Span(f"₹{open_price:.2f}" if open_price else "N/A")
                ], className="metric-change", style={"color": "var(--text-secondary)"})
            ], className="metric-card animate-fade-in delay-1"),
            
            # Volume Card
            html.Div([
                html.Div("Volume", className="metric-label"),
                html.Div(f"{volume:,.0f}" if volume else "N/A", className="metric-value", style={"fontSize": "1.5rem"}),
                html.Div("Trading Volume", className="metric-change", style={"color": "var(--text-secondary)"})
            ], className="metric-card animate-fade-in delay-2"),
            
            # Market Cap Card
            html.Div([
                html.Div("Market Cap", className="metric-label"),
                html.Div(format_number(market_cap) if market_cap else "N/A", className="metric-value"),
                html.Div(f"P/E: {fund_info.get('trailingPE', 'N/A')}", className="metric-change", style={"color": "var(--text-secondary)"})
            ], className="metric-card animate-fade-in delay-3")
        ]

        # 1. Charts - Updated to use chart-card class
        charts = html.Div([
            html.Div(dcc.Graph(figure=main_fig, config={'displayModeBar': False}), className="chart-card animate-slide-up"),
            html.Div([
                html.Div([
                    html.Div(dcc.Graph(figure=rsi_fig, config={'displayModeBar': False}), className="chart-card animate-slide-up delay-1", style={"width": "49%"}),
                    html.Div(dcc.Graph(figure=macd_fig, config={'displayModeBar': False}), className="chart-card animate-slide-up delay-1", style={"width": "49%"}),
                ], style={"display": "flex", "gap": "20px", "justifyContent": "space-between"}),
            ]),
            html.Div(dcc.Graph(figure=vol_fig, config={'displayModeBar': False}), className="chart-card animate-slide-up delay-2"),
            html.Div([
                html.Div([
                    html.Div(dcc.Graph(figure=monthly_fig, config={'displayModeBar': False}), className="chart-card animate-slide-up delay-2", style={"width": "49%"}),
                    html.Div(dcc.Graph(figure=day_fig, config={'displayModeBar': False}), className="chart-card animate-slide-up delay-2", style={"width": "49%"}),
                ], style={"display": "flex", "gap": "20px", "justifyContent": "space-between"}),
            ]),
            html.Div(dcc.Graph(figure=sector_fig, config={'displayModeBar': False}), className="chart-card animate-slide-up delay-3")
        ])
        
        # 2. News Feed
        news_items = fetch_stock_news(ticker)
        news_components = []
        if news_items:
            for item in news_items[:10]: # Show top 10
                title = item.get('title', 'No Title')
                publisher = item.get('publisher', 'Unknown')
                link = item.get('link', '#')
                
                card = html.Div([
                    html.A(html.H6(title, className="news-title"), href=link, target="_blank", className="text-decoration-none"),
                    html.Div(f"{publisher}", className="news-meta")
                ], className="news-card animate-fade-in")
                news_components.append(card)
        else:
            news_components.append(html.P("No recent news found.", className="text-secondary"))
            
        # 3. ML Prediction
        prediction = predict_price(df)
        if prediction:
            current = prediction['current_price']
            pred = prediction['predicted_price']
            change = ((pred - current) / current) * 100
            # Premium Palette Colors
            color = "#10b981" if change > 0 else "#ef4444"
            arrow = "▲" if change > 0 else "▼"
            
            pred_card = html.Div([
                html.H6("AI FORECAST", className="terminal-header mb-3"),
                html.Div([
                    html.Span(f"{pred:.2f}", className="prediction-value", style={"fontSize": "2rem", "color": color}),
                    html.Span(f" {arrow} {change:.2f}%", style={"color": color, "fontSize": "1rem", "marginLeft": "10px", "fontWeight": "600"})
                ], style={"marginBottom": "8px"}),
                html.Div(f"Confidence: {prediction['score']:.2f}", className="text-muted small")
            ], className="sidebar-card animate-fade-in")
        else:
            pred_card = html.Div([
                html.H6("AI FORECAST", className="terminal-header mb-3"),
                html.P("Not enough data", className="text-secondary small")
            ], className="sidebar-card")

        # 4. Terminal Panels - Wrapped in sidebar card
        def create_row(label, value):
            return html.Div([
                html.Span(label, className="terminal-label"),
                html.Span(str(value), className="terminal-value")
            ], className="terminal-row")

        terminal_panels = html.Div([
            html.H6("MARKET DATA", className="terminal-header mb-3"),
            # Price Panel
            html.Div([
                create_row("Current", f"{fund_info.get('currency', '')} {fund_info.get('currentPrice', 'N/A')}"),
                create_row("Open", fund_info.get('open', 'N/A')),
                create_row("High", fund_info.get('dayHigh', 'N/A')),
                create_row("Low", fund_info.get('dayLow', 'N/A')),
            ], className="mb-3"),
            
            html.Hr(style={"borderColor": "var(--glass-border)", "margin": "16px 0"}),
            
            html.H6("FUNDAMENTALS", className="terminal-header mb-3", style={"marginTop": "16px"}),
            # Fundamentals Panel
            html.Div([
                create_row("Market Cap", fund_info.get('marketCap', 'N/A')),
                create_row("P/E Ratio", fund_info.get('trailingPE', 'N/A')),
                create_row("P/B Ratio", fund_info.get('priceToBook', 'N/A')),
                create_row("Div Yield", fund_info.get('dividendYield', 'N/A')),
            ])
        ], className="sidebar-card animate-fade-in")

        return metric_cards, charts, news_components, pred_card, terminal_panels

    except Exception as e:
        return [], dbc.Alert(f"An error occurred: {str(e)}", color="danger", className="glass-card"), [], html.Div(), html.Div()

if __name__ == "__main__":
    app.run(debug=True)
