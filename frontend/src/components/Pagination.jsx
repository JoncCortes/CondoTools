export function Pagination({ page, count, pageSize = 20, onChange }) {
  const totalPages = Math.max(1, Math.ceil(count / pageSize))
  return (
    <div className="pagination">
      <button disabled={page <= 1} onClick={() => onChange(page - 1)}>Anterior</button>
      <span>Página {page} de {totalPages} ({count} registros)</span>
      <button disabled={page >= totalPages} onClick={() => onChange(page + 1)}>Próxima</button>
    </div>
  )
}
