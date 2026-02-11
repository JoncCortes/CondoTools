import { Link, Outlet, useLocation } from 'react-router-dom'
import { useEffect, useMemo, useState } from 'react'

import { api } from '../api/client'
import { staticMenuByRole } from '../constants/roles'
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
  '/settings': 'Configurações',
}

export function AppLayout() {
  const location = useLocation()
  const { user, clearAuth, activeCondominiumId, setActiveCondominium } = useAuthStore()
  const [menu, setMenu] = useState(null)
  const [condos, setCondos] = useState([])

  useEffect(() => {
    api.get('/menu/').then((res) => setMenu(res.data)).catch(() => setMenu(null))
    if (user?.role === 'PLATFORM_ADMIN') {
      api.get('/condominiums/').then((res) => setCondos(res.data.results || res.data || []))
    }
  }, [user?.role])

  const allowedLinks = useMemo(() => {
    if (menu?.menu_items?.length) return menu.menu_items.map((x) => x.path)
    return staticMenuByRole[user?.role] || []
  }, [menu, user?.role])

  return (
    <div className="layout">
      <aside className="sidebar">
        <h2>CondoTools</h2>
        {allowedLinks.map((path) => (
          <Link key={path} className={location.pathname === path ? 'active' : ''} to={path}>
            {labels[path] || path}
          </Link>
        ))}
        {(menu?.custom_pages || []).map((p) => (
          <Link key={p.slug} to={`/pages/${p.slug}`}>{p.title}</Link>
        ))}
      </aside>
      <main>
        <header className="topbar">
          <div className="top-left">
            <span>{user?.email} • {user?.role}</span>
            {user?.role === 'PLATFORM_ADMIN' && (
              <select value={activeCondominiumId || ''} onChange={(e) => setActiveCondominium(e.target.value || null)}>
                <option value="">Selecione condomínio ativo</option>
                {condos.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
              </select>
            )}
          </div>
          <button onClick={clearAuth}>Sair</button>
        </header>
        <section className="content"><Outlet /></section>
      </main>
    </div>
  )
}
