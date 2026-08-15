import type { Asset } from "../types";
import { DatasetIcon } from "./Icons";

interface LineageCanvasProps {
  assets: Asset[];
  isRunning: boolean;
  selectedId: string;
  onSelect: (id: string) => void;
}

function statusFor(asset: Asset): string {
  if (asset.contract === "observed_only") return "OBSERVED";
  if (asset.contract === "public_output" || asset.contract === "producer") return "CONTRACT PRESERVED";
  return "PATCH READY";
}

export function LineageCanvas({ assets, isRunning, selectedId, onSelect }: LineageCanvasProps) {
  const [source, ...downstream] = assets;
  return (
    <section className={`lineage-panel${isRunning ? " is-scanning" : ""}`} id="campaigns">
      <h2>Lineage</h2>
      <div className="lineage-canvas">
        <svg className="route-map" viewBox="0 0 760 420" preserveAspectRatio="none" aria-hidden="true">
          <path d="M210 210H316V48H365" />
          <path d="M316 210V129H365" />
          <path d="M316 210H365" />
          <path d="M316 210V291H365" />
          <path d="M316 210V372H365" />
        </svg>
        {source ? (
          <button className="asset-node source-node" type="button" onClick={() => onSelect(source.id)}>
            <DatasetIcon className="dataset-icon" />
            <span className="asset-copy"><strong>{source.label}</strong><small>{source.owner}</small></span>
            <span className="asset-status"><i />CONTRACT PRESERVED</span>
          </button>
        ) : null}
        <div className="downstream-list">
          {downstream.map((asset) => (
            <button
              className={`asset-node downstream-node${selectedId === asset.id ? " is-selected" : ""}`}
              key={asset.id}
              type="button"
              onClick={() => onSelect(asset.id)}
            >
              <DatasetIcon className="dataset-icon" />
              <span className="asset-copy"><strong>{asset.label}</strong><small>{asset.owner}</small></span>
              <span className={`asset-status${asset.contract === "observed_only" ? " is-observed" : ""}`}><i />{statusFor(asset)}</span>
            </button>
          ))}
        </div>
      </div>
    </section>
  );
}

