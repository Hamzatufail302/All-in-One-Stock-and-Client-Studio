import asyncio
import os, sys
sys.path.insert(0, os.path.abspath("."))
import app

async def run_tests():
    print("Testing get_youtube_overview()...")
    overview = await app.get_youtube_overview()
    assert "channels" in overview
    assert "video_blueprints" in overview
    assert len(overview["channels"]) == 4
    print(f" Overview passed: {len(overview['channels'])} channels, {sum(len(v) for v in overview['video_blueprints'].values())} blueprints.")

    print("\nTesting generate_idea_endpoint() for ink_explainer...")
    idea_req = app.YouTubeIdeaRequest(channel_id="ink_explainer", seed_keyword="thunderstorm survival")
    idea = await app.generate_idea_endpoint(idea_req)
    assert "title" in idea and "thumbnail_text" in idea and "ai_prompt" in idea
    print(f" Idea generated: '{idea['title']}' | Thumbnail text: '{idea['thumbnail_text']}'")

    print("\nTesting generate_ink_prompt_endpoint()...")
    prompt_req = app.InkPromptRequest(topic="Ancient human winter survival", scene_type="mammoth cave")
    ink_prompt = await app.generate_ink_prompt_endpoint(prompt_req)
    assert "full_prompt" in ink_prompt and "after_effects_recipe" in ink_prompt
    print(f" Ink prompt generated: '{ink_prompt['full_prompt'][:80]}...'")

    print("\nAll YouTube Studio tests passed successfully!")

if __name__ == "__main__":
    asyncio.run(run_tests())
