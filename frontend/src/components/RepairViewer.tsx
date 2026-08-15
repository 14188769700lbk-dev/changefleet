import type { RepairArtifact } from "../types";
import { ArrowIcon } from "./Icons";

interface RepairViewerProps {
  repair: RepairArtifact;
  repairIndex: number;
  repairCount: number;
  approved: boolean;
  onPrevious: () => void;
  onNext: () => void;
  onApprove: () => void;
}

function CodePane({ title, lines, tone }: { title: string; lines: string[]; tone: "current" | "proposed" }) {
  return (
    <div className={`code-pane is-${tone}`}>
      <h3>{tone === "current" ? "−" : "+"} &nbsp; {title}</h3>
      <pre>{lines.map((line, index) => <code key={`${line}-${index}`}><span>{12 + index}</span>{line || " "}</code>)}</pre>
    </div>
  );
}

export function RepairViewer({ repair, repairIndex, repairCount, approved, onPrevious, onNext, onApprove }: RepairViewerProps) {
  return (
    <section className="repair-viewer" id="policies">
      <div className="repair-toolbar">
        <strong>{repair.file}</strong>
        <span>Repair {repairIndex + 1} of {repairCount}</span>
        <div className="repair-nav" aria-label="Repair navigation">
          <button type="button" onClick={onPrevious} aria-label="Previous repair">←</button>
          <button type="button" onClick={onNext} aria-label="Next repair">→</button>
        </div>
        <button className="button button-outline" type="button">Review patch</button>
        <button className={`button ${approved ? "button-approved" : "button-approve"}`} type="button" onClick={onApprove} disabled={approved}>
          {approved ? "Approval recorded" : "Approve writeback"}
          <ArrowIcon className="button-icon" />
        </button>
      </div>
      <div className="diff-grid">
        <CodePane title="Current" lines={repair.current_sql} tone="current" />
        <CodePane title="Proposed" lines={repair.proposed_sql} tone="proposed" />
        <dl className="repair-meta">
          <div><dt>Owner</dt><dd>{repair.owner}</dd></div>
          <div><dt>Asset</dt><dd>{repair.asset_id}</dd></div>
          <div><dt>Policy</dt><dd>schema-evolution/v1</dd></div>
          <div><dt>Strategy</dt><dd>{repair.strategy}</dd></div>
          <div><dt>Status</dt><dd><i />{approved ? "APPROVED" : "PATCH READY"}</dd></div>
        </dl>
      </div>
    </section>
  );
}

