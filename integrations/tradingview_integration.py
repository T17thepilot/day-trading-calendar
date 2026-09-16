"""
TradingView Integration Guide
How to connect your custom indicators with the Trading Desk Calendar API
"""

# ============================================================================
# STEP 1: SET UP TRADINGVIEW WEBHOOK ALERTS
# ============================================================================

# In TradingView, create an alert with the following JSON:
# 
# {{
#   "ticker": "{{ticker}}",
#   "signal": "BUY",  # or SELL, CLOSE, etc.
#   "price": {{close}},
#   "indicator": "Your_Indicator_Name",
#   "time": "{{time}}",
#   "comment": "Your indicator logic description"
# }}
#
# Webhook URL: http://your-server:8000/api/tradingview/webhook


# ============================================================================
# STEP 2: EXAMPLE TRADINGVIEW CUSTOM INDICATOR ALERT SETUP
# ============================================================================

TRADINGVIEW_WEBHOOK_TEMPLATE = """
// In TradingView Alert Action, set Webhook URL:
// http://your-ip:8000/api/tradingview/webhook

// Then use this JSON in the message:
{
  "ticker": "{{ticker}}",
  "signal": "{{strategy.order.action}}",
  "price": {{close}},
  "indicator": "RSI_MA_Cross",
  "time": "{{time}}",
  "comment": "RSI above 70 + price above MA. Current time: {{timenow}}"
}
"""


# ============================================================================
# STEP 3: PYTHON SCRIPT TO SEND CUSTOM INDICATOR ALERTS (LOCAL)
# ============================================================================

import requests
import json
from datetime import datetime

def send_tradingview_alert(
    ticker: str,
    signal: str,
    price: float,
    indicator: str,
    comment: str = "",
    webhook_url: str = "http://localhost:8000/api/tradingview/webhook"
):
    """
    Send a custom indicator alert to the Trading Desk Calendar API
    
    Args:
        ticker: Futures contract (ES, NQ, CL, etc.)
        signal: BUY, SELL, CLOSE, HOLD, etc.
        price: Current price
        indicator: Name of your custom indicator
        comment: Any additional context
        webhook_url: API endpoint (default local)
    """
    payload = {
        "ticker": ticker,
        "signal": signal,
        "price": price,
        "indicator": indicator,
        "time": datetime.now().isoformat(),
        "comment": comment
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        print(f"✅ Alert sent: {ticker} {signal} @ {price}")
        print(f"Response: {response.json()}")
        return response.json()
    except Exception as e:
        print(f"❌ Error sending alert: {e}")
        return None


# ============================================================================
# STEP 4: GET TRADING ANALYSIS FOR YOUR ALERT
# ============================================================================

def get_alert_context(ticker: str):
    """
    Get market context for your alert signal
    Helps you decide if the signal aligns with current market conditions
    """
    try:
        # Get daily analysis
        daily = requests.get("http://localhost:8000/api/daily").json()
        
        # Get specific asset analysis
        asset = requests.get(f"http://localhost:8000/api/asset/{ticker}").json()
        
        # Get quick summary
        summary = requests.get("http://localhost:8000/api/quick-summary").json()
        
        context = {
            "ticker": ticker,
            "market_open": daily["data"]["market_status"]["status"],
            "current_time": summary["summary"]["time"],
            "risk_level": daily["data"]["risk_level"]["level"],
            "recommendation": daily["data"]["trading_recommendation"],
            "asset_info": asset["data"],
            "seasonal_strength": requests.get("http://localhost:8000/api/monthly").json()["data"]["historical_strength"]
        }
        
        return context
    except Exception as e:
        print(f"Error fetching context: {e}")
        return None


# ============================================================================
# STEP 5: AUTOMATED INDICATOR + CALENDAR INTEGRATION
# ============================================================================

def analyze_signal_with_calendar(ticker: str, signal: str, price: float, indicator: str):
    """
    Combine your indicator signal with calendar context
    Returns confidence score and recommendation
    """
    context = get_alert_context(ticker)
    
    if not context:
        return {"confidence": 0, "recommendation": "Context unavailable"}
    
    # Analyze signal strength based on market conditions
    confidence = 50  # Base confidence
    
    # Market open = high volatility bonus
    if context["market_open"] == "open":
        confidence += 10
    
    # Risk level modifier
    if context["risk_level"] == "Low-Medium":
        confidence += 15
    elif "High" in context["risk_level"]:
        confidence -= 10
    
    # Calendar seasonality bonus
    if "Strong" in context["seasonal_strength"]:
        if signal == "BUY":
            confidence += 20
    elif "Weak" in context["seasonal_strength"]:
        if signal == "SELL":
            confidence += 20
    
    # Clamp confidence between 0-100
    confidence = max(0, min(100, confidence))
    
    return {
        "ticker": ticker,
        "signal": signal,
        "confidence": confidence,
        "market_condition": context["recommendation"],
        "risk_assessment": context["risk_level"],
        "recommendation": (
            "✅ HIGH CONFIDENCE" if confidence >= 75 else
            "⚠️ MEDIUM CONFIDENCE" if confidence >= 50 else
            "❌ LOW CONFIDENCE"
        ),
        "details": context
    }


# ============================================================================
# STEP 6: USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    
    # Example 1: Send a simple alert
    print("=" * 60)
    print("EXAMPLE 1: Send indicator alert to API")
    print("=" * 60)
    send_tradingview_alert(
        ticker="ES",
        signal="BUY",
        price=5234.50,
        indicator="RSI_MA_Crossover",
        comment="RSI crossed above 50 at US market open"
    )
    
    # Example 2: Get context for your signal
    print("\n" + "=" * 60)
    print("EXAMPLE 2: Get market context for alert")
    print("=" * 60)
    context = get_alert_context("ES")
    if context:
        print(f"Market: {context['market_open']}")
        print(f"Risk Level: {context['risk_level']}")
        print(f"Recommendation: {context['recommendation']}")
    
    # Example 3: Analyze signal with calendar
    print("\n" + "=" * 60)
    print("EXAMPLE 3: Analyze signal strength")
    print("=" * 60)
    analysis = analyze_signal_with_calendar(
        ticker="ES",
        signal="BUY",
        price=5234.50,
        indicator="Custom_RSI_MA"
    )
    print(json.dumps(analysis, indent=2))
    
    # Example 4: Get quick trading summary
    print("\n" + "=" * 60)
    print("EXAMPLE 4: Quick one-glance summary")
    print("=" * 60)
    try:
        summary = requests.get("http://localhost:8000/api/quick-summary").json()
        print(f"Time: {summary['summary']['time']}")
        print(f"Top Asset: {summary['summary']['top_asset']}")
        print(f"Quick Tip: {summary['summary']['quick_tip']}")
    except:
        print("API not running - start with: python api/app.py")
