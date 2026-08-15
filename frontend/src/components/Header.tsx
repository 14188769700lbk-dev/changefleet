import { ArchitectureIcon, BrandMark } from "./Icons";

interface HeaderProps {
  onArchitecture: () => void;
}

export function Header({ onArchitecture }: HeaderProps) {
  return (
    <header className="app-header">
      <a className="brand" href="#main" aria-label="ChangeFleet home">
        <BrandMark className="brand-mark" />
        <span>ChangeFleet</span>
      </a>
      <nav aria-label="Primary navigation">
        {['Campaigns', 'Agents', 'Policies', 'Evidence'].map((item) => (
          <a key={item} href={`#${item.toLowerCase()}`}>{item}</a>
        ))}
      </nav>
      <div className="header-actions">
        <span className="mode-label">Fixture mode</span>
        <button className="button button-outline" type="button" onClick={onArchitecture}>
          <ArchitectureIcon className="button-icon" />
          Architecture
        </button>
      </div>
    </header>
  );
}

