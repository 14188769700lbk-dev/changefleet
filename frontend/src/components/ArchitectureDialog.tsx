interface ArchitectureDialogProps {
  open: boolean;
  onClose: () => void;
}

const stages = [
  ["01", "Scout", "Bounded lineage + ownership"],
  ["02", "Architect", "Contract-safe migration policy"],
  ["03", "Repair", "Isolated owner-specific drafts"],
  ["04", "Govern", "Scope + mutation enforcement"],
  ["05", "Proof", "Durable evidence record"],
];

export function ArchitectureDialog({ open, onClose }: ArchitectureDialogProps) {
  return open ? (
    <div className="dialog-backdrop" role="presentation" onMouseDown={onClose}>
      <section className="architecture-dialog" role="dialog" aria-modal="true" aria-labelledby="architecture-title" onMouseDown={(event) => event.stopPropagation()}>
        <div className="dialog-heading">
          <div>
            <h2 id="architecture-title">Five agents. One mutation boundary.</h2>
            <p>Gemini 3.5 + Google ADK Workflow on Cloud Run.</p>
          </div>
          <button type="button" onClick={onClose} aria-label="Close architecture dialog">×</button>
        </div>
        <ol className="architecture-flow">
          {stages.map(([number, name, description]) => (
            <li key={name}><span>{number}</span><strong>{name}</strong><p>{description}</p></li>
          ))}
        </ol>
        <div className="policy-boundary">
          <strong>Policy boundary</strong>
          <p>Inspect, plan, draft, and validate are permitted. External writeback requires explicit approval.</p>
        </div>
      </section>
    </div>
  ) : null;
}

