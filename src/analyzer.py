import google.generativeai as genai
import json
from typing import Any


def _extract_json_payload(response_text: str) -> dict[str, Any]:
    """
    Parses model output into a dictionary, even if it includes code fences or extra prose.
    """
    cleaned = response_text.replace("```json", "").replace("```", "").strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start == -1 or end == -1 or start >= end:
            raise
        parsed = json.loads(cleaned[start : end + 1])

    if not isinstance(parsed, dict):
        raise json.JSONDecodeError("Model output is not a JSON object.", cleaned, 0)

    return parsed


def _normalize_score(score: Any) -> float:
    try:
        numeric_score = float(score)
    except (TypeError, ValueError):
        return 5.0
    return max(0.0, min(10.0, numeric_score))


def analyze_content(api_key, ticker, content_type, text_content):
    """
    Analyzes text content (news or SEC filing) using Gemini models with fallback.
    
    Args:
        api_key (str): The Google Gemini API Key.
        ticker (str): Stock ticker symbol.
        content_type (str): "News" or "SEC Filing".
        text_content (str): The text to analyze.
        
    Returns:
        dict: Structured payload with keys 'summary', 'impact', 'score', and 'reasoning'.
    """
    if not api_key:
        return {
            "error": "No API Key provided."
        }
        
    try:
        genai.configure(api_key=api_key)
        
        # Try a list of models in order of preference.
        models_to_try = [
            "gemini-2.5-flash",
            "gemini-2.0-flash",
            "gemini-flash-latest",
        ]
        
        last_exception = None
        response = None
        
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

        for model_name in models_to_try:
            try:
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(
                    prompt,
                    generation_config={"response_mime_type": "application/json"},
                )
                break # If successful, exit loop
            except Exception as e:
                last_exception = e
                continue
                
        if not response:
             # If all models failed, try to list available models to help user debug
            try:
                available_models = [m.name for m in genai.list_models()]
                return {"error": f"Failed with models {models_to_try}. Available models: {available_models}. Last error: {last_exception}"}
            except Exception:
                return {"error": f"All models failed. Last error: {last_exception}"}

        
        response_text = getattr(response, "text", "") or ""
        if not response_text:
            return {
                "summary": "No response text returned by model.",
                "impact": "Uncertain",
                "score": 5.0,
                "reasoning": "The model returned an empty response.",
            }
        
        try:
            parsed = _extract_json_payload(response_text)
            return {
                "summary": parsed.get("summary", "No summary provided."),
                "impact": parsed.get("impact", "Uncertain"),
                "score": _normalize_score(parsed.get("score", 5.0)),
                "reasoning": parsed.get("reasoning", "No reasoning provided."),
            }
        except json.JSONDecodeError:
            # Fallback if specific format fails
            return {
                "summary": response_text,
                "impact": "Uncertain",
                "score": 5.0,
                "reasoning": "Model returned unstructured text."
            }
            
    except Exception as e:
        return {
            "error": str(e)
        }
