import asyncio
import app

async def run_direct_tests():
    print("Testing get_client_acquisition_data()...")
    overview = await app.get_client_acquisition_data()
    assert "current_requirements" in overview
    assert "prospecting_playbooks" in overview
    assert len(overview["current_requirements"]) == 6
    assert len(overview["prospecting_playbooks"]) == 5
    print(f" Overview passed: {len(overview['current_requirements'])} requirements, {len(overview['prospecting_playbooks'])} playbooks.")

    print("\nTesting generate_pitch_endpoint()...")
    req = app.GeneratePitchRequest(
        client_name="Ali Abdaal",
        channel_or_niche="Productivity & Tech",
        pitch_type="youtube_sample",
        custom_link="https://drive.google.com/sample"
    )
    pitch = await app.generate_pitch_endpoint(req)
    assert "subject" in pitch and "body" in pitch
    print(f" Pitch generated: '{pitch['subject']}'")

    print("\nTesting add_outreach_lead()...")
    lead_req = app.SaveLeadRequest(
        client_name="Ali Abdaal",
        channel_or_website="https://youtube.com/@aliabdaal",
        client_niche="Productivity & Tech",
        outreach_channel="Email",
        pitch_content=pitch["body"],
        status="Targeted",
        followup_date="2026-10-10",
        notes="High retention hook sample prepared"
    )
    save_res = await app.add_outreach_lead(lead_req)
    assert save_res["success"] is True
    lead_id = save_res["lead_id"]
    print(f" Lead saved with ID {lead_id}")

    print("\nTesting list_outreach_leads()...")
    list_res = await app.list_outreach_leads(None)
    leads = list_res["leads"]
    assert any(l["id"] == lead_id for l in leads)
    print(f" Listed {len(leads)} leads in CRM.")

    print("\nTesting update_outreach_lead_endpoint()...")
    up_req = app.UpdateLeadRequest(
        status="Sample Sent",
        notes="Loom 45s preview link delivered"
    )
    up_res = await app.update_outreach_lead_endpoint(lead_id, up_req)
    assert up_res["success"] is True
    print(" Lead status updated.")

    print("\nTesting remove_outreach_lead()...")
    del_res = await app.remove_outreach_lead(lead_id)
    assert del_res["success"] is True
    print(" Lead removed from CRM.")

    print("\n ALL DIRECT ENDPOINT TESTS PASSED COMPLETELY! ")

if __name__ == "__main__":
    asyncio.run(run_direct_tests())
