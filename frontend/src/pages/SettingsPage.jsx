import { useEffect, useMemo, useState } from 'react'

import { api } from '../api/client'
import { Alert } from '../components/Alert'
import { EntityCard } from '../components/EntityCard'
import { Modal } from '../components/Modal'
import { useAuthStore } from '../store/authStore'
import { extractApiError } from '../utils/apiError'

const tabs = [
  { key: 'condominios', label: 'Condomínios' },
  { key: 'usuarios', label: 'Usuários' },
  { key: 'assistente', label: 'Assistente' },
  { key: 'menu-paginas', label: 'Menu/Páginas' },
]

const roleOptions = [
  { value: 'PLATFORM_ADMIN', label: 'Admin da Plataforma' },
  { value: 'SINDICO', label: 'Síndico' },
  { value: 'PORTEIRO', label: 'Porteiro' },
  { value: 'MORADOR', label: 'Morador' },
]

function SectionMessage({ error, success }) {
  return (
    <>
      <Alert type="success" message={success} />
      <Alert type="error" message={error} />
    </>
  )
}

export function SettingsPage() {
  const { user, activeCondominiumId, setActiveCondominium } = useAuthStore()
  const [tab, setTab] = useState('condominios')
  const [condos, setCondos] = useState([])
  const [users, setUsers] = useState([])
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [condoModalOpen, setCondoModalOpen] = useState(false)
  const [newCondo, setNewCondo] = useState({ name: '', document: '', address: '' })
  const [newUser, setNewUser] = useState({ first_name: '', last_name: '', email: '', password: '', role: 'SINDICO', condominium: '' })
  const [wizardStep, setWizardStep] = useState(1)
  const [wizard, setWizard] = useState({
    condominium_mode: 'existing',
    condominium_id: '',
    name: '',
    document: '',
    address: '',
    syndic_first_name: '',
    syndic_last_name: '',
    syndic_email: '',
    syndic_password: '',
    unit_mode: 'range',
    block: '',
    start: 101,
    end: 120,
    list_text: '',
    created_condominium_id: '',
  })

  const load = async () => {
    try {
      const [condoRes, userRes] = await Promise.all([api.get('/condominiums/'), api.get('/users/?page_size=200')])
      setCondos(condoRes.data.results || condoRes.data || [])
      setUsers(userRes.data.results || userRes.data || [])
    } catch (err) {
      setError(extractApiError(err))
    }
  }

  useEffect(() => { if (user?.role === 'PLATFORM_ADMIN') load() }, [user?.role])

  const filteredUsers = useMemo(() => {
    if (!activeCondominiumId) return users
    return users.filter((u) => String(u.condominium || '') === String(activeCondominiumId))
  }, [users, activeCondominiumId])

  if (user?.role !== 'PLATFORM_ADMIN') {
    return <Alert type="error" message="Apenas administradores da plataforma podem acessar Configurações." />
  }

  const handleCreateCondo = async (e) => {
    e.preventDefault()
    try {
      await api.post('/condominiums/', newCondo)
      setSuccess('Condomínio criado com sucesso.')
      setError('')
      setCondoModalOpen(false)
      setNewCondo({ name: '', document: '', address: '' })
      load()
    } catch (err) {
      setError(extractApiError(err))
    }
  }

  const handleCreateUser = async (e) => {
    e.preventDefault()
    try {
      await api.post('/users/', { ...newUser, condominium: newUser.condominium || null })
      setSuccess('Usuário criado com sucesso.')
      setError('')
      setNewUser({ first_name: '', last_name: '', email: '', password: '', role: 'SINDICO', condominium: activeCondominiumId || '' })
      load()
    } catch (err) {
      setError(extractApiError(err))
    }
  }

  const runWizardStep2 = async () => {
    try {
      const payload = {
        syndic_first_name: wizard.syndic_first_name,
        syndic_last_name: wizard.syndic_last_name,
        syndic_email: wizard.syndic_email,
        syndic_password: wizard.syndic_password,
      }
      if (wizard.condominium_mode === 'existing') payload.condominium_id = Number(wizard.condominium_id)
      else {
        payload.name = wizard.name
        payload.document = wizard.document
        payload.address = wizard.address
      }
      const { data } = await api.post('/condominiums/wizard/setup/', payload)
      setWizard((s) => ({ ...s, created_condominium_id: data.condominium_id }))
      setActiveCondominium(String(data.condominium_id))
      setWizardStep(3)
      setSuccess('Passo 2 concluído. Agora crie unidades em lote.')
      load()
    } catch (err) {
      setError(extractApiError(err))
    }
  }

  const finishWizard = async () => {
    try {
      await api.post(`/condominiums/${wizard.created_condominium_id}/bulk-units/`, {
        mode: wizard.unit_mode,
        block: wizard.block,
        start: Number(wizard.start),
        end: Number(wizard.end),
        list_text: wizard.list_text,
      })
      setSuccess('Assistente finalizado com sucesso!')
      setWizardStep(1)
      setWizard((s) => ({ ...s, created_condominium_id: '' }))
      load()
    } catch (err) {
      setError(extractApiError(err))
    }
  }

  return (
    <div>
      <h1>Configurações</h1>
      <SectionMessage error={error} success={success} />
      <div className="tabs">
        {tabs.map((t) => <button key={t.key} onClick={() => setTab(t.key)} className={tab === t.key ? 'active' : ''}>{t.label}</button>)}
      </div>

      {tab === 'condominios' && (
        <>
          <div className="page-head"><h2>Condomínios</h2><button onClick={() => setCondoModalOpen(true)}>Novo condomínio</button></div>
          <div className="cards-grid">
            {condos.map((item) => (
              <EntityCard
                key={item.id}
                title={item.name}
                subtitle={item.document || 'Sem documento'}
                meta={[item.address || 'Sem endereço']}
                onClick={() => setActiveCondominium(String(item.id))}
              />
            ))}
          </div>
          <Modal open={condoModalOpen} title="Novo condomínio" onClose={() => setCondoModalOpen(false)}>
            <form className="form-grid" onSubmit={handleCreateCondo}>
              <input placeholder="Nome do condomínio" value={newCondo.name} onChange={(e) => setNewCondo({ ...newCondo, name: e.target.value })} required />
              <input placeholder="Documento (CNPJ/CPF)" value={newCondo.document} onChange={(e) => setNewCondo({ ...newCondo, document: e.target.value })} />
              <input placeholder="Endereço" value={newCondo.address} onChange={(e) => setNewCondo({ ...newCondo, address: e.target.value })} />
              <button type="submit">Salvar condomínio</button>
            </form>
          </Modal>
        </>
      )}

      {tab === 'usuarios' && (
        <>
          <h2>Usuários</h2>
          <form className="form-grid" onSubmit={handleCreateUser}>
            <input placeholder="Nome" value={newUser.first_name} onChange={(e) => setNewUser({ ...newUser, first_name: e.target.value })} required />
            <input placeholder="Sobrenome" value={newUser.last_name} onChange={(e) => setNewUser({ ...newUser, last_name: e.target.value })} />
            <input placeholder="E-mail" type="email" value={newUser.email} onChange={(e) => setNewUser({ ...newUser, email: e.target.value })} required />
            <input placeholder="Senha" type="password" value={newUser.password} onChange={(e) => setNewUser({ ...newUser, password: e.target.value })} required />
            <select value={newUser.role} onChange={(e) => setNewUser({ ...newUser, role: e.target.value })}>
              {roleOptions.map((r) => <option key={r.value} value={r.value}>{r.label}</option>)}
            </select>
            <select value={newUser.condominium || ''} onChange={(e) => setNewUser({ ...newUser, condominium: e.target.value })}>
              <option value="">Sem condomínio</option>
              {condos.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
            <button type="submit">Criar usuário</button>
          </form>
          <div className="cards-grid">
            {filteredUsers.map((u) => (
              <EntityCard key={u.id} title={`${u.first_name || ''} ${u.last_name || ''}`.trim() || u.email} subtitle={u.email} meta={[roleOptions.find((r) => r.value === u.role)?.label || u.role]} />
            ))}
          </div>
        </>
      )}

      {tab === 'assistente' && (
        <div>
          <h2>Assistente de implantação</h2>
          {wizardStep === 1 && (
            <div className="form-grid">
              <select value={wizard.condominium_mode} onChange={(e) => setWizard({ ...wizard, condominium_mode: e.target.value })}>
                <option value="existing">Escolher condomínio existente</option>
                <option value="new">Criar novo condomínio</option>
              </select>
              {wizard.condominium_mode === 'existing' ? (
                <select value={wizard.condominium_id} onChange={(e) => setWizard({ ...wizard, condominium_id: e.target.value })}>
                  <option value="">Selecione</option>
                  {condos.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
                </select>
              ) : (
                <>
                  <input placeholder="Nome do condomínio" value={wizard.name} onChange={(e) => setWizard({ ...wizard, name: e.target.value })} />
                  <input placeholder="Documento" value={wizard.document} onChange={(e) => setWizard({ ...wizard, document: e.target.value })} />
                  <input placeholder="Endereço" value={wizard.address} onChange={(e) => setWizard({ ...wizard, address: e.target.value })} />
                </>
              )}
              <button onClick={() => setWizardStep(2)}>Próximo</button>
            </div>
          )}

          {wizardStep === 2 && (
            <div className="form-grid">
              <input placeholder="Nome do síndico" value={wizard.syndic_first_name} onChange={(e) => setWizard({ ...wizard, syndic_first_name: e.target.value })} />
              <input placeholder="Sobrenome" value={wizard.syndic_last_name} onChange={(e) => setWizard({ ...wizard, syndic_last_name: e.target.value })} />
              <input placeholder="E-mail do síndico" type="email" value={wizard.syndic_email} onChange={(e) => setWizard({ ...wizard, syndic_email: e.target.value })} />
              <input placeholder="Senha" type="password" value={wizard.syndic_password} onChange={(e) => setWizard({ ...wizard, syndic_password: e.target.value })} />
              <button onClick={runWizardStep2}>Criar síndico e continuar</button>
            </div>
          )}

          {wizardStep === 3 && (
            <div className="form-grid">
              <select value={wizard.unit_mode} onChange={(e) => setWizard({ ...wizard, unit_mode: e.target.value })}>
                <option value="range">Intervalo</option>
                <option value="list">Lista</option>
              </select>
              <input placeholder="Bloco/Torre" value={wizard.block} onChange={(e) => setWizard({ ...wizard, block: e.target.value })} />
              {wizard.unit_mode === 'range' ? (
                <>
                  <input placeholder="Início" type="number" value={wizard.start} onChange={(e) => setWizard({ ...wizard, start: e.target.value })} />
                  <input placeholder="Fim" type="number" value={wizard.end} onChange={(e) => setWizard({ ...wizard, end: e.target.value })} />
                </>
              ) : (
                <textarea placeholder="Uma unidade por linha (A-101 ou 101)" value={wizard.list_text} onChange={(e) => setWizard({ ...wizard, list_text: e.target.value })} />
              )}
              <button onClick={finishWizard}>Finalizar assistente</button>
            </div>
          )}
        </div>
      )}

      {tab === 'menu-paginas' && <p>Configuração avançada de menu/páginas permanece disponível em versão futura sem impactar o fluxo principal.</p>}
    </div>
  )
}
