import { useState } from 'react'
import { Navigate } from 'react-router-dom'

import { api } from '../api/client'
import { Alert } from '../components/Alert'
import { useAuthStore } from '../store/authStore'

export function LoginPage() {
  const { login, accessToken, isLoading } = useAuthStore()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')

  if (accessToken) return <Navigate to="/dashboard" replace />

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!email || !password) {
      setError('Informe email e senha.')
      return
    }
    try {
      await login(email, password, api)
    } catch {
      setError('Credenciais inválidas.')
    }
  }

  return (
    <div className="auth-wrapper">
      <div className="auth-card">
        <h1>CondoTools</h1>
        <p>Faça login para continuar</p>
        <form onSubmit={handleSubmit} className="auth-form">
          <input placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} />
          <input type="password" placeholder="Senha" value={password} onChange={(e) => setPassword(e.target.value)} />
          <button type="submit" disabled={isLoading}>{isLoading ? 'Entrando...' : 'Entrar'}</button>
        </form>
        <Alert type="error" message={error} />
      </div>
    </div>
  )
}
