export function EntityCard({ title, subtitle, meta = [], onClick }) {
  return (
    <button className="entity-card" onClick={onClick}>
      <h4>{title}</h4>
      {subtitle && <p>{subtitle}</p>}
      <div className="entity-meta">
        {meta.map((m) => <span key={m}>{m}</span>)}
      </div>
    </button>
  )
}
