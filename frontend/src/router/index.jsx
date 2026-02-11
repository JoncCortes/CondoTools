import { createBrowserRouter, Navigate } from 'react-router-dom'

import { resources } from '../api/resources'
import { ProtectedRoute } from '../components/ProtectedRoute'
import { AppLayout } from '../layouts/AppLayout'
import { DashboardPage } from '../pages/DashboardPage'
import { EntityPage } from '../pages/EntityPage'
import { LoginPage } from '../pages/LoginPage'
import { ProfilePage } from '../pages/ProfilePage'

const entity = (cfg) => <EntityPage config={cfg} />

export const router = createBrowserRouter([
  { path: '/login', element: <LoginPage /> },
  {
    element: <ProtectedRoute />,
    children: [
      {
        element: <AppLayout />,
        children: [
          { path: '/', element: <Navigate to="/dashboard" replace /> },
          { path: '/dashboard', element: <DashboardPage /> },
          { path: '/units', element: entity(resources.units) },
          { path: '/residents', element: entity(resources.residents) },
          { path: '/visitors', element: entity(resources.visitors) },
          { path: '/visit-logs', element: entity(resources.visitLogs) },
          { path: '/packages', element: entity(resources.packages) },
          { path: '/announcements', element: entity(resources.announcements) },
          { path: '/incidents', element: entity(resources.incidents) },
          { path: '/common-areas', element: entity(resources.commonAreas) },
          { path: '/reservations', element: entity(resources.reservations) },
          { path: '/profile', element: <ProfilePage /> },
        ],
      },
    ],
  },
])
