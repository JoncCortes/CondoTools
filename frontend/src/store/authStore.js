import { create } from 'zustand'
import { fetchCurrentUser } from '../api/client'

const storage = {
  get: (key) => localStorage.getItem(key),
  set: (key, value) => localStorage.setItem(key, value),
  remove: (key) => localStorage.removeItem(key),
}

export const useAuthStore = create((set, get) => ({
  accessToken: storage.get('accessToken'),
  refreshToken: storage.get('refreshToken'),
  user: null,
  isLoading: false,

  setTokens: ({ access, refresh }) => {
    storage.set('accessToken', access)
    storage.set('refreshToken', refresh)
    set({ accessToken: access, refreshToken: refresh })
  },

  setUser: (user) => set({ user }),

  clearAuth: () => {
    storage.remove('accessToken')
    storage.remove('refreshToken')
    set({ accessToken: null, refreshToken: null, user: null })
  },

  login: async (email, password, api) => {
    set({ isLoading: true })
    try {
      const { data } = await api.post('/auth/token/', { email, password })
      get().setTokens(data)
      const user = await fetchCurrentUser()
      set({ user })
    } finally {
      set({ isLoading: false })
    }
  },

  bootstrap: async () => {
    const token = get().accessToken
    if (!token || get().user) return
    try {
      const user = await fetchCurrentUser()
      set({ user })
    } catch {
      get().clearAuth()
    }
  },
}))
