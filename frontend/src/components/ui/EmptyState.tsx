import { FiFileText } from 'react-icons/fi'

export default function EmptyState({ title = 'Nothing here yet', description = 'Check back soon for new content.' }: { title?: string; description?: string }) {
  return <div className="empty-state"><FiFileText size={32} /><h2>{title}</h2><p>{description}</p></div>
}
