import { useAuthStore } from '../store/authStore'

export function ProfilePage() {
  const user = useAuthStore((s) => s.user)

  return (
    <div>
      <h1>Perfil</h1>
      <div className="profile-card">
        <p><strong>Email:</strong> {user?.email}</p>
        <p><strong>Nome:</strong> {user?.first_name} {user?.last_name}</p>
        <p><strong>Role:</strong> {user?.role}</p>
        <p><strong>Condomínio:</strong> {user?.condominium || 'Sem condomínio (platform)'}</p>
      </div>
    </div>
  )
}
