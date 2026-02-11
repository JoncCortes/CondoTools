import { useAuthStore } from '../store/authStore'

export function DashboardPage() {
  const user = useAuthStore((s) => s.user)

  return (
    <div>
      <h1>Dashboard</h1>
      <p>Bem-vindo, {user?.first_name || user?.email}.</p>
      <p>Perfil: <strong>{user?.role}</strong></p>
      <p>Condomínio ID: <strong>{user?.condominium || 'N/A'}</strong></p>
    </div>
  )
}
