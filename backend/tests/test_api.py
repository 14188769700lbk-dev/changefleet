from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health_reports_five_adk_agents() -> None:
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json()["agent_count"] == 5


def test_architecture_exposes_policy_gated_workflow() -> None:
    response = client.get("/api/architecture")

    assert response.status_code == 200
    payload = response.json()
    assert payload["root"] == "changefleet"
    assert [stage["name"] for stage in payload["stages"]] == [
        "scout",
        "architect",
        "repair",
        "govern",
        "proof",
    ]
    assert payload["mutation_boundary"] == "explicit approval"


def test_campaign_and_approval_flow() -> None:
    campaign = client.post("/api/campaigns", json={})
    assert campaign.status_code == 200
    assert campaign.json()["summary"]["repairs"] == 4

    approval = client.post("/api/campaigns/CF-204/approve")
    assert approval.status_code == 200
    assert approval.json()["writeback_applied"] is False


def test_live_endpoint_fails_closed_without_credentials(monkeypatch) -> None:
    monkeypatch.delenv("GOOGLE_API_KEY", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_PROJECT", raising=False)
    monkeypatch.delenv("GOOGLE_CLOUD_LOCATION", raising=False)
    monkeypatch.delenv("GOOGLE_GENAI_USE_VERTEXAI", raising=False)

    response = client.post("/api/adk/run", json={})

    assert response.status_code == 503
    assert "credentials" in response.json()["detail"].lower()
