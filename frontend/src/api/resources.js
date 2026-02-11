export const STORE_OPTIONS = ['Shopee', 'Mercado Livre', 'Amazon', 'AliExpress', 'Shein', 'Magalu', 'Americanas', 'Casas Bahia', 'Correios', 'Jadlog', 'Total Express', 'DHL', 'FedEx', 'UPS', 'Outros']
export const BANK_OPTIONS = ['Nubank', 'Inter', 'Itaú', 'Bradesco', 'Santander', 'Caixa', 'Banco do Brasil', 'C6', 'PicPay', 'BTG', 'Next', 'Original', 'Safra', 'Outros']

export const resources = {
  units: {
    permissions: { view: 'units.view', create: 'units.create', update: 'units.update', delete: 'units.delete' },
    title: 'Unidades',
    endpoint: '/units/',
    fields: [
      { name: 'number', label: 'Número da unidade', required: true },
      { name: 'block', label: 'Bloco/Torre' },
      { name: 'floor', label: 'Andar' },
      { name: 'notes', label: 'Observações', type: 'textarea' },
    ],
    card: (item) => ({ title: item.display_name || item.number, subtitle: item.floor ? `Andar ${item.floor}` : 'Sem andar informado', meta: [`${item.resident_count || 0} morador(es)`] }),
  },
  residents: {
    permissions: { view: 'residents.view', create: 'residents.create', update: 'residents.update', delete: 'residents.delete' },
    title: 'Moradores',
    endpoint: '/residents/',
    fields: [
      { name: 'full_name', label: 'Nome', required: true },
      { name: 'phone', label: 'Telefone' },
      { name: 'unit', label: 'Unidade', required: true, type: 'select', optionSource: 'units' },
      { name: 'document', label: 'Documento' },
      { name: 'notes', label: 'Observações', type: 'textarea' },
      { name: 'photo_url', label: 'Foto (URL)' },
    ],
    card: (item) => ({ title: item.full_name, subtitle: item.unit_display || `Unidade ${item.unit}`, meta: [item.phone || 'Sem telefone'] }),
    groupBy: (item) => item.unit_display || `Unidade ${item.unit}`,
  },
  visitors: {
    permissions: { view: 'visitors.view', create: 'visitors.create', update: 'visitors.update', delete: 'visitors.delete' },
    title: 'Visitantes',
    endpoint: '/visitors/',
    fields: [
      { name: 'full_name', label: 'Nome', required: true },
      { name: 'document', label: 'Documento', required: true },
      { name: 'unit', label: 'Unidade', type: 'select', optionSource: 'units' },
      { name: 'authorized_by', label: 'Autorizado por' },
      { name: 'notes', label: 'Observações', type: 'textarea' },
    ],
    card: (item) => ({ title: item.full_name, subtitle: item.document, meta: [item.unit_display || 'Sem unidade'] }),
  },
  visitLogs: {
    permissions: { view: 'visit_logs.view', create: 'visit_logs.create', update: 'visit_logs.update', delete: 'visit_logs.delete' },
    title: 'Logs de Visita',
    endpoint: '/visit-logs/',
    fields: [
      { name: 'visitor', label: 'Visitante', required: true, type: 'select', optionSource: 'visitors' },
      { name: 'entry_at', label: 'Entrada', required: true, type: 'datetime-local' },
      { name: 'exit_at', label: 'Saída', type: 'datetime-local' },
      { name: 'notes', label: 'Observações', type: 'textarea' },
    ],
    card: (item) => ({ title: `Visita #${item.id}`, subtitle: `Entrada: ${item.entry_at}`, meta: [item.exit_at ? `Saída: ${item.exit_at}` : 'Em andamento'] }),
  },
  packages: {
    permissions: { view: 'packages.view', create: 'packages.create', update: 'packages.update', delete: 'packages.delete' },
    title: 'Encomendas',
    endpoint: '/packages/',
    fields: [
      { name: 'unit', label: 'Unidade', required: true, type: 'select', optionSource: 'units' },
      { name: 'resident', label: 'Destinatário', type: 'select', optionSource: 'residents' },
      { name: 'delivery_type', label: 'Tipo de entrega', required: true, type: 'select', options: [
        { value: 'LETTER', label: 'Carta registrada' },
        { value: 'PACKAGE', label: 'Encomenda' },
      ] },
      { name: 'store', label: 'Loja' },
      { name: 'bank', label: 'Banco' },
      { name: 'other_store', label: 'Outra loja' },
      { name: 'other_bank', label: 'Outro banco' },
      { name: 'description', label: 'Descrição', required: true },
    ],
    card: (item) => ({ title: item.description, subtitle: item.unit_display || `Unidade ${item.unit}`, meta: [item.delivery_type, item.store || item.bank || '-'] }),
  },
  announcements: {
    permissions: { view: 'announcements.view', create: 'announcements.create', update: 'announcements.update', delete: 'announcements.delete' },
    title: 'Comunicados',
    endpoint: '/announcements/',
    fields: [
      { name: 'title', label: 'Título', required: true },
      { name: 'content', label: 'Conteúdo', required: true, type: 'textarea' },
    ],
    card: (item) => ({ title: item.title, subtitle: item.content?.slice(0, 90), meta: [] }),
  },
  incidents: {
    permissions: { view: 'occurrences.view', create: 'occurrences.create', update: 'occurrences.update', delete: 'occurrences.delete' },
    title: 'Ocorrências',
    endpoint: '/incidents/',
    fields: [
      { name: 'title', label: 'Título', required: true },
      { name: 'description', label: 'Descrição', required: true, type: 'textarea' },
      { name: 'status', label: 'Status', required: true },
    ],
    card: (item) => ({ title: item.title, subtitle: item.description?.slice(0, 90), meta: [item.status] }),
  },
  commonAreas: {
    permissions: { view: 'common_areas.view', create: 'common_areas.create', update: 'common_areas.update', delete: 'common_areas.delete' },
    title: 'Áreas Comuns',
    endpoint: '/common-areas/',
    fields: [
      { name: 'name', label: 'Nome', required: true },
      { name: 'description', label: 'Descrição', type: 'textarea' },
    ],
    card: (item) => ({ title: item.name, subtitle: item.description, meta: [] }),
  },
  reservations: {
    permissions: { view: 'reservations.view', create: 'reservations.create', update: 'reservations.update', delete: 'reservations.delete' },
    title: 'Reservas',
    endpoint: '/reservations/',
    fields: [
      { name: 'common_area', label: 'Área comum', required: true, type: 'select', optionSource: 'common-areas' },
      { name: 'unit', label: 'Unidade', required: true, type: 'select', optionSource: 'units' },
      { name: 'start_at', label: 'Início', required: true, type: 'datetime-local' },
      { name: 'end_at', label: 'Fim', required: true, type: 'datetime-local' },
      { name: 'status', label: 'Status', required: true },
    ],
    card: (item) => ({ title: `Reserva #${item.id}`, subtitle: `${item.start_at} → ${item.end_at}`, meta: [item.status] }),
  },
}
