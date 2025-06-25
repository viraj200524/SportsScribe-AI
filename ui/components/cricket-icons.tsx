import type { LightbulbIcon as LucideProps } from "lucide-react"

export function CricketBat(props: LucideProps) {
  return (
    <svg
      {...props}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M3 12h18" />
      <path d="M3 6h18" />
      <path d="M3 18h18" />
      <circle cx="12" cy="12" r="2" />
    </svg>
  )
}

export function CricketBall(props: LucideProps) {
  return (
    <svg
      {...props}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <circle cx="12" cy="12" r="10" />
      <path d="M8 12c0-4 2-6 4-6s4 2 4 6-2 6-4 6-4-2-4-6z" />
      <path d="M12 2v20" />
    </svg>
  )
}

export function CricketStumps(props: LucideProps) {
  return (
    <svg
      {...props}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="2"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <path d="M6 2v20" />
      <path d="M12 2v20" />
      <path d="M18 2v20" />
      <path d="M4 4h16" />
      <path d="M4 6h16" />
    </svg>
  )
}
