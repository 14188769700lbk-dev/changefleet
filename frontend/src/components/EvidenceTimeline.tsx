import type { EvidenceEvent } from "../types";

interface EvidenceTimelineProps {
  events: EvidenceEvent[];
  visibleCount: number;
}

function timestamp(offset: number): string {
  const base = 10 * 3600 + 21 * 60 + 3 + offset;
  const hours = String(Math.floor(base / 3600)).padStart(2, "0");
  const minutes = String(Math.floor((base % 3600) / 60)).padStart(2, "0");
  const seconds = String(base % 60).padStart(2, "0");
  return `${hours}:${minutes}:${seconds}`;
}

export function EvidenceTimeline({ events, visibleCount }: EvidenceTimelineProps) {
  return (
    <aside className="evidence-panel" id="evidence">
      <div className="section-heading">
        <h2>Live evidence</h2>
        <span>Auto-scroll on</span>
      </div>
      <ol className="timeline" aria-live="polite">
        {events.slice(0, visibleCount).map((event) => (
          <li className={`timeline-event is-${event.status}`} key={`${event.stage}-${event.title}`}>
            <span className="timeline-mark">{event.status === "approval_required" ? "!" : "✓"}</span>
            <div>
              <strong>{event.title}</strong>
              <p>{event.detail}</p>
            </div>
            <time>{timestamp(event.offset_seconds)}</time>
          </li>
        ))}
      </ol>
    </aside>
  );
}

