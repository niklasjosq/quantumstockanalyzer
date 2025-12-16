import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from src.data_fetcher import fetch_stock_history, fetch_stock_info, fetch_news, fetch_sec_filings
from src.analyzer import analyze_content

# Page Config
st.set_page_config(page_title="Stock News Feeder", layout="wide", page_icon="📈")

# Custom CSS for "Dark Mode" aesthetic if needed, though Streamlit handles dark mode well by default.
st.markdown("""
<style>
    .stApp {
        background-color: #0e1117;
        color: #fafafa;
    }
    .stCard {
        background-color: #262730;
        padding: 1rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("Settings")
    
    api_key = st.text_input("Gemini API Key", type="password", help="Enter your Google Gemini API key here.")
    
    default_tickers = ["IONQ", "RGTI", "QUBT", "QBTS", "ARQQ", "CCCX", "CHAC", "DMYY"]
    selected_ticker = st.selectbox("Select Stock", default_tickers + ["Other..."])
    
    if selected_ticker == "Other...":
        selected_ticker = st.text_input("Enter Ticker Symbol").upper()
    
    period = st.selectbox("History Period", ["1mo", "3mo", "6mo", "1y", "5y"], index=3)

if not selected_ticker:
    st.warning("Please select or enter a ticker.")
    st.stop()

# Main Content
st.title(f"{selected_ticker} - Stock Dashboard")

# create tabs
tab1, tab2, tab3 = st.tabs(["Dashboard", "Latest News", "SEC Filings & Analysis"])

# --- Tab 1: Dashboard ---
with tab1:
    st.subheader("Price History")
    
    with st.spinner("Fetching stock data..."):
        try:
            hist = fetch_stock_history(selected_ticker, period=period)
            info = fetch_stock_info(selected_ticker)
            
            # Key Stats
            col1, col2, col3, col4 = st.columns(4)
            current_price = info.get('currentPrice', info.get('previousClose', 'N/A'))
            col1.metric("Current Price", f"${current_price}")
            col2.metric("Market Cap", f"${info.get('marketCap', 'N/A')}")
            col3.metric("52W High", f"${info.get('fiftyTwoWeekHigh', 'N/A')}")
            col4.metric("52W Low", f"${info.get('fiftyTwoWeekLow', 'N/A')}")
            
            # Chart
            fig = go.Figure(data=[go.Candlestick(x=hist.index,
                            open=hist['Open'],
                            high=hist['High'],
                            low=hist['Low'],
                            close=hist['Close'])])
            fig.update_layout(template="plotly_dark", height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            st.caption(info.get('longBusinessSummary', 'No summary available.'))
            
        except Exception as e:
            st.error(f"Error loading dashboard data: {e}")

# --- Tab 2: News ---
with tab2:
    st.subheader("Latest News")
    with st.spinner("Fetching news..."):
        try:
            news_items = fetch_news(selected_ticker)
            if not news_items:
                st.info("No recent news found.")
            
            for item in news_items:
                with st.container():
                    col_img, col_text = st.columns([1, 4])
                    
                    with col_img:
                        if item.get('thumbnail'):
                            st.image(item['thumbnail'], use_container_width=True)
                        else:
                            st.markdown("📷 *No Image*")
                            
                    with col_text:
                        st.markdown(f"### [{item.get('title', 'No Title')}]({item.get('link', '#')})")
                        
                        pub_time = item.get('publishTime', 'N/A')
                        if 'T' in str(pub_time):
                            pub_time = pub_time.replace('T', ' ').replace('Z', '')
                            
                        st.caption(f"**{item.get('publisher', 'Unknown')}** • {pub_time}")
                        
                    st.divider()
        except Exception as e:
            st.error(f"Error fetching news: {e}")

# --- Tab 3: Filings & Analysis ---
with tab3:
    st.subheader("SEC Filings (EDGAR)")
    
    if not api_key:
        st.warning("⚠️ Enter Gemini API Key in sidebar to enable AI Analysis.")
    
    with st.spinner("Fetching filings..."):
        filings = fetch_sec_filings(selected_ticker)
    
    if not filings:
        st.info("No recent SEC filings found via RSS.")
    else:
        for filing in filings[:10]: # Limit to 10
            with st.expander(f"{filing['category']} - {filing['title']} ({filing['updated'][:10]})"):
                st.markdown(f"**Link:** [View Full Filing]({filing['link']})")
                st.write(filing['summary'])
                
                if api_key:
                    if st.button(f"Analyze Impact (Gemini)", key=filing['link']):
                        with st.spinner("Analyzing with Gemini Flash..."):
                            # We construct a text blob from the summary + title. 
                            # For full Deep Dive we'd need to scrape the link, but summary is often distinct enough for 'Flash' demo.
                            text_to_analyze = f"Title: {filing['title']}\nCategory: {filing['category']}\nSummary: {filing['summary']}"
                            
                            analysis = analyze_content(api_key, selected_ticker, "SEC Filing", text_to_analyze)
                            
                            if "error" in analysis:
                                st.error(analysis["error"])
                            else:
                                color = "green" if analysis.get("impact") == "Bullish" else "red" if analysis.get("impact") == "Bearish" else "grey"
                                st.markdown(f"#### AI Impact Analysis: :{color}[{analysis.get('impact')}]")
                                st.metric("Sentiment Score", f"{analysis.get('score')}/10")
                                st.write(f"**Summary:** {analysis.get('summary')}")
                                st.write(f"**Reasoning:** {analysis.get('reasoning')}")
