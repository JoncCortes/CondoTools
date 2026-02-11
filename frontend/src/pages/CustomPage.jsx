import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'

import { api } from '../api/client'
import { Alert } from '../components/Alert'

export function CustomPage() {
  const { slug } = useParams()
  const [page, setPage] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => {
    api.get(`/pages/${slug}/`).then((res) => setPage(res.data)).catch(() => setError('Página não encontrada.'))
  }, [slug])

  return (
    <div>
      <Alert type="error" message={error} />
      <h1>{page?.title}</h1>
      <div className="markdown">{page?.content}</div>
    </div>
  )
}
