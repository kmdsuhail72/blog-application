export default function Avatar({ name, src }: { name: string; src?: string }) {
  return src ? <img className="ui-avatar" src={src} alt={name} /> : <span className="ui-avatar" aria-label={name}>{name.slice(0, 1).toUpperCase()}</span>
}
