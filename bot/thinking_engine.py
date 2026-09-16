"""
AI Thinking Engine for Day Trading Calendar
Analyzes market data and generates intelligent trading breakdowns
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any
import requests

class TradingThinkingBot:
    """Main AI analysis engine for trading insights"""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        self.holidays = self.load_json("holidays.json")
        self.sessions = self.load_json("market_sessions.json")
        self.current_date = datetime.now()
        
    def load_json(self, filename: str) -> Dict:
        """Load JSON data files"""
        filepath = os.path.join(self.data_dir, filename)
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: {filename} not found")
            return {}
    
    def get_daily_breakdown(self) -> Dict[str, Any]:
        """Generate today's trading breakdown"""
        today = self.current_date.strftime("%Y-%m-%d")
        
        analysis = {
            "date": today,
            "day_of_week": self.current_date.strftime("%A"),
            "market_status": self._check_market_status(today),
            "economic_events": self._get_todays_events(),
            "best_assets": self._rank_assets_for_today(),
            "session_summary": self._get_session_summary(),
            "trading_recommendation": self._generate_recommendation("daily"),
            "risk_level": self._assess_daily_risk()
        }
        
        return analysis
    
    def get_monthly_breakdown(self) -> Dict[str, Any]:
        """Generate this month's trading patterns"""
        current_month = self.current_date.strftime("%B")
        current_year = self.current_date.year
        
        analysis = {
            "month": current_month,
            "year": current_year,
            "historical_strength": self._get_month_seasonality(current_month),
            "upcoming_events": self._get_monthly_events(),
            "best_trading_days": self._identify_best_days_in_month(),
            "volume_patterns": self._get_volume_patterns(current_month),
            "recommended_focus": self._get_monthly_focus(current_month),
            "monthly_recommendation": self._generate_recommendation("monthly")
        }
        
        return analysis
    
    def get_yearly_breakdown(self) -> Dict[str, Any]:
        """Generate year's trading patterns and opportunities"""
        current_year = self.current_date.year
        
        analysis = {
            "year": current_year,
            "q_performance": self._get_quarterly_performance(),
            "seasonal_patterns": self._get_seasonal_patterns(),
            "major_events_calendar": self._get_yearly_events(),
            "best_quarters": self._rank_quarters(),
            "volatility_forecast": self._get_volatility_forecast(),
            "yearly_recommendation": self._generate_recommendation("yearly")
        }
        
        return analysis
    
    def _check_market_status(self, date_str: str) -> Dict:
        """Check if markets are open/closed"""
        holidays = self.holidays.get("us_market_holidays_2026", [])
        
        for holiday in holidays:
            if holiday["date"] == date_str:
                return {
                    "status": holiday["market_status"],
                    "name": holiday["name"],
                    "impact": holiday["impact"],
                    "notes": holiday["notes"]
                }
        
        return {
            "status": "open",
            "name": "Regular Trading Day",
            "impact": "normal"
        }
    
    def _get_todays_events(self) -> List[Dict]:
        """Get economic events scheduled for today"""
        today = self.current_date.strftime("%Y-%m-%d")
        
        # Check FOMC meetings
        fomc_dates = self.holidays.get("fomc_meeting_dates_2026", [])
        events = []
        
        for fomc in fomc_dates:
            if fomc.get("announcement") == today:
                events.append({
                    "time": fomc["time"],
                    "event": "FOMC Rate Decision",
                    "impact": fomc["impact"],
                    "importance": "CRITICAL"
                })
        
        # Add placeholder for other economic data
        events.append({
            "note": "Check economic calendar for EIA, Jobs, Inflation data"
        })
        
        return events
    
    def _rank_assets_for_today(self) -> List[Dict]:
        """Rank best trading assets for today"""
        ranking = []
        
        day_of_week = self.current_date.strftime("%A")
        
        # Monday preferences
        if day_of_week == "Monday":
            ranking = [
                {"asset": "ES (S&P 500)", "reason": "Week start volatility", "score": 9.5},
                {"asset": "NQ (NASDAQ)", "reason": "Tech sector moves", "score": 9.3},
                {"asset": "CL (Crude Oil)", "reason": "Weekly trend setup", "score": 8.5}
            ]
        
        # Mid-week
        elif day_of_week in ["Tuesday", "Wednesday", "Thursday"]:
            ranking = [
                {"asset": "ES (S&P 500)", "reason": "Consistent liquidity", "score": 9.0},
                {"asset": "NQ (NASDAQ)", "reason": "Mid-week momentum", "score": 8.8},
                {"asset": "DX (Dollar Index)", "reason": "Data sensitivity", "score": 8.5}
            ]
        
        # Friday
        else:
            ranking = [
                {"asset": "ES (S&P 500)", "reason": "Week close positioning", "score": 8.8},
                {"asset": "NQ (NASDAQ)", "reason": "Tech rebalancing", "score": 8.5},
                {"asset": "GC (Gold)", "reason": "Weekend risk-off", "score": 8.3}
            ]
        
        return ranking
    
    def _get_session_summary(self) -> Dict:
        """Get current market session information"""
        hour = self.current_date.hour
        
        sessions_info = {
            "current_time": self.current_date.strftime("%H:%M ET"),
            "active_sessions": [],
            "next_session": ""
        }
        
        # Determine active session
        if 2 <= hour < 9:
            sessions_info["active_sessions"].append("London Session (2:00-9:00 ET)")
        if 9 <= hour < 16:
            sessions_info["active_sessions"].append("US Session (9:30-16:00 ET)")
        if 17 <= hour or hour < 2:
            sessions_info["active_sessions"].append("Evening/Asian Session")
        
        return sessions_info
    
    def _get_todays_best_times(self) -> List[str]:
        """Get optimal trading times for today"""
        hour = self.current_date.hour
        
        best_times = [
            "08:00-09:30 ET: London-US Overlap (HIGH LIQUIDITY)",
            "09:30-11:00 ET: US Market Open (HIGH VOLATILITY)",
            "14:30-16:00 ET: US Close (PROFIT TAKING)",
            "02:00-03:00 ET: London Open (TRENDING)"
        ]
        
        return best_times
    
    def _get_month_seasonality(self, month: str) -> Dict:
        """Get historical seasonal patterns for the month"""
        seasonality = {
            "January": {"strength": "Very Strong", "avg_return": "+1.5%", "volatility": "High", "notes": "January Effect, new positioning"},
            "February": {"strength": "Weak", "avg_return": "-0.3%", "volatility": "Medium", "notes": "Post-holiday pullback"},
            "March": {"strength": "Strong", "avg_return": "+0.8%", "volatility": "High", "notes": "Q1 end earnings"},
            "April": {"strength": "Very Strong", "avg_return": "+1.2%", "volatility": "Medium", "notes": "Spring rally begins"},
            "May": {"strength": "Weak", "avg_return": "-0.5%", "volatility": "Low", "notes": "'Sell in May' syndrome"},
            "June": {"strength": "Weak", "avg_return": "-0.2%", "volatility": "Medium", "notes": "Mid-year doldrums"},
            "July": {"strength": "Medium", "avg_return": "+0.4%", "volatility": "Low", "notes": "Summer vacation volume"},
            "August": {"strength": "Weak", "avg_return": "-0.1%", "volatility": "Medium", "notes": "Late summer weakness"},
            "September": {"strength": "Weakest", "avg_return": "-1.0%", "volatility": "Very High", "notes": "Historically weakest month"},
            "October": {"strength": "Strong", "avg_return": "+1.0%", "volatility": "Very High", "notes": "Crash histories, but strong mean revert"},
            "November": {"strength": "Very Strong", "avg_return": "+1.8%", "volatility": "Medium", "notes": "Thanksgiving rally"},
            "December": {"strength": "Very Strong", "avg_return": "+1.5%", "volatility": "Medium", "notes": "Year-end rally (except tax-loss Jan)"}
        }
        
        return seasonality.get(month, {"strength": "Unknown", "volatility": "Medium"})
    
    def _get_volume_patterns(self, month: str) -> Dict:
        """Get historical volume patterns"""
        return {
            "month": month,
            "pattern": "Increased volume expected post-Labor Day through year-end",
            "best_volume_days": "Tuesdays and Wednesdays typically",
            "low_volume_risk": "Avoid trading during low-volume periods (avoid last hour of Friday)"
        }
    
    def _get_monthly_focus(self, month: str) -> List[str]:
        """Get recommended trading focus for the month"""
        focus_areas = {
            "September": ["Risk management", "Reduce position size", "Focus on liquid assets only", "Watch for capitulation"],
            "October": ["Volatility opportunities", "Rebalance portfolios", "Watch for panic selling", "Mean reversion plays"],
            "November": ["Trend following", "Thanksgiving rally", "Momentum plays", "Year-end positioning"],
            "December": ["Year-end flows", "Tax-loss harvesting setup", "Thin volume risk", "Santa Claus rally"]
        }
        
        return focus_areas.get(month, ["Follow seasonal patterns", "Track economic data", "Manage risk"])
    
    def _get_quarterly_performance(self) -> Dict:
        """Get quarterly performance patterns"""
        return {
            "Q1": {"strength": "Very Strong", "avg_return": "+3.2%", "best_assets": ["ES", "NQ"], "notes": "Strong start to year"},
            "Q2": {"strength": "Weak", "avg_return": "-0.5%", "best_assets": ["DX", "GC"], "notes": "May-June weakness"},
            "Q3": {"strength": "Weakest", "avg_return": "-1.8%", "best_assets": ["GC", "VIX"], "notes": "September crashes, summer doldrums"},
            "Q4": {"strength": "Very Strong", "avg_return": "+3.5%", "best_assets": ["ES", "NQ"], "notes": "Best quarter of year, tax-loss selling, rally"}
        }
    
    def _get_yearly_events(self) -> List[Dict]:
        """Get major yearly events affecting trading"""
        events = [
            {"date": "January", "event": "FOMC", "impact": "High", "asset_impact": ["ES", "DX"]},
            {"date": "March", "event": "FOMC", "impact": "High", "asset_impact": ["ES", "DX"]},
            {"date": "May", "event": "FOMC", "impact": "High", "asset_impact": ["ES", "DX"]},
            {"date": "June", "event": "FOMC", "impact": "High", "asset_impact": ["ES", "DX"]},
            {"date": "July", "event": "FOMC", "impact": "High", "asset_impact": ["ES", "DX"]},
            {"date": "September", "event": "FOMC + Crash Cycle", "impact": "Critical", "asset_impact": ["VIX", "GC", "ES"]},
            {"date": "November", "event": "FOMC + Thanksgiving", "impact": "High", "asset_impact": ["ES", "NQ"]},
            {"date": "December", "event": "FOMC + Year-End", "impact": "High", "asset_impact": ["ES", "NQ"]}
        ]
        return events
    
    def _rank_quarters(self) -> List[Dict]:
        """Rank quarters by historical strength"""
        return [
            {"quarter": "Q4", "rank": 1, "strength": "Very Strong", "return": "+3.5%"},
            {"quarter": "Q1", "rank": 2, "strength": "Very Strong", "return": "+3.2%"},
            {"quarter": "Q2", "rank": 3, "strength": "Weak", "return": "-0.5%"},
            {"quarter": "Q3", "rank": 4, "strength": "Weakest", "return": "-1.8%"}
        ]
    
    def _get_volatility_forecast(self) -> Dict:
        """Forecast expected volatility patterns"""
        return {
            "overall_trend": "Increased volatility expected Q4 2026",
            "seasonal": "September already passed (historically weakest), October historically volatile",
            "fomc_impact": "Every FOMC meeting causes 1-3% moves",
            "recommendations": "Position sizing should account for seasonal volatility"
        }
    
    def _get_monthly_events(self) -> List[Dict]:
        """Get events scheduled this month"""
        current_month = self.current_date.month
        current_year = self.current_date.year
        
        fomc_dates = self.holidays.get("fomc_meeting_dates_2026", [])
        events = []
        
        for fomc in fomc_dates:
            fomc_month = int(fomc["announcement"].split("-")[1])
            if fomc_month == current_month:
                events.append({
                    "date": fomc["announcement"],
                    "event": "FOMC Rate Decision",
                    "impact": fomc["impact"]
                })
        
        return events
    
    def _identify_best_days_in_month(self) -> List[str]:
        """Identify historically best trading days in current month"""
        return [
            "Tuesdays and Wednesdays (highest volume historically)",
            "First week after market opens",
            "Mid-month (around 10th-15th)",
            "Avoid last 2 trading days of month (reduced volume)"
        ]
    
    def _assess_daily_risk(self) -> Dict:
        """Assess daily risk factors"""
        day_of_week = self.current_date.strftime("%A")
        
        risk_levels = {
            "Monday": {"level": "Medium-High", "reason": "Week start volatility, gap risk"},
            "Tuesday": {"level": "Low-Medium", "reason": "Steady trading, good liquidity"},
            "Wednesday": {"level": "Low-Medium", "reason": "Mid-week stability"},
            "Thursday": {"level": "Medium", "reason": "Before-weekend positioning"},
            "Friday": {"level": "Medium", "reason": "Holiday weekend gap risk"}
        }
        
        return risk_levels.get(day_of_week, {"level": "Medium", "reason": "Regular day"})
    
    def _generate_recommendation(self, timeframe: str) -> str:
        """Generate AI-powered trading recommendation"""
        recommendations = {
            "daily": self._daily_recommendation(),
            "monthly": self._monthly_recommendation(),
            "yearly": self._yearly_recommendation()
        }
        
        return recommendations.get(timeframe, "Review market conditions")
    
    def _daily_recommendation(self) -> str:
        """Daily AI recommendation"""
        hour = self.current_date.hour
        day = self.current_date.strftime("%A")
        
        if 8 <= hour <= 9:
            return "🔥 LONDON-US OVERLAP: Prime trading window. High liquidity expected. Focus on liquid majors (ES, NQ, CL)."
        elif 9 <= hour <= 12:
            return "📈 US SESSION: Market open energy. Watch for economic data reactions. Tight stops recommended."
        elif 12 <= hour <= 15:
            return "⚖️ MID-SESSION: Consolidation likely. Look for mean-reversion setups."
        else:
            return "🌙 OFF-HOURS: Reduced liquidity. Only trade major news events. Wider spreads expected."
    
    def _monthly_recommendation(self) -> str:
        """Monthly AI recommendation"""
        month = self.current_date.strftime("%B")
        
        monthly_recs = {
            "September": "⚠️ HISTORICALLY WEAKEST MONTH: Reduce position size 30-50%. Focus on downside protection. Avoid new long entries.",
            "October": "⚡ VOLATILE BUT RECOVERS: Great mean-reversion opportunities. Expect 3-5% swings. Capitalize on panic selling.",
            "November": "📊 THANKSGIVING RALLY INCOMING: Bullish bias. Follow the trend. Build long positions. Momentum plays work.",
            "December": "🎄 YEAR-END STRENGTH: Strong returns expected. Watch for thin liquidity last week. Tax-loss harvesting opportunities."
        }
        
        return monthly_recs.get(month, f"{month} trading: Follow seasonal patterns and manage risk accordingly.")
    
    def _yearly_recommendation(self) -> str:
        """Yearly AI recommendation"""
        current_quarter = (self.current_date.month - 1) // 3 + 1
        
        if current_quarter == 4:
            return "🎯 Q4 STRATEGY: Best quarter historically. Bullish positioning recommended. Focus on ES, NQ. Target year-end rally."
        elif current_quarter == 1:
            return "🎯 Q1 STRATEGY: Strong quarter. Ride the January effect. Maintain bullish bias. Growth names outperform."
        elif current_quarter == 2:
            return "🎯 Q2 STRATEGY: Weak quarter. Reduce exposure. Consider defensive plays. Watch for May weakness."
        else:
            return "🎯 Q3 STRATEGY: Weakest quarter. High risk/reward. Defensive positioning. Watch for September crash signals."
    
    def print_daily_report(self):
        """Print formatted daily report"""
        report = self.get_daily_breakdown()
        print("\n" + "="*60)
        print(f"TRADING DESK - DAILY BREAKDOWN")
        print(f"Date: {report['date']} ({report['day_of_week']})")
        print("="*60)
        print(f"\n📊 Market Status: {report['market_status'].get('status').upper()}")
        print(f"💬 {report['market_status'].get('name')}")
        
        print(f"\n🎯 TOP ASSETS TODAY:")
        for i, asset in enumerate(report['best_assets'], 1):
            print(f"   {i}. {asset['asset']} - {asset['reason']} (Score: {asset['score']})")
        
        print(f"\n⏰ BEST TRADING TIMES:")
        for time_window in self._get_todays_best_times():
            print(f"   • {time_window}")
        
        print(f"\n⚠️ DAILY RISK: {report['risk_level']['level']}")
        print(f"   Reason: {report['risk_level']['reason']}")
        
        print(f"\n💡 RECOMMENDATION:")
        print(f"   {report['trading_recommendation']}")
        print("\n" + "="*60)
    
    def print_monthly_report(self):
        """Print formatted monthly report"""
        report = self.get_monthly_breakdown()
        print("\n" + "="*60)
        print(f"TRADING DESK - MONTHLY BREAKDOWN")
        print(f"Month: {report['month']} {report['year']}")
        print("="*60)
        
        seasonality = report['historical_strength']
        print(f"\n📈 Seasonal Strength: {seasonality['strength']}")
        print(f"   Avg Return: {seasonality['avg_return']}")
        print(f"   Volatility: {seasonality['volatility']}")
        print(f"   Notes: {seasonality['notes']}")
        
        print(f"\n🎯 RECOMMENDED FOCUS:")
        for focus in report['recommended_focus']:
            print(f"   • {focus}")
        
        print(f"\n🏆 BEST TRADING DAYS:")
        for day in report['best_trading_days']:
            print(f"   • {day}")
        
        print(f"\n💡 MONTHLY RECOMMENDATION:")
        print(f"   {report['monthly_recommendation']}")
        print("\n" + "="*60)
    
    def print_yearly_report(self):
        """Print formatted yearly report"""
        report = self.get_yearly_breakdown()
        print("\n" + "="*60)
        print(f"TRADING DESK - YEARLY BREAKDOWN")
        print(f"Year: {report['year']}")
        print("="*60)
        
        print(f"\n📊 QUARTERLY RANKINGS:")
        for q in report['best_quarters']:
            print(f"   #{q['rank']}: {q['quarter']} - {q['strength']} ({q['return']})")
        
        print(f"\n🎪 MAJOR EVENTS:")
        for event in report['major_events_calendar'][:5]:  # Show first 5
            print(f"   • {event['date']}: {event['event']} (Impact: {event['impact']})")
        
        print(f"\n💡 YEARLY RECOMMENDATION:")
        print(f"   {report['yearly_recommendation']}")
        print("\n" + "="*60)


if __name__ == "__main__":
    # Initialize bot
    bot = TradingThinkingBot()
    
    # Generate and print all reports
    bot.print_daily_report()
    bot.print_monthly_report()
    bot.print_yearly_report()
