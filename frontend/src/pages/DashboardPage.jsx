import { useEffect, useState } from 'react'

import { api } from '../api/client'
import { Alert } from '../components/Alert'
import { EmptyState } from '../components/EmptyState'

const cards = [
  ['units_total', 'Total de Unidades'],
  ['residents_total', 'Total de Moradores'],
  ['visitors_today', 'Visitantes do dia'],
  ['packages_pending', 'Encomendas pendentes'],
  ['incidents_open', 'Ocorrências abertas'],
  ['reservations_upcoming', 'Reservas próximas (7 dias)'],
]

export function DashboardPage() {
  const [summary, setSummary] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    setLoading(true)
    api.get('/dashboard/summary/')
      .then((res) => setSummary(res.data))
      .catch((err) => setError(err.response?.data?.detail || 'Falha ao carregar dashboard.'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <div className="cards-grid">{Array.from({ length: 6 }).map((_, i) => <div key={i} className="kpi-card skeleton" />)}</div>

  return (
    <div>
      <h1>Dashboard</h1>
      <Alert type="error" message={error} />
      {summary?.message && <EmptyState title="Contexto de condomínio" description={summary.message} />}
      <div className="cards-grid">
        {cards.map(([key, label]) => (
          <div className="kpi-card" key={key}>
            <p>{label}</p>
            <h2>{summary?.[key] ?? 0}</h2>
          </div>
        ))}
      </div>
    </div>
  )
}
