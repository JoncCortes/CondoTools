import { Navigate, Outlet, useLocation } from 'react-router-dom'

import { pagePermissions } from '../constants/roles'
import { useAuthStore } from '../store/authStore'

export function ProtectedRoute() {
  const location = useLocation()
  const { accessToken, user } = useAuthStore()

  if (!accessToken) return <Navigate to="/login" replace />
  if (!user) return <div className="loading">Carregando sessão...</div>

  const roles = pagePermissions[location.pathname]
  if (roles && !roles.includes(user.role)) {
    return <Navigate to="/dashboard" replace />
  }

  return <Outlet />
}
