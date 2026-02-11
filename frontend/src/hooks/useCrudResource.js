import { useEffect, useState } from 'react'

import { api } from '../api/client'
import { extractApiError } from '../utils/apiError'

export function useCrudResource(endpoint) {
  const [items, setItems] = useState([])
  const [count, setCount] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')

  const load = async (targetPage = page) => {
    setLoading(true)
    setError('')
    try {
      const { data } = await api.get(`${endpoint}?page=${targetPage}`)
      setItems(data.results || [])
      setCount(data.count || 0)
    } catch (err) {
      setError(extractApiError(err))
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => { load(page) }, [page])

  const save = async (payload, editingId = null) => {
    setLoading(true)
    setError('')
    setSuccess('')
    try {
      if (editingId) {
        await api.patch(`${endpoint}${editingId}/`, payload)
        setSuccess('Registro atualizado com sucesso.')
      } else {
        await api.post(endpoint, payload)
        setSuccess('Registro criado com sucesso.')
      }
      await load(page)
      return true
    } catch (err) {
      setError(extractApiError(err))
      return false
    } finally {
      setLoading(false)
    }
  }

  const remove = async (id) => {
    setLoading(true)
    setError('')
    try {
      await api.delete(`${endpoint}${id}/`)
      setSuccess('Registro removido com sucesso.')
      await load(page)
      return true
    } catch (err) {
      setError(extractApiError(err))
      return false
    } finally {
      setLoading(false)
    }
  }

  return { items, count, page, setPage, loading, error, success, save, remove, reload: load }
}
