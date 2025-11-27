import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots

# Premium Fintech Palette
COLORS = {
    'background': 'rgba(0,0,0,0)',
    'text': '#ffffff',
    'grid': 'rgba(255,255,255,0.05)',
    'primary': '#2962ff',
    'secondary': '#9ca3af',
    'success': '#00c853',
    'danger': '#d50000',
    'warning': '#ffd600',
    'purple': '#7c4dff',
    'cyan': '#00b0ff'
}

FONT_FAMILY = "Inter, sans-serif"

def update_layout_common(fig, title, height=None):
    """Applies common premium layout settings to a figure."""
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['background'],
        plot_bgcolor=COLORS['background'],
        font=dict(family=FONT_FAMILY, color=COLORS['text']),
        title=dict(text=title, font=dict(size=14, color=COLORS['secondary'])),
        xaxis=dict(showgrid=False, showline=True, linecolor=COLORS['grid']),
        yaxis=dict(showgrid=True, gridcolor=COLORS['grid'], showline=False),
        margin=dict(l=10, r=10, t=40, b=10),
        hovermode='x unified'
    )
    if height:
        fig.update_layout(height=height)
    return fig

def create_volatility_chart(df):
    """Creates a figure for volatility analysis."""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.1, subplot_titles=('Price History', 'Volatility (Rolling Std Dev)'))
    
    # Price
    fig.add_trace(go.Scatter(x=df.index, y=df['Adj Close'], name='Adj Close', 
                             line=dict(color=COLORS['primary'], width=2)), row=1, col=1)
    
    # Volatility
    fig.add_trace(go.Scatter(x=df.index, y=df['RollingVol_30'], name='30-Day Volatility', 
                             line=dict(color=COLORS['warning'], width=1.5)), row=2, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['RollingVol_90'], name='90-Day Volatility', 
                             line=dict(color=COLORS['purple'], dash='dash', width=1.5)), row=2, col=1)
    
    update_layout_common(fig, "Price & Volatility Analysis", height=600)
    return fig

def create_seasonal_charts(trends_data):
    """Creates figures for seasonal trends."""
    # Monthly Trend
    monthly_fig = px.bar(trends_data['monthly'], x=trends_data['monthly'].index, y=trends_data['monthly'].values,
                         title="Average Monthly Returns", labels={'y': 'Avg Return', 'index': 'Month'})
    monthly_fig.update_traces(marker_color=COLORS['primary'], marker_line_width=0)
    update_layout_common(monthly_fig, "Average Monthly Returns")
    
    # Day of Week Trend
    day_fig = px.bar(trends_data['day_of_week'], x=trends_data['day_of_week'].index, y=trends_data['day_of_week'].values,
                     title="Average Day-of-Week Returns", labels={'y': 'Avg Return', 'index': 'Day'})
    day_fig.update_traces(marker_color=COLORS['cyan'], marker_line_width=0)
    update_layout_common(day_fig, "Average Day-of-Week Returns")
    
    # Yearly Trend
    yearly_fig = px.bar(trends_data['yearly'], x=trends_data['yearly'].index, y=trends_data['yearly'].values,
                        title="Average Yearly Returns", labels={'y': 'Avg Return', 'index': 'Year'})
    yearly_fig.update_traces(marker_color=COLORS['purple'], marker_line_width=0)
    update_layout_common(yearly_fig, "Average Yearly Returns")
    
    return monthly_fig, day_fig, yearly_fig

def create_volume_chart(df, monthly_volume):
    """Creates figures for volume analysis."""
    # Volume over time with MA
    vol_fig = go.Figure()
    vol_fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color='rgba(255, 255, 255, 0.1)'))
    vol_fig.add_trace(go.Scatter(x=df.index, y=df['Volume_MA20'], name='20-Day MA', line=dict(color=COLORS['cyan'], width=1.5)))
    update_layout_common(vol_fig, "Volume Analysis", height=400)
    
    # Monthly Volume
    monthly_vol_fig = px.bar(monthly_volume, x=monthly_volume.index, y=monthly_volume.values,
                             title="Average Monthly Volume", labels={'y': 'Avg Volume', 'index': 'Month'})
    monthly_vol_fig.update_traces(marker_color=COLORS['secondary'], marker_line_width=0)
    update_layout_common(monthly_vol_fig, "Average Monthly Volume")
    
    return vol_fig, monthly_vol_fig

def create_sector_chart(sector_perf):
    """Creates a figure for sector comparison."""
    fig = px.line(sector_perf, x=sector_perf.index, y=sector_perf.columns, title="Sector Performance Comparison")
    update_layout_common(fig, "Sector Performance Comparison", height=500)
    return fig

def create_main_chart(df):
    """Creates the main candlestick chart with volume and MA overlays."""
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, 
                        vertical_spacing=0.05, row_heights=[0.7, 0.3])

    # Candlestick
    fig.add_trace(go.Candlestick(x=df.index,
                open=df['Open'], high=df['High'],
                low=df['Low'], close=df['Adj Close'],
                name='OHLC',
                increasing_line_color=COLORS['success'], decreasing_line_color=COLORS['danger']), row=1, col=1)

    # Moving Averages
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name='50-Day SMA', 
                             line=dict(color=COLORS['warning'], width=1)), row=1, col=1)
    fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], name='200-Day SMA', 
                             line=dict(color=COLORS['cyan'], width=1)), row=1, col=1)

    # Volume
    colors = [COLORS['success'] if row['Open'] - row['Adj Close'] >= 0 
              else COLORS['danger'] for index, row in df.iterrows()]
    fig.add_trace(go.Bar(x=df.index, y=df['Volume'], name='Volume', marker_color=colors), row=2, col=1)

    update_layout_common(fig, "Price Action & Volume", height=700)
    fig.update_xaxes(rangeslider_visible=False)
    
    return fig

def create_technical_charts(df):
    """Creates RSI and MACD charts."""
    # RSI
    rsi_fig = go.Figure()
    rsi_fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI', line=dict(color=COLORS['purple'])))
    rsi_fig.add_hline(y=70, line_dash="dash", line_color=COLORS['danger'], opacity=0.5)
    rsi_fig.add_hline(y=30, line_dash="dash", line_color=COLORS['success'], opacity=0.5)
    update_layout_common(rsi_fig, "Relative Strength Index (RSI)", height=300)

    # MACD
    macd_fig = go.Figure()
    macd_fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD', line=dict(color=COLORS['cyan'])))
    macd_fig.add_trace(go.Scatter(x=df.index, y=df['Signal_Line'], name='Signal', line=dict(color=COLORS['warning'])))
    macd_fig.add_bar(x=df.index, y=df['MACD'] - df['Signal_Line'], name='Histogram', marker_color='rgba(255,255,255,0.1)')
    update_layout_common(macd_fig, "MACD", height=300)
    
    return rsi_fig, macd_fig
