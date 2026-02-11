import { useMemo } from 'react'

export function EntityForm({ fields, values, onChange, onSubmit, submitLabel = 'Salvar', loading }) {
  const hasErrors = useMemo(
    () => fields.some((f) => f.required && !String(values[f.name] ?? '').trim()),
    [fields, values],
  )

  return (
    <form className="form-grid" onSubmit={onSubmit}>
      {fields.map((field) => (
        <div key={field.name} className="field-wrap">
          <label>{field.label}{field.required ? ' *' : ''}</label>
          {field.type === 'textarea' ? (
            <textarea
              value={values[field.name] ?? ''}
              onChange={(e) => onChange(field.name, e.target.value)}
              placeholder={field.label}
            />
          ) : field.type === 'select' ? (
            <select
              value={values[field.name] ?? ''}
              onChange={(e) => onChange(field.name, e.target.value || null)}
            >
              <option value="">Selecione</option>
              {(field.options || []).map((opt) => (
                <option key={opt.value} value={opt.value}>{opt.label}</option>
              ))}
            </select>
          ) : (
            <input
              type={field.type || 'text'}
              value={values[field.name] ?? ''}
              onChange={(e) => onChange(field.name, e.target.value)}
              placeholder={field.label}
            />
          )}
        </div>
      ))}
      <button type="submit" disabled={loading || hasErrors}>{loading ? 'Salvando...' : submitLabel}</button>
    </form>
  )
}
