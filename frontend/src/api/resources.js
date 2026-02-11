export const STORE_OPTIONS = ['Shopee', 'Mercado Livre', 'Amazon', 'AliExpress', 'Shein', 'Magalu', 'Americanas', 'Casas Bahia', 'Correios', 'Jadlog', 'Total Express', 'DHL', 'FedEx', 'UPS', 'Outros']
export const BANK_OPTIONS = ['Nubank', 'Inter', 'Itaú', 'Bradesco', 'Santander', 'Caixa', 'Banco do Brasil', 'C6', 'PicPay', 'BTG', 'Next', 'Original', 'Safra', 'Outros']

export const resources = {
  units: {
    title: 'Unidades',
    endpoint: '/units/',
    fields: [
      { name: 'code', label: 'Código', required: true },
      { name: 'block', label: 'Bloco' },
    ],
    card: (item) => ({ title: `${item.code}`, subtitle: `Bloco ${item.block || '-'}`, meta: [`ID ${item.id}`] }),
  },
  residents: {
    title: 'Moradores',
    endpoint: '/residents/',
    fields: [
      { name: 'full_name', label: 'Nome', required: true },
      { name: 'phone', label: 'Telefone' },
      { name: 'unit', label: 'Unidade', required: true, type: 'number' },
      { name: 'document', label: 'Documento' },
      { name: 'notes', label: 'Observações' },
      { name: 'photo_url', label: 'Foto (URL)' },
    ],
    card: (item) => ({ title: item.full_name, subtitle: `Unidade ${item.unit}`, meta: [item.phone || 'Sem telefone'] }),
    groupBy: (item) => `Unidade ${item.unit}`,
  },
  visitors: {
    title: 'Visitantes',
    endpoint: '/visitors/',
    fields: [
      { name: 'full_name', label: 'Nome', required: true },
      { name: 'document', label: 'Documento', required: true },
      { name: 'unit', label: 'Unidade', type: 'number' },
    ],
    card: (item) => ({ title: item.full_name, subtitle: item.document, meta: [item.unit ? `Unidade ${item.unit}` : 'Sem unidade'] }),
  },
  visitLogs: {
    title: 'Logs de Visita',
    endpoint: '/visit-logs/',
    fields: [
      { name: 'visitor', label: 'Visitante', required: true, type: 'number' },
      { name: 'entry_at', label: 'Entrada (ISO)', required: true },
      { name: 'exit_at', label: 'Saída (ISO)' },
      { name: 'notes', label: 'Observações' },
    ],
    card: (item) => ({ title: `Visitante #${item.visitor}`, subtitle: `Entrada: ${item.entry_at}`, meta: [item.exit_at ? `Saída: ${item.exit_at}` : 'Em andamento'] }),
  },
  packages: {
    title: 'Encomendas',
    endpoint: '/packages/',
    fields: [
      { name: 'unit', label: 'Unidade', required: true, type: 'number' },
      { name: 'resident', label: 'Destinatário (Resident ID)', type: 'number' },
      { name: 'delivery_type', label: 'Tipo (LETTER/PACKAGE)', required: true },
      { name: 'store', label: 'Loja' },
      { name: 'bank', label: 'Banco' },
      { name: 'other_store', label: 'Outra loja' },
      { name: 'other_bank', label: 'Outro banco' },
      { name: 'description', label: 'Descrição', required: true },
    ],
    card: (item) => ({ title: item.description, subtitle: `Unidade ${item.unit}`, meta: [item.delivery_type, item.store || item.bank || '-'] }),
  },
  announcements: {
    title: 'Comunicados',
    endpoint: '/announcements/',
    fields: [
      { name: 'title', label: 'Título', required: true },
      { name: 'content', label: 'Conteúdo', required: true },
    ],
    card: (item) => ({ title: item.title, subtitle: item.content?.slice(0, 90), meta: [] }),
  },
  incidents: {
    title: 'Ocorrências',
    endpoint: '/incidents/',
    fields: [
      { name: 'title', label: 'Título', required: true },
      { name: 'description', label: 'Descrição', required: true },
      { name: 'status', label: 'Status', required: true },
    ],
    card: (item) => ({ title: item.title, subtitle: item.description?.slice(0, 90), meta: [item.status] }),
  },
  commonAreas: {
    title: 'Áreas Comuns',
    endpoint: '/common-areas/',
    fields: [
      { name: 'name', label: 'Nome', required: true },
      { name: 'description', label: 'Descrição' },
    ],
    card: (item) => ({ title: item.name, subtitle: item.description, meta: [] }),
  },
  reservations: {
    title: 'Reservas',
    endpoint: '/reservations/',
    fields: [
      { name: 'common_area', label: 'Área Comum', required: true, type: 'number' },
      { name: 'unit', label: 'Unidade', required: true, type: 'number' },
      { name: 'start_at', label: 'Início (ISO)', required: true },
      { name: 'end_at', label: 'Fim (ISO)', required: true },
      { name: 'status', label: 'Status', required: true },
    ],
    card: (item) => ({ title: `Reserva #${item.id}`, subtitle: `${item.start_at} → ${item.end_at}`, meta: [item.status] }),
  },
}
