import sys, os
sys.path.insert(0, os.path.abspath("."))
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
from crawler.daily_calendar import MASTER_CALENDAR_EVENTS, get_upcoming_ranked_events

print(f"Total master events: {len(MASTER_CALENDAR_EVENTS)}")
categories = set()
for e in MASTER_CALENDAR_EVENTS:
    categories.add(e.get("category", "General"))
print("Categories:", sorted(list(categories)))

upcoming = get_upcoming_ranked_events(days_ahead=365)
lates = [e for e in upcoming if e.get('is_late')]
print(f"Total late events: {len(lates)}")
from crawler.seasonal_trends import get_current_seasonal_intel
intel = get_current_seasonal_intel()
print(f"Current Seasonal Month: {intel['current_month_name']} - Target: {intel['upload_now_target']}")
for n in intel['priority_niches']:
    print(f"- {n['theme']} | Window: {n['upload_date_range']} | Due: {n['upload_deadline']} | {n['timing_badge']}")
