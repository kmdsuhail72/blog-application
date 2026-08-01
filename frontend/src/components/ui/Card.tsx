export default function Card({ children, className = '' }: { children: React.ReactNode; className?: string }) {
  return <section className={`ui-card ${className}`}>{children}</section>
}
