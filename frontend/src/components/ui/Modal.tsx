export default function Modal({ open, title, children, onClose }: { open: boolean; title: string; children: React.ReactNode; onClose: () => void }) {
  if (!open) return null
  return <div className="ui-modal-backdrop" role="presentation" onMouseDown={onClose}><section className="ui-modal" role="dialog" aria-modal="true" aria-label={title} onMouseDown={(event) => event.stopPropagation()}><header><h2>{title}</h2><button onClick={onClose} aria-label="Close">×</button></header>{children}</section></div>
}
