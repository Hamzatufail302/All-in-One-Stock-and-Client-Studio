import sqlite3
import os
from datetime import datetime, timedelta

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data")
DB_PATH = os.path.join(DB_DIR, "stock_crawler.db")

def get_connection():
    os.makedirs(DB_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # Table for saved keywords & production queue
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS saved_items (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        keyword TEXT NOT NULL,
        platform TEXT DEFAULT 'Multi',
        asset_type TEXT DEFAULT 'All',
        demand_score REAL DEFAULT 0,
        competition TEXT DEFAULT 'Medium',
        tags TEXT DEFAULT '',
        title_suggestion TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        status TEXT DEFAULT 'Idea',
        created_at TEXT NOT NULL
    );
    """)

    # Table for search history
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS search_history (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        query TEXT NOT NULL,
        platform TEXT DEFAULT 'All',
        results_count INTEGER DEFAULT 0,
        searched_at TEXT NOT NULL
    );
    """)

    # Table for daily targets & goals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT UNIQUE NOT NULL,
        target_vectors INTEGER DEFAULT 5,
        target_images INTEGER DEFAULT 10,
        target_videos INTEGER DEFAULT 5,
        target_templates INTEGER DEFAULT 3,
        notes TEXT DEFAULT '',
        updated_at TEXT NOT NULL
    );
    """)

    # Table for logged/completed assets per day
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS daily_completed_assets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT NOT NULL,
        title TEXT NOT NULL,
        asset_type TEXT NOT NULL,
        platform TEXT NOT NULL,
        prompt_or_tags TEXT DEFAULT '',
        status TEXT DEFAULT 'Created',
        created_at TEXT NOT NULL
    );
    """)

    # Table for video editing outreach leads & CRM
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS outreach_leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_name TEXT NOT NULL,
        channel_or_website TEXT DEFAULT '',
        client_niche TEXT DEFAULT 'YouTube',
        outreach_channel TEXT DEFAULT 'Email',
        pitch_content TEXT DEFAULT '',
        status TEXT DEFAULT 'Targeted',
        followup_date TEXT DEFAULT '',
        notes TEXT DEFAULT '',
        created_at TEXT NOT NULL
    );
    """)

    conn.commit()
    conn.close()

def save_keyword(item: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO saved_items (keyword, platform, asset_type, demand_score, competition, tags, title_suggestion, notes, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item.get("keyword", ""),
        item.get("platform", "Multi"),
        item.get("asset_type", "All"),
        item.get("demand_score", 0),
        item.get("competition", "Medium"),
        item.get("tags", ""),
        item.get("title_suggestion", ""),
        item.get("notes", ""),
        item.get("status", "Idea"),
        now
    ))
    item_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return item_id

def get_saved_items(status=None, platform=None) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM saved_items WHERE 1=1"
    params = []
    if status and status != 'All':
        query += " AND status = ?"
        params.append(status)
    if platform and platform != 'All':
        query += " AND platform = ?"
        params.append(platform)
    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def update_saved_item(item_id: int, updates: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    params = []
    for k, v in updates.items():
        if k in ['keyword', 'platform', 'asset_type', 'demand_score', 'competition', 'tags', 'title_suggestion', 'notes', 'status']:
            fields.append(f"{k} = ?")
            params.append(v)
    if not fields:
        conn.close()
        return False
    params.append(item_id)
    sql = f"UPDATE saved_items SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(sql, params)
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_saved_item(item_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM saved_items WHERE id = ?", (item_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def add_search_history(query: str, platform: str, results_count: int):
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO search_history (query, platform, results_count, searched_at)
        VALUES (?, ?, ?, ?)
    """, (query, platform, results_count, now))
    conn.commit()
    conn.close()

def get_search_history(limit: int = 20) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM search_history ORDER BY id DESC LIMIT ?", (limit,))
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def clear_search_history():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM search_history")
    conn.commit()
    conn.close()

# --- DAILY GOAL & PROGRESS TRACKING HELPERS ---

def get_or_create_daily_goal(date_str: str = None) -> dict:
    if not date_str or not date_str.strip():
        date_str = datetime.now().strftime("%Y-%m-%d")
    else:
        date_str = date_str.strip()
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM daily_goals WHERE date = ?", (date_str,))
    row = cursor.fetchone()
    if not row:
        now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("""
            INSERT INTO daily_goals (date, target_vectors, target_images, target_videos, target_templates, notes, updated_at)
            VALUES (?, 5, 10, 5, 3, '', ?)
        """, (date_str, now_str))
        conn.commit()
        cursor.execute("SELECT * FROM daily_goals WHERE date = ?", (date_str,))
        row = cursor.fetchone()
    goal = dict(row)
    
    # Calculate completed counts for this date
    cursor.execute("""
        SELECT asset_type, status, COUNT(*) as count 
        FROM daily_completed_assets 
        WHERE date = ? 
        GROUP BY asset_type, status
    """, (date_str,))
    counts = cursor.fetchall()
    
    comp_map = {
        'vectors': 0,
        'images': 0,
        'videos': 0,
        'templates': 0,
        'total_created': 0,
        'total_uploaded': 0
    }
    for c in counts:
        atype = (c['asset_type'] or '').lower()
        cnt = c['count']
        if any(w in atype for w in ['vector', 'illustrator', 'svg', 'icon']):
            comp_map['vectors'] += cnt
        elif any(w in atype for w in ['video', 'footage', 'motion', 'lottie']):
            comp_map['videos'] += cnt
        elif any(w in atype for w in ['template', 'canva', 'mockup', 'psd', 'photoshop', 'print', 'brochure', 'flyer']):
            comp_map['templates'] += cnt
        elif any(w in atype for w in ['image', 'photo', 'ai', 'render', '3d']):
            comp_map['images'] += cnt
        else:
            comp_map['images'] += cnt
            
        if c['status'] == 'Uploaded':
            comp_map['total_uploaded'] += cnt
        comp_map['total_created'] += cnt

    goal['completed_vectors'] = comp_map['vectors']
    goal['completed_images'] = comp_map['images']
    goal['completed_videos'] = comp_map['videos']
    goal['completed_templates'] = comp_map['templates']
    goal['total_created'] = comp_map['total_created']
    goal['total_uploaded'] = comp_map['total_uploaded']
    
    tgt_vec = int(goal.get('target_vectors') or 0)
    tgt_img = int(goal.get('target_images') or 0)
    tgt_vid = int(goal.get('target_videos') or 0)
    tgt_tmp = int(goal.get('target_templates') or 0)
    total_target = tgt_vec + tgt_img + tgt_vid + tgt_tmp
    goal['total_target'] = total_target
    goal['percentage'] = min(round((comp_map['total_created'] / total_target * 100), 1) if total_target > 0 else 0, 100.0)

    # Fetch individual completed assets for this day
    cursor.execute("SELECT * FROM daily_completed_assets WHERE date = ? ORDER BY id DESC", (date_str,))
    goal['assets'] = [dict(r) for r in cursor.fetchall()]

    conn.close()
    return goal

