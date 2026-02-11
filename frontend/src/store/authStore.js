import { create } from 'zustand'
import { fetchCurrentUser, fetchMyPermissions } from '../api/client'

const storage = {
  get: (key) => localStorage.getItem(key),
  set: (key, value) => localStorage.setItem(key, value),
  remove: (key) => localStorage.removeItem(key),
}

export const useAuthStore = create((set, get) => ({
  accessToken: storage.get('accessToken'),
  refreshToken: storage.get('refreshToken'),
  activeCondominiumId: storage.get('activeCondominiumId'),
  user: null,
  permissions: [],
  isLoading: false,

  setActiveCondominium: (id) => {
    if (!id) {
      storage.remove('activeCondominiumId')
      set({ activeCondominiumId: null })
      return
    }
    storage.set('activeCondominiumId', String(id))
    set({ activeCondominiumId: String(id) })
  },

  setTokens: ({ access, refresh }) => {
    storage.set('accessToken', access)
    storage.set('refreshToken', refresh)
    set({ accessToken: access, refreshToken: refresh })
  },

  clearAuth: () => {
    storage.remove('accessToken')
    storage.remove('refreshToken')
    storage.remove('activeCondominiumId')
    set({ accessToken: null, refreshToken: null, user: null, activeCondominiumId: null, permissions: [] })
  },

  login: async (email, password, api) => {
    set({ isLoading: true })
    try {
      const { data } = await api.post('/auth/token/', { email, password })
      get().setTokens(data)
      const [user, permsData] = await Promise.all([fetchCurrentUser(), fetchMyPermissions()])
      set({ user, permissions: permsData.permissions || [] })
      if (user?.role !== 'PLATFORM_ADMIN' && user?.condominium) {
        get().setActiveCondominium(user.condominium)
      }
    } finally {
      set({ isLoading: false })
    }
  },

  bootstrap: async () => {
    const token = get().accessToken
    if (!token || get().user) return
    try {
      const [user, permsData] = await Promise.all([fetchCurrentUser(), fetchMyPermissions()])
      set({ user, permissions: permsData.permissions || [] })
      if (user?.role !== 'PLATFORM_ADMIN' && user?.condominium) {
        get().setActiveCondominium(user.condominium)
      }
    } catch {
      get().clearAuth()
    }
  },
}))
