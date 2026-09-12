import re
from calendar import monthrange
from datetime import datetime, timedelta

PARTICIPANTS = ["Rahul", "Priya", "Aman", "Neha", "Arjun", "Simran", "Karan", "Riya"]

DECISION_KEYWORDS = [
    "decide", "decided", "decision", "finalize", "finalized", "final", 
    "fixed", "locked", "confirmed", "confirm", "settle", "settled", 
    "agree", "agreed", "choose", "chosen", "book", "booked", "pakka", "done"
]

MONTHS = {
    "january": 1, "february": 2, "march": 3, "april": 4,
    "may": 5, "june": 6, "july": 7, "august": 8,
    "september": 9, "october": 10, "november": 11, "december": 12,
}


def _month_range(year: int, month: int):
    last_day = monthrange(year, month)[1]
    return {
        "start": datetime(year, month, 1).isoformat(),
        "end": datetime(year, month, last_day, 23, 59, 59).isoformat(),
    }


def parse_query(query: str, ref_date: datetime = None):
    if ref_date is None:
        ref_date = datetime(2026, 9, 1)
        
    q_lower = query.lower()
    
    # 1. Person extraction
    person = None
    for p in PARTICIPANTS:
        pattern = r'\b' + re.escape(p.lower()) + r'\b'
        if re.search(pattern, q_lower):
            person = p
            break
            
    # 2. Time range extraction
    time_range = None
    if "today" in q_lower:
        start = ref_date.replace(hour=0, minute=0, second=0)
        end = ref_date.replace(hour=23, minute=59, second=59)
        time_range = {"start": start.isoformat(), "end": end.isoformat()}
    elif "yesterday" in q_lower:
        start = (ref_date - timedelta(days=1)).replace(hour=0, minute=0, second=0)
        end = (ref_date - timedelta(days=1)).replace(hour=23, minute=59, second=59)
        time_range = {"start": start.isoformat(), "end": end.isoformat()}
    elif "last week" in q_lower:
        end = ref_date.replace(hour=23, minute=59, second=59, microsecond=0)
        start = (ref_date - timedelta(days=7)).replace(hour=0, minute=0, second=0, microsecond=0)
        time_range = {"start": start.isoformat(), "end": end.isoformat()}
    elif "this month" in q_lower:
        time_range = _month_range(ref_date.year, ref_date.month)
    elif "last month" in q_lower:
        year = ref_date.year if ref_date.month > 1 else ref_date.year - 1
        month = ref_date.month - 1 or 12
        time_range = _month_range(year, month)
    else:
        month_match = re.search(r"\b(" + "|".join(MONTHS) + r")\b(?:\s+(\d{1,2}))?(?:\s*,?\s*(\d{4}))?", q_lower)
        if month_match:
            month = MONTHS[month_match.group(1)]
            day = month_match.group(2)
            year = int(month_match.group(3) or ref_date.year)
            if day:
                day_number = int(day)
                if day_number <= monthrange(year, month)[1]:
                    start = datetime(year, month, day_number)
                    end = start.replace(hour=23, minute=59, second=59)
                    time_range = {"start": start.isoformat(), "end": end.isoformat()}
            else:
                time_range = _month_range(year, month)

    # 3. Intent Detection
    is_decision = any(kw in q_lower for kw in DECISION_KEYWORDS)
    
    if is_decision:
        intent = "decision"
    elif person is not None:
        intent = "person"
    elif time_range is not None:
        intent = "time"
    else:
        intent = "semantic"
        
    return {
        "intent": intent,
        "person": person,
        "time_range": time_range,
        "semantic_query": query.strip()
    }
