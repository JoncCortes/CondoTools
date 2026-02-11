import { useMemo, useState } from 'react'

import { Alert } from '../components/Alert'
import { DataTable } from '../components/DataTable'
import { EntityForm } from '../components/EntityForm'
import { Loading } from '../components/Loading'
import { Pagination } from '../components/Pagination'
import { useCrudResource } from '../hooks/useCrudResource'

export function EntityPage({ config }) {
  const { items, count, page, setPage, loading, error, success, save } = useCrudResource(config.endpoint)
  const [editing, setEditing] = useState(null)
  const [formValues, setFormValues] = useState({})

  const fields = useMemo(() => config.fields, [config.fields])

  const onEdit = (row) => {
    setEditing(row)
    setFormValues(row)
  }

  const onChange = (name, value) => {
    setFormValues((prev) => ({ ...prev, [name]: value }))
  }

  const onSubmit = async (e) => {
    e.preventDefault()
    const payload = fields.reduce((acc, f) => {
      const raw = formValues[f.name]
      if (raw === undefined || raw === '') return acc
      acc[f.name] = f.type === 'number' ? Number(raw) : raw
      return acc
    }, {})

    for (const field of fields) {
      if (field.required && (payload[field.name] === undefined || payload[field.name] === '')) {
        return
      }
    }

    const ok = await save(payload, editing?.id)
    if (ok) {
      setEditing(null)
      setFormValues({})
    }
  }

  return (
    <div>
      <h1>{config.title}</h1>
      <Alert type="success" message={success} />
      <Alert type="error" message={error} />
      <EntityForm
        fields={fields}
        values={formValues}
        onChange={onChange}
        onSubmit={onSubmit}
        submitLabel={editing ? 'Atualizar' : 'Criar'}
        loading={loading}
      />

      {loading ? <Loading /> : <DataTable fields={fields} rows={items} onEdit={onEdit} />}
      <Pagination page={page} count={count} onChange={setPage} />
    </div>
  )
}
