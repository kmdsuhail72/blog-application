export default function Badge({ children, tone = 'neutral' }: { children: React.ReactNode; tone?: 'neutral' | 'success' | 'warning' }) {
  return <span className={`ui-badge ui-badge--${tone}`}>{children}</span>
}
