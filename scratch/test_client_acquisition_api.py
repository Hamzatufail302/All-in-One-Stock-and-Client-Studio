import json
from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

def test_api():
    print("Testing GET /api/client-acquisition/overview...")
    res = client.get("/api/client-acquisition/overview")
    assert res.status_code == 200, f"Expected 200, got {res.status_code}"
    data = res.json()
    assert "current_requirements" in data
    assert "prospecting_playbooks" in data
    assert "cold_email_templates" in data
    assert "objection_handling" in data
    assert "retainer_presets" in data
    print(f" Overview passed: {len(data['current_requirements'])} requirements, {len(data['prospecting_playbooks'])} playbooks.")

    print("\nTesting POST /api/client-acquisition/generate-pitch...")
    pitch_res = client.post("/api/client-acquisition/generate-pitch", json={
        "client_name": "Ali Abdaal",
        "channel_or_niche": "Productivity & Tech",
        "pitch_type": "youtube_sample",
        "custom_link": "https://drive.google.com/sample"
    })
    assert pitch_res.status_code == 200
    pitch_data = pitch_res.json()
    assert "subject" in pitch_data and "body" in pitch_data
    print(" Pitch generation passed:", pitch_data["subject"])

    print("\nTesting POST /api/client-acquisition/leads...")
    lead_res = client.post("/api/client-acquisition/leads", json={
        "client_name": "Test Creator Ali",
        "channel_or_website": "https://youtube.com/@ali",
        "client_niche": "Productivity",
        "outreach_channel": "Email",
        "pitch_content": "Hey Ali, re-edited your latest video hook...",
        "status": "Targeted",
        "followup_date": "2026-10-10",
        "notes": "Fast-paced editing sample sent"
    })
    assert lead_res.status_code == 200
    lead_info = lead_res.json()
    lead_id = lead_info["lead_id"]
    print(f" Lead created with ID {lead_id}")

    print("\nTesting GET /api/client-acquisition/leads...")
    list_res = client.get("/api/client-acquisition/leads")
    assert list_res.status_code == 200
    leads = list_res.json()["leads"]
    assert any(l["id"] == lead_id for l in leads)
    print(f" Listed {len(leads)} leads successfully.")

    print("\nTesting PUT /api/client-acquisition/leads/{lead_id}...")
    up_res = client.put(f"/api/client-acquisition/leads/{lead_id}", json={
        "status": "Sample Sent",
        "notes": "Delivered 45s Loom video link"
    })
    assert up_res.status_code == 200
    print(" Status update passed.")

    print("\nTesting DELETE /api/client-acquisition/leads/{lead_id}...")
    del_res = client.delete(f"/api/client-acquisition/leads/{lead_id}")
    assert del_res.status_code == 200
    print(" Delete lead passed.")

    print("\n ALL CLIENT ACQUISITION TESTS PASSED SUCCESSFULLY! ")

if __name__ == "__main__":
    test_api()
