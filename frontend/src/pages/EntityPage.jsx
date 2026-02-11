import { useMemo, useState } from 'react'

import { Alert } from '../components/Alert'
import { EmptyState } from '../components/EmptyState'
import { EntityCard } from '../components/EntityCard'
import { EntityForm } from '../components/EntityForm'
import { Loading } from '../components/Loading'
import { Modal } from '../components/Modal'
import { Pagination } from '../components/Pagination'
import { useCrudResource } from '../hooks/useCrudResource'
import { useAuthStore } from '../store/authStore'

export function EntityPage({ config }) {
  const { items, count, page, setPage, loading, error, success, save, remove } = useCrudResource(config.endpoint)
  const [createOpen, setCreateOpen] = useState(false)
  const [detailOpen, setDetailOpen] = useState(false)
  const [selected, setSelected] = useState(null)
  const [editing, setEditing] = useState(false)
  const [formValues, setFormValues] = useState({})
  const { user, activeCondominiumId } = useAuthStore()

  const fields = useMemo(() => config.fields, [config.fields])

  const onSelect = (item) => {
    setSelected(item)
    setFormValues(item)
    setDetailOpen(true)
    setEditing(false)
  }

  const onSubmitCreate = async (e) => {
    e.preventDefault()
    const ok = await save(formValues)
    if (ok) {
      setCreateOpen(false)
      setFormValues({})
    }
  }

  const onSubmitEdit = async (e) => {
    e.preventDefault()
    const ok = await save(formValues, selected?.id)
    if (ok) {
      setEditing(false)
      setDetailOpen(false)
      setSelected(null)
    }
  }

  const grouped = config.groupBy
    ? Object.entries(items.reduce((acc, item) => {
      const key = config.groupBy(item)
      acc[key] = acc[key] || []
      acc[key].push(item)
      return acc
    }, {}))
    : [['', items]]

  const requiresCondo = user?.role === 'PLATFORM_ADMIN' && !activeCondominiumId

  return (
    <div>
      <div className="page-head">
        <h1>{config.title}</h1>
        <button onClick={() => { setCreateOpen(true); setFormValues({}) }}>Criar / Registrar</button>
      </div>

      {requiresCondo && <EmptyState title="Selecione um condomínio ativo" description="Use o seletor no topo para carregar e criar registros deste módulo." />}
      <Alert type="success" message={success} />
      <Alert type="error" message={error} />

      {loading ? <Loading /> : (
        grouped.map(([group, groupItems]) => (
          <div key={group || 'default'}>
            {group && <h3 className="group-title">{group}</h3>}
            <div className="cards-grid">
              {groupItems.map((item) => {
                const c = config.card ? config.card(item) : { title: String(item.id), subtitle: '', meta: [] }
                return <EntityCard key={item.id} title={c.title} subtitle={c.subtitle} meta={c.meta} onClick={() => onSelect(item)} />
              })}
            </div>
          </div>
        ))
      )}

      {!loading && items.length === 0 && !requiresCondo && (
        <EmptyState title="Nenhum registro" description="Clique em Criar / Registrar para adicionar o primeiro item." />
      )}

      <Pagination page={page} count={count} onChange={setPage} />

      <Modal open={createOpen} title={`Novo ${config.title}`} onClose={() => setCreateOpen(false)}>
        <EntityForm
          fields={fields}
          values={formValues}
          onChange={(name, value) => setFormValues((v) => ({ ...v, [name]: value }))}
          onSubmit={onSubmitCreate}
          loading={loading}
        />
      </Modal>

      <Modal open={detailOpen} title={config.title} onClose={() => setDetailOpen(false)}>
        {!editing && selected && (
          <div>
            <pre className="json-preview">{JSON.stringify(selected, null, 2)}</pre>
            <div className="row-actions">
              <button onClick={() => setEditing(true)}>Editar</button>
              <button className="danger" onClick={async () => { const ok = await remove(selected.id); if (ok) setDetailOpen(false) }}>Excluir</button>
            </div>
          </div>
        )}
        {editing && (
          <EntityForm
            fields={fields}
            values={formValues}
            onChange={(name, value) => setFormValues((v) => ({ ...v, [name]: value }))}
            onSubmit={onSubmitEdit}
            submitLabel="Salvar alterações"
            loading={loading}
          />
        )}
      </Modal>
    </div>
  )
}
