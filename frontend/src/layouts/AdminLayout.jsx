import { Link, Outlet } from 'react-router-dom'
import { useAuthStore } from '../store/authStore'

const menu = [
  ['Condomínios', '/condominiums'],
  ['Unidades', '/units'],
  ['Moradores', '/residents'],
  ['Funcionários', '/staff'],
  ['Visitantes', '/visitors'],
  ['Logs de Visita', '/visit-logs'],
  ['Encomendas', '/packages'],
  ['Comunicados', '/announcements'],
  ['Ocorrências', '/incidents'],
  ['Áreas Comuns', '/common-areas'],
  ['Reservas', '/reservations'],
]

export function AdminLayout() {
  const { user, logout } = useAuthStore()
  return (
    <div className="layout">
      <aside className="sidebar">
        <h2>CondoTools</h2>
        {menu.map(([label, path]) => (
          <Link key={path} to={path}>{label}</Link>
        ))}
      </aside>
      <main>
        <header className="topbar">
          <span>{user?.username} ({user?.role})</span>
          <button onClick={logout}>Sair</button>
        </header>
        <section className="content"><Outlet /></section>
      </main>
    </div>
  )
}
