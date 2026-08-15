interface IconProps {
  className?: string;
}

export function BrandMark({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 32 32" aria-hidden="true">
      <rect width="32" height="32" fill="currentColor" />
      <path d="M6 10.5 14 7l5 2.25L26 6v5.5L19 15l-5-2.25-8 3.5v-5.75Z" fill="white" />
      <path d="m6 21 8-3.5 5 2.25 7-3.25V22l-7 3.5-5-2.25L6 26.5V21Z" fill="white" />
    </svg>
  );
}

export function ArchitectureIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <path d="M12 4v5M5 13V9h14v4M5 13v3M12 13v3M19 13v3" stroke="currentColor" strokeWidth="1.6" />
      <rect x="9.5" y="2" width="5" height="4" fill="currentColor" />
      <rect x="2.5" y="16" width="5" height="4" fill="currentColor" />
      <rect x="9.5" y="16" width="5" height="4" fill="currentColor" />
      <rect x="16.5" y="16" width="5" height="4" fill="currentColor" />
    </svg>
  );
}

export function DatasetIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" aria-hidden="true">
      <rect x="3" y="3" width="18" height="18" stroke="currentColor" strokeWidth="1.4" />
      <path d="M3 9h18M3 15h18M9 3v18M15 3v18" stroke="currentColor" strokeWidth="1.1" />
    </svg>
  );
}

export function ArrowIcon({ className }: IconProps) {
  return (
    <svg className={className} viewBox="0 0 20 20" fill="none" aria-hidden="true">
      <path d="M3 10h13M11 5l5 5-5 5" stroke="currentColor" strokeWidth="1.8" />
    </svg>
  );
}

