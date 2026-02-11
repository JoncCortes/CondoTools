import { useEffect, useState } from 'react'

import { api } from '../api/client'
import { Alert } from '../components/Alert'

const tabs = ['condominios', 'usuarios', 'menu-paginas']

function CrudTab({ title, endpoint, fields }) {
  const [items, setItems] = useState([])
  const [form, setForm] = useState({})
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const load = () => api.get(endpoint).then((r) => setItems(r.data.results || r.data))
  useEffect(() => { load() }, [endpoint])

  const submit = async (e) => {
    e.preventDefault()
    try {
      await api.post(endpoint, form)
      setSuccess('Criado com sucesso.')
      setError('')
      setForm({})
      load()
    } catch (err) {
      setError(JSON.stringify(err.response?.data || {}))
    }
  }

  return (
    <div>
      <h2>{title}</h2>
      <Alert type="success" message={success} />
      <Alert type="error" message={error} />
      <form className="form-grid" onSubmit={submit}>
        {fields.map((f) => (
          <input key={f} value={form[f] || ''} onChange={(e) => setForm({ ...form, [f]: e.target.value })} placeholder={f} />
        ))}
        <button type="submit">Criar</button>
      </form>
      <div className="cards-grid">
        {items.map((item) => <div className="small-card" key={item.id}>{item.name || item.email || item.label || item.title}</div>)}
      </div>
    </div>
  )
}

export function SettingsPage() {
  const [tab, setTab] = useState(tabs[0])

  return (
    <div>
      <h1>Configurações</h1>
      <div className="tabs">
        {tabs.map((t) => <button key={t} onClick={() => setTab(t)} className={tab === t ? 'active' : ''}>{t}</button>)}
      </div>

      {tab === 'condominios' && <CrudTab title="Condomínios" endpoint="/condominiums/" fields={['name', 'document', 'address']} />}
      {tab === 'usuarios' && <CrudTab title="Usuários" endpoint="/users/" fields={['email', 'password', 'first_name', 'last_name', 'role', 'condominium']} />}
      {tab === 'menu-paginas' && (
        <>
          <CrudTab title="Categorias" endpoint="/settings/menu-categories/" fields={['name', 'order']} />
          <CrudTab title="Itens de menu" endpoint="/settings/menu-items/" fields={['key', 'label', 'path', 'category', 'order', 'enabled', 'allowed_roles']} />
          <CrudTab title="Páginas customizadas" endpoint="/settings/custom-pages/" fields={['title', 'slug', 'category', 'content', 'allowed_roles', 'enabled']} />
        </>
      )}
    </div>
  )
}
