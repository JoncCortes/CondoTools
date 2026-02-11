import { useMemo } from 'react'

export function EntityForm({ fields, values, onChange, onSubmit, submitLabel = 'Salvar', loading }) {
  const hasErrors = useMemo(
    () => fields.some((f) => f.required && !values[f.name]),
    [fields, values],
  )

  return (
    <form className="form-grid" onSubmit={onSubmit}>
      {fields.map((field) => (
        <div key={field.name} className="field-wrap">
          <label>{field.label}{field.required ? ' *' : ''}</label>
          <input
            type={field.type || 'text'}
            value={values[field.name] ?? ''}
            onChange={(e) => onChange(field.name, e.target.value)}
            placeholder={field.label}
          />
        </div>
      ))}
      <button type="submit" disabled={loading || hasErrors}>{loading ? 'Salvando...' : submitLabel}</button>
    </form>
  )
}