def update_daily_goal_targets(date_str: str, targets: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    now_str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    fields = ["updated_at = ?"]
    params = [now_str]
    for k in ['target_vectors', 'target_images', 'target_videos', 'target_templates', 'notes']:
        if k in targets and targets[k] is not None:
            fields.append(f"{k} = ?")
            params.append(targets[k])
    params.append(date_str)
    cursor.execute(f"UPDATE daily_goals SET {', '.join(fields)} WHERE date = ?", params)
    conn.commit()
    conn.close()
    return True

def log_daily_asset(asset: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    date_str = asset.get('date') or now.strftime("%Y-%m-%d")
    now_str = now.strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO daily_completed_assets (date, title, asset_type, platform, prompt_or_tags, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        date_str,
        asset.get('title', 'Untitled Asset'),
        asset.get('asset_type', 'AI Image'),
        asset.get('platform', 'Adobe Stock'),
        asset.get('prompt_or_tags', ''),
        asset.get('status', 'Created'),
        now_str
    ))
    asset_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return asset_id

def update_logged_asset(asset_id: int, updates: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    params = []
    for k in ['title', 'asset_type', 'platform', 'prompt_or_tags', 'status']:
        if k in updates and updates[k] is not None:
            fields.append(f"{k} = ?")
            params.append(updates[k])
    if not fields:
        conn.close()
        return False
    params.append(asset_id)
    cursor.execute(f"UPDATE daily_completed_assets SET {', '.join(fields)} WHERE id = ?", params)
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_logged_asset(asset_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM daily_completed_assets WHERE id = ?", (asset_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def get_progress_streak_and_history(days: int = 14) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now()
    history = []
    current_streak = 0
    streak_active = True

    for i in range(days):
        day_date = (now - timedelta(days=i)).strftime("%Y-%m-%d")
        cursor.execute("SELECT COUNT(*) as cnt FROM daily_completed_assets WHERE date = ?", (day_date,))
        cnt = cursor.fetchone()['cnt']
        
        cursor.execute("SELECT target_vectors + target_images + target_videos + target_templates as tgt FROM daily_goals WHERE date = ?", (day_date,))
        row_g = cursor.fetchone()
        tgt = (row_g['tgt'] if (row_g and row_g['tgt'] is not None) else 23) or 23
        
        if cnt > 0 and streak_active:
            current_streak += 1
        elif i > 0 and cnt == 0:
            streak_active = False

        history.append({
            "date": day_date,
            "completed": cnt,
            "target": tgt,
            "percentage": min(round((cnt / tgt * 100), 1) if tgt > 0 else 0, 100.0)
        })

    conn.close()
    return {
        "streak_days": current_streak,
        "history": history
    }

# --- VIDEO CLIENT OUTREACH LEADS ---

def save_outreach_lead(item: dict) -> int:
    conn = get_connection()
    cursor = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO outreach_leads (client_name, channel_or_website, client_niche, outreach_channel, pitch_content, status, followup_date, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        item.get("client_name", ""),
        item.get("channel_or_website", ""),
        item.get("client_niche", "YouTube"),
        item.get("outreach_channel", "Email"),
        item.get("pitch_content", ""),
        item.get("status", "Targeted"),
        item.get("followup_date", ""),
        item.get("notes", ""),
        now
    ))
    lead_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return lead_id

def get_outreach_leads(status=None) -> list:
    conn = get_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM outreach_leads WHERE 1=1"
    params = []
    if status and status != 'All':
        query += " AND status = ?"
        params.append(status)
    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = [dict(row) for row in cursor.fetchall()]
    conn.close()
    return rows

def update_outreach_lead(lead_id: int, updates: dict) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    fields = []
    values = []
    for k, v in updates.items():
        if k in ("client_name", "channel_or_website", "client_niche", "outreach_channel", "pitch_content", "status", "followup_date", "notes"):
            fields.append(f"{k} = ?")
            values.append(v)
    if not fields:
        conn.close()
        return False
    values.append(lead_id)
    query = f"UPDATE outreach_leads SET {', '.join(fields)} WHERE id = ?"
    cursor.execute(query, values)
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

def delete_outreach_lead(lead_id: int) -> bool:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM outreach_leads WHERE id = ?", (lead_id,))
    affected = cursor.rowcount
    conn.commit()
    conn.close()
    return affected > 0

