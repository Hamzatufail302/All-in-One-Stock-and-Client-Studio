import urllib.request
import json
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

base = "http://127.0.0.1:8000"

def test(url):
    try:
        req = urllib.request.Request(base + url)
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            print(f"PASS: {url} (keys: {list(data.keys()) if isinstance(data, dict) else len(data)})")
            return data
    except Exception as e:
        print(f"FAIL: {url} -> {e}")
        return None

print("Testing backend endpoints:")
test("/api/trends/overview")
cal = test("/api/daily-events?days=180")
if cal and "events" in cal:
    events = cal["events"]
    print(f"Total events returned: {len(events)}")
    late = [e for e in events if e.get("is_late")]
    fashion = [e for e in events if "fashion" in e.get("category", "").lower()]
    birthday = [e for e in events if "birthday" in e.get("category", "").lower()]
    print(f"Late events ({len(late)}): {[e['name'] for e in late]}")
    print(f"Fashion events ({len(fashion)}): {[e['name'] for e in fashion]}")
    print(f"Birthday events ({len(birthday)}): {[e['name'] for e in birthday]}")
    for e in late[:2]:
        print(f"Sample Late Event: {e['name']} | Upload Window: {e.get('upload_date_range')} | Deadline: {e.get('golden_upload_deadline')} | Badge: {e.get('timing_badge')}")

search = test("/api/search?q=halloween%20vector")
if search and "results" in search:
    res = search["results"][0]
    print(f"Sample Search Result: kw={res.get('keyword')} | deadline={res.get('upload_deadline')} | range={res.get('upload_date_range')} | is_late={res.get('is_late')} | badge={res.get('timing_badge')}")

quota = test("/api/ai-daily-quota?count=20")
if quota and "prompts" in quota:
    p = quota["prompts"][0]
    print(f"Sample Quota Prompt: title={p.get('title')} | deadline={p.get('upload_deadline')} | range={p.get('upload_date_range')} | is_late={p.get('is_late')}")

android = test("/api/android/studio")
if android and "trending_apps" in android:
    print(f"Android Apps count: {len(android['trending_apps'])}")
