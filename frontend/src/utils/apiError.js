export function extractApiError(error) {
  const status = error?.response?.status
  const data = error?.response?.data

  if (status === 403) return 'Você não tem permissão para essa ação.'
  if (status === 401) return 'Sessão expirada. Faça login novamente.'

  if (typeof data === 'string' && data.trim()) return data
  if (data?.detail) return data.detail

  if (data && typeof data === 'object') {
    const parts = []
    for (const [key, value] of Object.entries(data)) {
      if (Array.isArray(value) && value.length) parts.push(`${key}: ${value.join(', ')}`)
      else if (typeof value === 'string' && value.trim()) parts.push(`${key}: ${value}`)
      else if (value && typeof value === 'object') {
        const nested = Object.values(value).flat().filter(Boolean)
        if (nested.length) parts.push(`${key}: ${nested.join(', ')}`)
      }
    }
    if (parts.length) return parts.join(' | ')
  }

  if (status) return `Não foi possível concluir a solicitação (HTTP ${status}).`
  return 'Não foi possível concluir a solicitação.'
}
