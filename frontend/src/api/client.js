import axios from 'axios'
import { useAuthStore } from '../store/authStore'
import { parseJwt } from '../utils/jwt'

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
  const { accessToken } = useAuthStore.getState()
  const payload = parseJwt(accessToken)
  if (!payload?.user_id) return null
  const { data } = await api.get(`/users/${payload.user_id}/`)
  return data
}

api.interceptors.request.use((config) => {
  const { accessToken } = useAuthStore.getState()
  if (accessToken) config.headers.Authorization = `Bearer ${accessToken}`
  return config
})

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const original = error.config
    const status = error.response?.status
    const { refreshToken, clearAuth, setTokens } = useAuthStore.getState()

    if (status !== 401 || original._retry || !refreshToken) {
      return Promise.reject(error)
    }

    if (isRefreshing) {
      return new Promise((resolve, reject) => {
        queue.push({ resolve, reject })
      }).then((token) => {
        original.headers.Authorization = `Bearer ${token}`
        return api(original)
      })
    }

    original._retry = true
    isRefreshing = true

    try {
      const { data } = await rawClient.post('/auth/token/refresh/', { refresh: refreshToken })
      setTokens({ access: data.access, refresh: refreshToken })
      flushQueue(null, data.access)
      original.headers.Authorization = `Bearer ${data.access}`
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
