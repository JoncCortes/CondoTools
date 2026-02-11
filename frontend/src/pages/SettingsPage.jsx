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

export function SettingsPage() {
  const { user, activeCondominiumId, setActiveCondominium } = useAuthStore()
  const [tab, setTab] = useState('condominios')
  const [condos, setCondos] = useState([])
  const [users, setUsers] = useState([])
  const [menuItems, setMenuItems] = useState([])
  const [error, setError] = useState('')
  const [success, setSuccess] = useState('')
  const [selectedCondo, setSelectedCondo] = useState(null)
  const [selectedUser, setSelectedUser] = useState(null)
  const [selectedMenu, setSelectedMenu] = useState(null)
  const [wizardStep, setWizardStep] = useState(1)

  const [newCondo, setNewCondo] = useState({ name: '', document: '', address: '' })
  const [newUser, setNewUser] = useState({ first_name: '', last_name: '', email: '', password: '', role: 'SINDICO', condominium: '' })
  const [wizard, setWizard] = useState({ condominium_mode: 'existing', condominium_id: '', name: '', document: '', address: '', syndic_first_name: '', syndic_last_name: '', syndic_email: '', syndic_password: '', unit_mode: 'range', block: '', start: 101, end: 120, list_text: '', created_condominium_id: '' })

  const load = async () => {
    try {
      const [condoRes, userRes, menuRes] = await Promise.all([
        api.get('/condominiums/'),
        api.get('/users/?page_size=200'),
        api.get('/settings/menu-items/?page_size=200'),
      ])
      setCondos(condoRes.data.results || condoRes.data || [])
      setUsers(userRes.data.results || userRes.data || [])
      setMenuItems(menuRes.data.results || menuRes.data || [])
    } catch (err) {
      if (import.meta.env.DEV) console.error('settings load error', err?.response?.data || err)
      setError(extractApiError(err))
    }
  }

  useEffect(() => { if (user?.role === 'PLATFORM_ADMIN') load() }, [user?.role])

  const filteredUsers = useMemo(() => {
    if (!activeCondominiumId) return users
    return users.filter((u) => String(u.condominium || '') === String(activeCondominiumId))
  }, [users, activeCondominiumId])

  if (user?.role !== 'PLATFORM_ADMIN') return <Alert type="error" message="Apenas administradores da plataforma podem acessar Configurações." />

  const handleError = (err, fallback = 'Não foi possível concluir a ação.') => {
    if (import.meta.env.DEV) console.error('settings action error', err?.response?.data || err)
    setError(extractApiError(err) || fallback)
    setSuccess('')
  }

  const createCondo = async (e) => {
    e.preventDefault()
    try {
      await api.post('/condominiums/', newCondo)
      setSuccess('Condomínio criado com sucesso.')
      setNewCondo({ name: '', document: '', address: '' })
      await load()
    } catch (err) { handleError(err) }
  }

  const saveCondo = async () => {
    try {
      await api.patch(`/condominiums/${selectedCondo.id}/`, selectedCondo)
      setSuccess('Condomínio atualizado com sucesso.')
      setSelectedCondo(null)
      await load()
    } catch (err) { handleError(err) }
  }

  const removeCondo = async (condo) => {
    if (!window.confirm(`Excluir condomínio "${condo.name}"?`)) return
    try {
      await api.delete(`/condominiums/${condo.id}/`)
      setSuccess('Condomínio removido.')
      if (String(activeCondominiumId) === String(condo.id)) {
        const remaining = condos.filter((c) => c.id !== condo.id)
        setActiveCondominium(remaining[0] ? String(remaining[0].id) : null)
      }
      await load()
    } catch (err) { handleError(err) }
  }

  const createUser = async (e) => {
    e.preventDefault()
    try {
      const payload = { ...newUser, condominium: newUser.role === 'PLATFORM_ADMIN' ? null : Number(newUser.condominium) }
      await api.post('/users/', payload)
      setSuccess('Usuário criado com sucesso.')
      setNewUser({ first_name: '', last_name: '', email: '', password: '', role: 'SINDICO', condominium: activeCondominiumId || '' })
      await load()
    } catch (err) { handleError(err) }
  }

  const saveUser = async () => {
    try {
      const payload = { ...selectedUser, condominium: selectedUser.role === 'PLATFORM_ADMIN' ? null : selectedUser.condominium }
      await api.patch(`/users/${selectedUser.id}/`, payload)
      setSuccess('Usuário atualizado com sucesso.')
      setSelectedUser(null)
      await load()
    } catch (err) { handleError(err) }
  }

  const removeUser = async (userItem) => {
    if (!window.confirm(`Excluir usuário ${userItem.email}?`)) return
    try {
      await api.delete(`/users/${userItem.id}/`)
      setSuccess('Usuário removido com sucesso.')
      setSelectedUser(null)
      await load()
    } catch (err) { handleError(err) }
  }

  const resetPassword = async (userItem) => {
    const password = window.prompt('Digite a nova senha:')
    if (!password) return
    try {
      await api.post(`/users/${userItem.id}/set-password/`, { password })
      setSuccess('Senha redefinida com sucesso.')
    } catch (err) { handleError(err) }
  }

  const saveMenuItem = async () => {
    try {
      await api.patch(`/settings/menu-items/${selectedMenu.id}/`, selectedMenu)
      setSuccess('Item de menu atualizado.')
      setSelectedMenu(null)
      await load()
    } catch (err) { handleError(err) }
  }

  const toggleMenuVisibility = async (item) => {
    try {
      await api.patch(`/settings/menu-items/${item.id}/`, { enabled: !item.enabled })
      await load()
    } catch (err) { handleError(err) }
  }

  const moveMenu = async (item, direction) => {
    try {
      await api.post(`/settings/menu-items/${item.id}/${direction === 'up' ? 'move-up' : 'move-down'}/`)
      await load()
    } catch (err) { handleError(err) }
  }

  const runWizardStep2 = async () => {
    try {
      const payload = { syndic_first_name: wizard.syndic_first_name, syndic_last_name: wizard.syndic_last_name, syndic_email: wizard.syndic_email, syndic_password: wizard.syndic_password }
      if (wizard.condominium_mode === 'existing') payload.condominium_id = Number(wizard.condominium_id)
      else Object.assign(payload, { name: wizard.name, document: wizard.document, address: wizard.address })
      const { data } = await api.post('/condominiums/wizard/setup/', payload)
      setWizard((s) => ({ ...s, created_condominium_id: data.condominium_id }))
      setActiveCondominium(String(data.condominium_id))
      setWizardStep(3)
      await load()
    } catch (err) { handleError(err) }
  }

  const finishWizard = async () => {
    try {
      await api.post(`/condominiums/${wizard.created_condominium_id}/bulk-units/`, { mode: wizard.unit_mode, block: wizard.block, start: Number(wizard.start), end: Number(wizard.end), list_text: wizard.list_text })
      setSuccess('Assistente finalizado com sucesso!')
      setWizardStep(1)
      setWizard((s) => ({ ...s, created_condominium_id: '' }))
      await load()
    } catch (err) { handleError(err) }
  }

  return (
    <div>
      <h1>Configurações</h1>
      <Alert type="success" message={success} />
      <Alert type="error" message={error} />
      <div className="tabs">{tabs.map((t) => <button key={t.key} onClick={() => setTab(t.key)} className={tab === t.key ? 'active' : ''}>{t.label}</button>)}</div>

      {tab === 'condominios' && (
        <>
          <h2>Condomínios</h2>
          <form className="form-grid" onSubmit={createCondo}>
            <input placeholder="Nome do condomínio" value={newCondo.name} onChange={(e) => setNewCondo({ ...newCondo, name: e.target.value })} required />
            <input placeholder="Documento" value={newCondo.document} onChange={(e) => setNewCondo({ ...newCondo, document: e.target.value })} />
            <input placeholder="Endereço" value={newCondo.address} onChange={(e) => setNewCondo({ ...newCondo, address: e.target.value })} />
            <button type="submit">Criar condomínio</button>
          </form>
          <div className="cards-grid">
            {condos.map((item) => <EntityCard key={item.id} title={item.name} subtitle={item.document || 'Sem documento'} meta={[item.address || 'Sem endereço']} onClick={() => setSelectedCondo(item)} />)}
          </div>
        </>
      )}

      {tab === 'usuarios' && (
        <>
          <h2>Usuários</h2>
          <form className="form-grid" onSubmit={createUser}>
            <input placeholder="Nome" value={newUser.first_name} onChange={(e) => setNewUser({ ...newUser, first_name: e.target.value })} required />
            <input placeholder="Sobrenome" value={newUser.last_name} onChange={(e) => setNewUser({ ...newUser, last_name: e.target.value })} />
            <input placeholder="E-mail" type="email" value={newUser.email} onChange={(e) => setNewUser({ ...newUser, email: e.target.value })} required />
            <input placeholder="Senha" type="password" value={newUser.password} onChange={(e) => setNewUser({ ...newUser, password: e.target.value })} required />
            <select value={newUser.role} onChange={(e) => setNewUser({ ...newUser, role: e.target.value, condominium: e.target.value === 'PLATFORM_ADMIN' ? '' : newUser.condominium })}>
              {roleOptions.map((r) => <option key={r.value} value={r.value}>{r.label}</option>)}
            </select>
            <select disabled={newUser.role === 'PLATFORM_ADMIN'} value={newUser.condominium || ''} onChange={(e) => setNewUser({ ...newUser, condominium: e.target.value })} required={newUser.role !== 'PLATFORM_ADMIN'}>
              <option value="">Selecione condomínio</option>
              {condos.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}
            </select>
            <button type="submit">Criar usuário</button>
          </form>
          <div className="cards-grid">
            {filteredUsers.map((u) => (
              <EntityCard key={u.id} title={`${u.first_name || ''} ${u.last_name || ''}`.trim() || u.email} subtitle={u.email} meta={[roleOptions.find((r) => r.value === u.role)?.label || u.role, condos.find((c) => c.id === u.condominium)?.name || 'Sem condomínio']} onClick={() => setSelectedUser(u)} />
            ))}
          </div>
        </>
      )}

      {tab === 'assistente' && (
        <div>
          <h2>Assistente de implantação</h2>
          {wizardStep === 1 && <div className="form-grid"><select value={wizard.condominium_mode} onChange={(e) => setWizard({ ...wizard, condominium_mode: e.target.value })}><option value="existing">Escolher condomínio existente</option><option value="new">Criar novo condomínio</option></select>{wizard.condominium_mode === 'existing' ? <select value={wizard.condominium_id} onChange={(e) => setWizard({ ...wizard, condominium_id: e.target.value })}><option value="">Selecione</option>{condos.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}</select> : <><input placeholder="Nome do condomínio" value={wizard.name} onChange={(e) => setWizard({ ...wizard, name: e.target.value })} /><input placeholder="Documento" value={wizard.document} onChange={(e) => setWizard({ ...wizard, document: e.target.value })} /><input placeholder="Endereço" value={wizard.address} onChange={(e) => setWizard({ ...wizard, address: e.target.value })} /></>}<button onClick={() => setWizardStep(2)}>Próximo</button></div>}
          {wizardStep === 2 && <div className="form-grid"><input placeholder="Nome do síndico" value={wizard.syndic_first_name} onChange={(e) => setWizard({ ...wizard, syndic_first_name: e.target.value })} /><input placeholder="Sobrenome" value={wizard.syndic_last_name} onChange={(e) => setWizard({ ...wizard, syndic_last_name: e.target.value })} /><input placeholder="E-mail do síndico" type="email" value={wizard.syndic_email} onChange={(e) => setWizard({ ...wizard, syndic_email: e.target.value })} /><input placeholder="Senha" type="password" value={wizard.syndic_password} onChange={(e) => setWizard({ ...wizard, syndic_password: e.target.value })} /><button onClick={runWizardStep2}>Criar síndico e continuar</button></div>}
          {wizardStep === 3 && <div className="form-grid"><select value={wizard.unit_mode} onChange={(e) => setWizard({ ...wizard, unit_mode: e.target.value })}><option value="range">Intervalo</option><option value="list">Lista</option></select><input placeholder="Bloco/Torre" value={wizard.block} onChange={(e) => setWizard({ ...wizard, block: e.target.value })} />{wizard.unit_mode === 'range' ? <><input placeholder="Início" type="number" value={wizard.start} onChange={(e) => setWizard({ ...wizard, start: e.target.value })} /><input placeholder="Fim" type="number" value={wizard.end} onChange={(e) => setWizard({ ...wizard, end: e.target.value })} /></> : <textarea placeholder="Uma unidade por linha (A-101 ou 101)" value={wizard.list_text} onChange={(e) => setWizard({ ...wizard, list_text: e.target.value })} />}<button onClick={finishWizard}>Finalizar assistente</button></div>}
        </div>
      )}

      {tab === 'menu-paginas' && (
        <div>
          <h2>Menu/Páginas</h2>
          <div className="cards-grid">
            {menuItems.sort((a, b) => a.order - b.order).map((item) => (
              <EntityCard
                key={item.id}
                title={item.label}
                subtitle={`${item.path} • Ordem ${item.order}`}
                meta={[item.enabled ? 'Visível' : 'Oculto', item.condominium ? `Condomínio #${item.condominium}` : 'Global']}
                onClick={() => setSelectedMenu(item)}
              />
            ))}
          </div>
          <div className="row-actions">
            <button onClick={() => load()}>Atualizar</button>
          </div>
        </div>
      )}

      <Modal open={!!selectedCondo} title="Condomínio" onClose={() => setSelectedCondo(null)}>
        {selectedCondo && <div className="form-grid"><input value={selectedCondo.name || ''} onChange={(e) => setSelectedCondo({ ...selectedCondo, name: e.target.value })} /><input value={selectedCondo.document || ''} onChange={(e) => setSelectedCondo({ ...selectedCondo, document: e.target.value })} /><input value={selectedCondo.address || ''} onChange={(e) => setSelectedCondo({ ...selectedCondo, address: e.target.value })} /><div className="row-actions"><button onClick={() => setActiveCondominium(String(selectedCondo.id))}>Selecionar como ativo</button><button onClick={saveCondo}>Salvar</button><button className="danger" onClick={() => removeCondo(selectedCondo)}>Excluir</button></div></div>}
      </Modal>

      <Modal open={!!selectedUser} title="Usuário" onClose={() => setSelectedUser(null)}>
        {selectedUser && <div className="form-grid"><input value={selectedUser.first_name || ''} onChange={(e) => setSelectedUser({ ...selectedUser, first_name: e.target.value })} /><input value={selectedUser.last_name || ''} onChange={(e) => setSelectedUser({ ...selectedUser, last_name: e.target.value })} /><input value={selectedUser.email || ''} onChange={(e) => setSelectedUser({ ...selectedUser, email: e.target.value })} /><select value={selectedUser.role} onChange={(e) => setSelectedUser({ ...selectedUser, role: e.target.value, condominium: e.target.value === 'PLATFORM_ADMIN' ? null : selectedUser.condominium })}>{roleOptions.map((r) => <option key={r.value} value={r.value}>{r.label}</option>)}</select><select disabled={selectedUser.role === 'PLATFORM_ADMIN'} value={selectedUser.condominium || ''} onChange={(e) => setSelectedUser({ ...selectedUser, condominium: Number(e.target.value) })}><option value="">Selecione condomínio</option>{condos.map((c) => <option key={c.id} value={c.id}>{c.name}</option>)}</select><div className="row-actions"><button onClick={saveUser}>Salvar</button><button onClick={() => resetPassword(selectedUser)}>Resetar senha</button><button className="danger" onClick={() => removeUser(selectedUser)}>Excluir</button></div></div>}
      </Modal>

      <Modal open={!!selectedMenu} title="Item de Menu" onClose={() => setSelectedMenu(null)}>
        {selectedMenu && <div className="form-grid"><input value={selectedMenu.label || ''} onChange={(e) => setSelectedMenu({ ...selectedMenu, label: e.target.value })} /><input value={selectedMenu.path || ''} onChange={(e) => setSelectedMenu({ ...selectedMenu, path: e.target.value })} /><input value={selectedMenu.icon || ''} onChange={(e) => setSelectedMenu({ ...selectedMenu, icon: e.target.value })} placeholder="Ícone" /><label><input type="checkbox" checked={!!selectedMenu.enabled} onChange={(e) => setSelectedMenu({ ...selectedMenu, enabled: e.target.checked })} /> Visível</label><div className="row-actions"><button onClick={saveMenuItem}>Salvar</button><button onClick={() => toggleMenuVisibility(selectedMenu)}>{selectedMenu.enabled ? 'Ocultar' : 'Mostrar'}</button><button onClick={() => moveMenu(selectedMenu, 'up')}>Subir</button><button onClick={() => moveMenu(selectedMenu, 'down')}>Descer</button></div></div>}
      </Modal>
    </div>
  )
}
