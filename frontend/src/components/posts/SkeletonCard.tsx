import Skeleton from '../ui/Skeleton'

export default function SkeletonCard() { return <div className="loading-card"><Skeleton className="loading-card__image" /><Skeleton /><Skeleton className="loading-card__line" /><Skeleton className="loading-card__line" /></div> }
