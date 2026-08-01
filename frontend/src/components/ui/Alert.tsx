export default function Alert({ children, tone = 'error' }: { children: React.ReactNode; tone?: 'error' | 'info' | 'success' }) {
  return <p className={`ui-alert ui-alert--${tone}`} role="alert">{children}</p>
}
