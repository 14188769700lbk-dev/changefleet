from app.engine import FleetEngine
from app.models import ChangeRequest


def test_campaign_has_complete_bounded_evidence() -> None:
    result = FleetEngine().run(ChangeRequest())

    assert result.state == "approval_required"
    assert result.summary.model_dump() == {
        "affected_assets": 6,
        "repairs": 4,
        "owners": 3,
        "approval_gates": 1,
    }
    assert [event.stage for event in result.events] == [
        "Scout",
        "Scout",
        "Repair",
        "Govern",
        "Proof",
    ]
    assert {repair.asset_id for repair in result.repairs} == {
        "warehouse.orders",
        "shipping_performance",
        "revenue_by_market",
        "daily_fulfillment",
    }


def test_public_contract_reads_new_field_without_renaming_output() -> None:
    result = FleetEngine().run(ChangeRequest())
    repair = next(item for item in result.repairs if item.asset_id == "revenue_by_market")

    assert any("country_code AS country" in line for line in repair.proposed_sql)
    assert repair.strategy == "Preserve the public output contract"


def test_approval_is_recorded_without_external_mutation() -> None:
    engine = FleetEngine()
    engine.run(ChangeRequest())

    approval = engine.approve("CF-204")

    assert approval.state == "approved"
    assert approval.writeback_applied is False

