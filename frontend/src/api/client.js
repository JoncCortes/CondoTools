import axios from 'axios'
import { useAuthStore } from '../store/authStore'

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

export const api = axios.create({ baseURL: API_URL })
const rawClient = axios.create({ baseURL: API_URL })

let isRefreshing = false
let queue = []

function flushQueue(error, token = null) {
  queue.forEach((p) => (error ? p.reject(error) : p.resolve(token)))
  queue = []
}

export async function fetchCurrentUser() {
  const { data } = await api.get('/users/me/')
  return data
}

export async function fetchMyPermissions() {
  const { data } = await api.get('/permissions/me/')
  return data
}

export async function fetchPermissionRegistry() {
  const { data } = await api.get('/permissions/registry/')
  return data
}

api.interceptors.request.use((config) => {
  const { accessToken, activeCondominiumId } = useAuthStore.getState()
  if (accessToken) config.headers.Authorization = `Bearer ${accessToken}`
  if (activeCondominiumId) config.headers['X-CONDOMINIUM-ID'] = activeCondominiumId
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config || {}
    const status = error.response?.status
    const { refreshToken, clearAuth, setTokens } = useAuthStore.getState()

    if (status !== 401 || original._retry || !refreshToken) {
      return Promise.reject(error)
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => queue.push({ resolve, reject })).then((token) => {
        original.headers = { ...(original.headers || {}), Authorization: `Bearer ${token}` }
        return api(original)
      })
    }

    original._retry = true
    isRefreshing = true

    try {
      const { data } = await rawClient.post('/auth/token/refresh/', { refresh: refreshToken })
      setTokens({ access: data.access, refresh: refreshToken })
      flushQueue(null, data.access)
      original.headers = { ...(original.headers || {}), Authorization: `Bearer ${data.access}` }
      return api(original)
    } catch (err) {
      flushQueue(err, null)
      clearAuth()
      return Promise.reject(err)
    } finally {
      isRefreshing = false
    }
  },
)
