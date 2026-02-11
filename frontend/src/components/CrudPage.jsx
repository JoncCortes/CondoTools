import { useEffect, useState } from 'react'
import { api } from '../api/client'

export function CrudPage({ title, endpoint, fields }) {
  const [items, setItems] = useState([])
  const [form, setForm] = useState({})
  const [page, setPage] = useState(1)
  const [count, setCount] = useState(0)
  const [error, setError] = useState('')

  const load = async (targetPage = page) => {
    const { data } = await api.get(`/${endpoint}/?page=${targetPage}`)
    setItems(data.results || [])
    setCount(data.count || 0)
  }

  useEffect(() => { load(page) }, [page])

  const submit = async (e) => {
    e.preventDefault()
    for (const field of fields) {
      if (field.required && !form[field.name]) {
        setError(`Campo obrigatório: ${field.label}`)
        return
      }
    }
    setError('')
    await api.post(`/${endpoint}/`, form)
    setForm({})
    load(1)
    setPage(1)
  }

  return (
    <div>
      <h1>{title}</h1>
      <form onSubmit={submit} className="form-grid">
        {fields.map((field) => (
          <input
            key={field.name}
            placeholder={field.label}
            value={form[field.name] || ''}
            onChange={(e) => setForm({ ...form, [field.name]: e.target.value })}
          />
        ))}
        <button type="submit">Salvar</button>
      </form>
      {error && <p className="error">{error}</p>}
      <table>
        <thead>
          <tr>{fields.map((f) => <th key={f.name}>{f.label}</th>)}</tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>{fields.map((f) => <td key={f.name}>{String(item[f.name] ?? '')}</td>)}</tr>
          ))}
        </tbody>
      </table>
      <div className="pagination">
        <button disabled={page <= 1} onClick={() => setPage(page - 1)}>Anterior</button>
        <span>Página {page} ({count} registros)</span>
        <button disabled={items.length === 0} onClick={() => setPage(page + 1)}>Próxima</button>
      </div>
    </div>
  )
}
