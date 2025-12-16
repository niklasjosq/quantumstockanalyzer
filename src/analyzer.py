import google.generativeai as genai
import os

def analyze_content(api_key, ticker, content_type, text_content):
    """
    Analyzes text content (news or SEC filing) using Gemini 1.5 Flash.
    
    Args:
        api_key (str): The Google Gemini API Key.
        ticker (str): Stock ticker symbol.
        content_type (str): "News" or "SEC Filing".
        text_content (str): The text to analyze.
        
    Returns:
        dict: JSON-like structure with keys 'sentiment_score', 'sentiment_label', 'summary', 'reasoning'.
    """
    if not api_key:
        return {
            "error": "No API Key provided."
        }
        
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-flash-latest')
        
        prompt = f"""
        You are a senior financial analyst.
        Analyze the following {content_type} for the stock {ticker}.
        
        Content:
        {text_content}
        
        Task:
        1. Summarize the key points relevant to investors.
        2. Determine the potential impact on the stock price (Bullish, Bearish, or Neutral).
        3. Assign a sentiment score from 0 (Extremely Bearish) to 10 (Extremely Bullish).
        
        Format the output strictly as the following JSON (no markdown block, just raw text or simple format I can parse, but let's ask for JSON):
        {{
            "summary": "...",
            "impact": "...",
            "score": 0.0,
            "reasoning": "..."
        }}
        """
        
        response = model.generate_content(prompt)
        
        # Simple cleanup to ensure we get valid JSON-like string if model adds backticks
        text_resp = response.text.replace("```json", "").replace("```", "").strip()
        
        import json
        try:
            return json.loads(text_resp)
        except json.JSONDecodeError:
            # Fallback if specific format fails
            return {
                "summary": response.text,
                "impact": "Uncertain",
                "score": 5.0,
                "reasoning": "Model returned unstructured text."
            }
            
    except Exception as e:
        return {
            "error": str(e)
        }
