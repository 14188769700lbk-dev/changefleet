import { startTransition, useState } from "react";

import { ArchitectureDialog } from "./components/ArchitectureDialog";
import { ChangeForm } from "./components/ChangeForm";
import { EvidenceTimeline } from "./components/EvidenceTimeline";
import { Header } from "./components/Header";
import { LineageCanvas } from "./components/LineageCanvas";
import { RepairViewer } from "./components/RepairViewer";
import { StageRail } from "./components/StageRail";
import { fixtureCampaign } from "./data/fixture";
import type { CampaignResult } from "./types";

const wait = (milliseconds: number) => new Promise((resolve) => window.setTimeout(resolve, milliseconds));

async function requestCampaign(): Promise<CampaignResult> {
  try {
    const response = await fetch("/api/campaigns", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(fixtureCampaign.change),
    });
    if (response.ok) return await response.json() as CampaignResult;
  } catch {
    // The checked-in fixture keeps the public demo functional without a backend.
  }
  return fixtureCampaign;
}

export default function App() {
  const [campaign, setCampaign] = useState<CampaignResult>(fixtureCampaign);
  const [activeStage, setActiveStage] = useState(4);
  const [visibleEvents, setVisibleEvents] = useState(fixtureCampaign.events.length);
  const [selectedRepairIndex, setSelectedRepairIndex] = useState(2);
  const [selectedAssetId, setSelectedAssetId] = useState("revenue_by_market");
  const [isRunning, setIsRunning] = useState(false);
  const [architectureOpen, setArchitectureOpen] = useState(false);

  const repair = campaign.repairs[selectedRepairIndex] ?? campaign.repairs[0];

  async function runCampaign() {
    if (isRunning) return;
    setIsRunning(true);
    setVisibleEvents(0);
    setActiveStage(0);
    const resultPromise = requestCampaign();

    for (let stage = 0; stage < 5; stage += 1) {
      await wait(360);
      setActiveStage(stage);
      setVisibleEvents(Math.min(stage + 1, fixtureCampaign.events.length));
    }

    const result = await resultPromise;
    startTransition(() => {
      setCampaign(result);
      setVisibleEvents(result.events.length);
      setSelectedRepairIndex(2);
      setSelectedAssetId("revenue_by_market");
      setIsRunning(false);
    });
  }

  async function approveWriteback() {
    try {
      await fetch(`/api/campaigns/${campaign.campaign_id}/approve`, { method: "POST" });
    } finally {
      setCampaign((current) => ({ ...current, state: "approved" }));
    }
  }

  function moveRepair(delta: number) {
    setSelectedRepairIndex((current) => (current + delta + campaign.repairs.length) % campaign.repairs.length);
  }

  function selectAsset(assetId: string) {
    setSelectedAssetId(assetId);
    const repairIndex = campaign.repairs.findIndex((item) => item.asset_id === assetId);
    if (repairIndex >= 0) setSelectedRepairIndex(repairIndex);
  }

  return (
    <div className="app-shell">
      <Header onArchitecture={() => setArchitectureOpen(true)} />
      <main>
        <ChangeForm isRunning={isRunning} onRun={runCampaign} />
        <StageRail stages={campaign.agent_stages} activeIndex={activeStage} summary={campaign.summary} />
        <div className="workspace-grid">
          <LineageCanvas assets={campaign.assets} isRunning={isRunning} selectedId={selectedAssetId} onSelect={selectAsset} />
          <EvidenceTimeline events={campaign.events} visibleCount={visibleEvents} />
        </div>
        <RepairViewer
          repair={repair}
          repairIndex={selectedRepairIndex}
          repairCount={campaign.repairs.length}
          approved={campaign.state === "approved"}
          onPrevious={() => moveRepair(-1)}
          onNext={() => moveRepair(1)}
          onApprove={approveWriteback}
        />
      </main>
      <ArchitectureDialog open={architectureOpen} onClose={() => setArchitectureOpen(false)} />
    </div>
  );
}

