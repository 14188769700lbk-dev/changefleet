import type { CampaignResult, StageName } from "../types";

interface StageRailProps {
  stages: StageName[];
  activeIndex: number;
  summary: CampaignResult["summary"];
}

export function StageRail({ stages, activeIndex, summary }: StageRailProps) {
  return (
    <section className="stage-band" id="agents" aria-label="Agent orchestration stages">
      <ol className="stage-rail">
        {stages.map((stage, index) => {
          const complete = index < activeIndex;
          const active = index === activeIndex;
          return (
            <li className={active ? "is-active" : complete ? "is-complete" : ""} key={stage}>
              <span className="stage-number">{index + 1}</span>
              <span className="stage-copy">
                <strong>{stage}</strong>
                <small>{complete ? "✓ Complete" : active ? "● In progress" : "Queued"}</small>
              </span>
            </li>
          );
        })}
      </ol>
      <p className="summary-line">
        {summary.affected_assets} affected assets <b>·</b> {summary.repairs} repairs <b>·</b> {summary.owners} owners <b>·</b> {summary.approval_gates} approval gate
      </p>
    </section>
  );
}

