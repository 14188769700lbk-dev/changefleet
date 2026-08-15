import { ArrowIcon } from "./Icons";

interface ChangeFormProps {
  isRunning: boolean;
  onRun: () => void;
}

export function ChangeForm({ isRunning, onRun }: ChangeFormProps) {
  return (
    <section className="intro" id="main">
      <h1>Protect every downstream contract.</h1>
      <p>An agent fleet turns one risky schema change into owner-specific repairs, policy gates, and durable proof.</p>
      <div className="change-strip" aria-label="Proposed schema change">
        <div className="change-field">
          <span>Source</span>
          <strong>warehouse.orders</strong>
        </div>
        <div className="change-field change-field-wide">
          <span>Change</span>
          <strong>shipping_country <b aria-hidden="true">→</b> country_code</strong>
        </div>
        <button className="button button-primary" type="button" onClick={onRun} disabled={isRunning}>
          {isRunning ? "Coordinating fleet…" : "Run coordinated repair"}
          <ArrowIcon className="button-icon" />
        </button>
      </div>
    </section>
  );
}

