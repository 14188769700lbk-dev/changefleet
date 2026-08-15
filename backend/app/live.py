from __future__ import annotations

import os
import uuid

from google.adk.runners import InMemoryRunner
from google.genai import types

from .agent import root_agent


def live_credentials_available() -> bool:
    vertex_enabled = os.getenv("GOOGLE_GENAI_USE_VERTEXAI", "").lower() in {
        "1",
        "true",
        "yes",
    }
    return bool(
        os.getenv("GOOGLE_API_KEY")
        or (
            vertex_enabled
            and os.getenv("GOOGLE_CLOUD_PROJECT")
            and os.getenv("GOOGLE_CLOUD_LOCATION")
        )
    )


async def run_live_agent(prompt: str, user_id: str) -> str:
    if not live_credentials_available():
        raise RuntimeError(
            "Live Gemini credentials are not configured. Set GOOGLE_API_KEY or "
            "enable Vertex AI and set Google Cloud project and location variables."
        )

    runner = InMemoryRunner(node=root_agent, app_name="changefleet")
    session = await runner.session_service.create_session(
        app_name="changefleet",
        user_id=user_id,
        session_id=f"cf-{uuid.uuid4().hex[:12]}",
    )
    message = types.Content(role="user", parts=[types.Part(text=prompt)])
    final_text = ""
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session.id,
        new_message=message,
    ):
        if event.is_final_response() and event.content and event.content.parts:
            final_text = "".join(part.text or "" for part in event.content.parts)
    return final_text
