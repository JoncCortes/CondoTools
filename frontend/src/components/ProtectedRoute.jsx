import { Navigate, Outlet, useLocation } from 'react-router-dom'

import { routePermissionMap } from '../constants/roles'
import { useAuthStore } from '../store/authStore'

export function ProtectedRoute() {
  const location = useLocation()
  const { accessToken, user, permissions } = useAuthStore()

  if (!accessToken) return <Navigate to="/login" replace />
  if (!user) return <div className="loading">Carregando sessão...</div>

  const required = routePermissionMap[location.pathname]
  if (required && !permissions.includes(required) && user.role !== 'PLATFORM_ADMIN') {
    return <Navigate to="/dashboard" replace />
  }

  return <Outlet />
}
