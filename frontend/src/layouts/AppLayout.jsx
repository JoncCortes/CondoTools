import { Link, Outlet, useLocation } from 'react-router-dom'

import { menuByRole } from '../constants/roles'
import { useAuthStore } from '../store/authStore'

const labels = {
  '/dashboard': 'Dashboard',
  '/units': 'Unidades',
  '/residents': 'Moradores',
  '/visitors': 'Visitantes',
  '/visit-logs': 'Logs de visita',
  '/packages': 'Encomendas',
  '/announcements': 'Comunicados',
  '/incidents': 'Ocorrências',
  '/common-areas': 'Áreas comuns',
  '/reservations': 'Reservas',
  '/profile': 'Perfil',
}

export function AppLayout() {
  const location = useLocation()
  const { user, clearAuth } = useAuthStore()
  const allowedLinks = menuByRole[user?.role] || []

  return (
    <div className="layout">
      <aside className="sidebar">
        <h2>CondoTools</h2>
        {allowedLinks.map((path) => (
          <Link key={path} className={location.pathname === path ? 'active' : ''} to={path}>
            {labels[path]}
          </Link>
        ))}
      </aside>
      <main>
        <header className="topbar">
          <span>{user?.email} • {user?.role}</span>
          <button onClick={clearAuth}>Sair</button>
        </header>
        <section className="content"><Outlet /></section>
      </main>
    </div>
  )
}
